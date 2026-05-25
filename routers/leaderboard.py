from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from database import get_db
from models import Character, Evaluation, Persona

MIN_EVALUATIONS = 5

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _persona_stats(db: Session, persona_ids: list[int], phrase_ids: list[int]) -> dict:
    avr_total = db.query(func.count(Evaluation.id)).filter(
        Evaluation.persona_id.in_(persona_ids),
        Evaluation.mode == "ai_vs_real",
    ).scalar() or 0
    avr_fooled = db.query(func.count(Evaluation.id)).filter(
        Evaluation.persona_id.in_(persona_ids),
        Evaluation.mode == "ai_vs_real",
        Evaluation.picked_ai == True,
    ).scalar() or 0
    fool_rate = round(avr_fooled / avr_total * 100, 1) if avr_total >= MIN_EVALUATIONS else None

    ava_total = 0
    ava_wins = 0
    win_rate = None
    if phrase_ids:
        ava_total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.mode == "ai_vs_ai",
            or_(
                Evaluation.phrase_id.in_(phrase_ids),
                Evaluation.opponent_id.in_(phrase_ids),
            ),
        ).scalar() or 0
        ava_wins = db.query(func.count(Evaluation.id)).filter(
            Evaluation.mode == "ai_vs_ai",
            Evaluation.winner_id.in_(phrase_ids),
        ).scalar() or 0
        win_rate = round(ava_wins / ava_total * 100, 1) if ava_total >= MIN_EVALUATIONS else None

    return {
        "avr_total": avr_total,
        "fool_rate": fool_rate,
        "ava_total": ava_total,
        "win_rate": win_rate,
    }


def _sort_key(e: dict) -> tuple:
    return (
        e["fool_rate"] is not None or e["win_rate"] is not None,
        (e["fool_rate"] or 0) + (e["win_rate"] or 0),
    )


@router.get("/leaderboard")
def leaderboard(request: Request, db: Session = Depends(get_db)):
    personas = db.query(Persona).all()

    # --- Persona leaderboard ---
    entries = []
    for persona in personas:
        phrase_ids = [p.id for p in persona.phrases]
        stats = _persona_stats(db, [persona.id], phrase_ids)
        entries.append({"persona": persona, **stats})
    entries.sort(key=_sort_key, reverse=True)

    # --- Model leaderboard ---
    model_map: dict[str, list[Persona]] = {}
    for p in personas:
        model_map.setdefault(p.model, []).append(p)

    model_entries = []
    for model, model_personas in model_map.items():
        persona_ids = [p.id for p in model_personas]
        phrase_ids = [ph.id for p in model_personas for ph in p.phrases]
        stats = _persona_stats(db, persona_ids, phrase_ids)
        model_entries.append({
            "model": model,
            "model_short": model.split("/")[-1],
            "persona_count": len(model_personas),
            **stats,
        })
    model_entries.sort(key=_sort_key, reverse=True)

    # --- Evaluator leaderboard ---
    evaluator_rows = (
        db.query(Evaluation.evaluator_nickname)
        .distinct()
        .all()
    )
    evaluator_entries = []
    for (nick,) in evaluator_rows:
        total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nick
        ).scalar() or 0
        avr_count = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nick,
            Evaluation.mode == "ai_vs_real",
        ).scalar() or 0
        correct = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nick,
            Evaluation.mode == "ai_vs_real",
            Evaluation.picked_ai == False,
        ).scalar() or 0
        accuracy = round(correct / avr_count * 100, 1) if avr_count >= MIN_EVALUATIONS else None
        evaluator_entries.append({
            "nickname": nick,
            "total": total,
            "avr_count": avr_count,
            "correct": correct,
            "accuracy": accuracy,
        })
    evaluator_entries.sort(
        key=lambda e: (e["accuracy"] is not None, e["accuracy"] or 0, e["total"]),
        reverse=True,
    )

    # --- Current user stats ---
    nickname = request.cookies.get("nickname")
    user_stats = None
    if nickname:
        u_total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nickname
        ).scalar() or 0
        u_correct = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nickname,
            Evaluation.mode == "ai_vs_real",
            Evaluation.picked_ai == False,
        ).scalar() or 0
        if u_total:
            user_stats = {"total": u_total, "correct": u_correct}

    characters = db.query(Character).order_by(Character.name).all()

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "entries": entries,
            "model_entries": model_entries,
            "evaluator_entries": evaluator_entries,
            "min_evaluations": MIN_EVALUATIONS,
            "nickname": nickname,
            "user_stats": user_stats,
            "characters": characters,
        },
    )
