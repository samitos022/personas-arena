import random
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Evaluation, Persona, Phrase

MIN_EVALUATIONS_VISIBLE = 5

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _pick_round(db: Session, persona_id: int | None = None):
    """Return (persona, ai_phrase, real_phrase) or None if no valid persona exists."""
    query = db.query(Persona).join(Phrase).filter(Phrase.type == "ai")

    if persona_id:
        query = query.filter(Persona.id == persona_id)

    personas = query.all()
    random.shuffle(personas)

    for persona in personas:
        ai_phrases = [p for p in persona.phrases if p.type == "ai"]
        real_phrases = [p for p in persona.phrases if p.type == "real"]
        if ai_phrases and real_phrases:
            return persona, random.choice(ai_phrases), random.choice(real_phrases)

    return None


@router.get("/arena")
def arena_page(request: Request, persona_id: int | None = None, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/?next=arena")

    result = _pick_round(db, persona_id)
    if result is None:
        return templates.TemplateResponse(
            "arena.html",
            {"request": request, "error": "Nessuna persona disponibile.", "nickname": nickname},
        )

    persona, ai_phrase, real_phrase = result
    # Shuffle so user doesn't know which side is AI
    cards = [
        {"phrase": ai_phrase, "label": "A"},
        {"phrase": real_phrase, "label": "B"},
    ]
    random.shuffle(cards)

    return templates.TemplateResponse(
        "arena.html",
        {
            "request": request,
            "persona": persona,
            "cards": cards,
            "ai_phrase_id": ai_phrase.id,
            "real_phrase_id": real_phrase.id,
            "nickname": nickname,
        },
    )


@router.post("/arena/evaluate")
def evaluate(
    request: Request,
    persona_id: int = Form(...),
    ai_phrase_id: int = Form(...),
    real_phrase_id: int = Form(...),
    chosen_id: int = Form(...),
    db: Session = Depends(get_db),
):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/")

    is_correct = chosen_id == real_phrase_id

    ev = Evaluation(
        evaluator_nickname=nickname,
        persona_id=persona_id,
        ai_phrase_id=ai_phrase_id,
        real_phrase_id=real_phrase_id,
        chosen_id=chosen_id,
        is_correct=is_correct,
    )
    db.add(ev)
    db.commit()

    ai_phrase = db.get(Phrase, ai_phrase_id)
    real_phrase = db.get(Phrase, real_phrase_id)
    persona = db.get(Persona, persona_id)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "is_correct": is_correct,
            "ai_phrase": ai_phrase,
            "real_phrase": real_phrase,
            "persona": persona,
            "chosen_id": chosen_id,
            "nickname": nickname,
        },
    )


@router.get("/persona/{persona_id}")
def persona_detail(request: Request, persona_id: int, db: Session = Depends(get_db)):
    persona = db.get(Persona, persona_id)
    if persona is None:
        return RedirectResponse(url="/leaderboard")

    total = db.query(func.count(Evaluation.id)).filter(Evaluation.persona_id == persona_id).scalar()
    fooled = db.query(func.count(Evaluation.id)).filter(
        Evaluation.persona_id == persona_id, Evaluation.is_correct == False
    ).scalar()
    fool_rate = (fooled / total * 100) if total else None

    return templates.TemplateResponse(
        "persona.html",
        {
            "request": request,
            "persona": persona,
            "total": total,
            "fooled": fooled,
            "fool_rate": fool_rate,
            "min_visible": MIN_EVALUATIONS_VISIBLE,
        },
    )
