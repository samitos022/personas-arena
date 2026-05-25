import random
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Character, Evaluation, Phrase, Question

MIN_EVALUATIONS_VISIBLE = 5

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _pick_round(
    db: Session,
    character_id: int | None = None,
    nickname: str | None = None,
) -> dict | None:
    # Build sets of comparisons this user has already evaluated
    seen_avr: set[tuple[int, int]] = set()          # (question_id, phrase_id)
    seen_ava: set[tuple[int, frozenset]] = set()    # (question_id, frozenset{phrase_id, opponent_id})
    if nickname:
        for q_id, p_id in db.query(Evaluation.question_id, Evaluation.phrase_id).filter(
            Evaluation.evaluator_nickname == nickname,
            Evaluation.mode == "ai_vs_real",
        ).all():
            seen_avr.add((q_id, p_id))

        for q_id, p_id, o_id in db.query(
            Evaluation.question_id, Evaluation.phrase_id, Evaluation.opponent_id
        ).filter(
            Evaluation.evaluator_nickname == nickname,
            Evaluation.mode == "ai_vs_ai",
        ).all():
            seen_ava.add((q_id, frozenset({p_id, o_id})))

    query = db.query(Character)
    if character_id:
        query = query.filter(Character.id == character_id)

    characters = query.all()
    random.shuffle(characters)

    for char in characters:
        approved_qs = [q for q in char.questions if q.approved]
        random.shuffle(approved_qs)

        avr: list[tuple] = []   # (question, phrase)
        ava: list[tuple] = []   # (question, phrase_a, phrase_b)

        for q in approved_qs:
            phrases = q.phrases

            if q.real_answer and phrases:
                unseen = [p for p in phrases if (q.id, p.id) not in seen_avr]
                if unseen:
                    avr.append((q, random.choice(unseen)))

            by_persona: dict[int, list] = {}
            for p in phrases:
                by_persona.setdefault(p.persona_id, []).append(p)

            if len(by_persona) >= 2:
                persona_lists = list(by_persona.values())
                unseen_pairs: list[tuple] = []
                for i in range(len(persona_lists)):
                    for j in range(i + 1, len(persona_lists)):
                        pa = random.choice(persona_lists[i])
                        pb = random.choice(persona_lists[j])
                        if (q.id, frozenset({pa.id, pb.id})) not in seen_ava:
                            unseen_pairs.append((pa, pb))
                if unseen_pairs:
                    pa, pb = random.choice(unseen_pairs)
                    ava.append((q, pa, pb))

        modes = []
        if avr:
            modes.append("ai_vs_real")
        if ava:
            modes.append("ai_vs_ai")

        if not modes:
            continue

        mode = random.choice(modes)

        if mode == "ai_vs_real":
            q, phrase = random.choice(avr)
            return {"mode": "ai_vs_real", "character": char, "question": q, "phrase": phrase}
        else:
            q, pa, pb = random.choice(ava)
            if random.random() < 0.5:
                pa, pb = pb, pa
            return {"mode": "ai_vs_ai", "character": char, "question": q, "phrase_a": pa, "phrase_b": pb}

    return None


@router.get("/arena")
def arena_page(request: Request, character_id: int | None = None, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/?next=arena")

    round_data = _pick_round(db, character_id, nickname)
    if round_data is None:
        return templates.TemplateResponse(
            "arena.html",
            {"request": request, "error": "Hai già valutato tutti i confronti disponibili! Torna più tardi.", "nickname": nickname},
        )

    return templates.TemplateResponse(
        "arena.html",
        {"request": request, "round": round_data, "nickname": nickname},
    )


@router.post("/arena/evaluate")
async def evaluate(request: Request, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/")

    form = await request.form()
    mode = form.get("mode")
    question_id = int(form.get("question_id"))
    question = db.get(Question, question_id)

    if mode == "ai_vs_real":
        phrase_id = int(form.get("phrase_id"))
        picked_ai = form.get("chosen") == "ai"
        phrase = db.get(Phrase, phrase_id)

        db.add(Evaluation(
            evaluator_nickname=nickname,
            mode="ai_vs_real",
            persona_id=phrase.persona_id,
            question_id=question_id,
            phrase_id=phrase_id,
            picked_ai=picked_ai,
        ))
        db.commit()

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "mode": "ai_vs_real",
                "picked_ai": picked_ai,
                "phrase": phrase,
                "question": question,
                "nickname": nickname,
            },
        )

    else:  # ai_vs_ai
        phrase_a_id = int(form.get("phrase_a_id"))
        phrase_b_id = int(form.get("phrase_b_id"))
        winner_id = int(form.get("chosen"))

        phrase_a = db.get(Phrase, phrase_a_id)
        phrase_b = db.get(Phrase, phrase_b_id)
        winner = db.get(Phrase, winner_id)
        loser = phrase_b if winner_id == phrase_a_id else phrase_a

        db.add(Evaluation(
            evaluator_nickname=nickname,
            mode="ai_vs_ai",
            persona_id=phrase_a.persona_id,
            question_id=question_id,
            phrase_id=phrase_a_id,
            opponent_id=phrase_b_id,
            winner_id=winner_id,
        ))
        db.commit()

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "mode": "ai_vs_ai",
                "winner": winner,
                "loser": loser,
                "question": question,
                "nickname": nickname,
            },
        )
