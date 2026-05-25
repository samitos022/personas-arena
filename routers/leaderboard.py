from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from database import get_db
from models import Character, Evaluation, Persona

MIN_EVALUATIONS = 5

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/leaderboard")
def leaderboard(request: Request, db: Session = Depends(get_db)):
    personas = db.query(Persona).all()

    entries = []
    for persona in personas:
        phrase_ids = [p.id for p in persona.phrases]

        # AI vs Real: fool rate (user picked AI = wrong)
        avr_total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.persona_id == persona.id,
            Evaluation.mode == "ai_vs_real",
        ).scalar() or 0
        avr_fooled = db.query(func.count(Evaluation.id)).filter(
            Evaluation.persona_id == persona.id,
            Evaluation.mode == "ai_vs_real",
            Evaluation.picked_ai == True,
        ).scalar() or 0
        fool_rate = round(avr_fooled / avr_total * 100, 1) if avr_total >= MIN_EVALUATIONS else None

        # AI vs AI: win rate
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

        entries.append({
            "persona": persona,
            "avr_total": avr_total,
            "fool_rate": fool_rate,
            "ava_total": ava_total,
            "win_rate": win_rate,
        })

    entries.sort(
        key=lambda e: (
            e["fool_rate"] is not None or e["win_rate"] is not None,
            (e["fool_rate"] or 0) + (e["win_rate"] or 0),
        ),
        reverse=True,
    )

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
            "min_evaluations": MIN_EVALUATIONS,
            "nickname": nickname,
            "user_stats": user_stats,
            "characters": characters,
        },
    )
