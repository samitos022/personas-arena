from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
from models import Evaluation, Persona

MIN_EVALUATIONS = 5

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/leaderboard")
def leaderboard(request: Request, db: Session = Depends(get_db)):
    personas = db.query(Persona).all()

    entries = []
    for persona in personas:
        total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.persona_id == persona.id
        ).scalar() or 0
        fooled = db.query(func.count(Evaluation.id)).filter(
            Evaluation.persona_id == persona.id,
            Evaluation.is_correct == False,
        ).scalar() or 0
        fool_rate = (fooled / total * 100) if total >= MIN_EVALUATIONS else None
        entries.append({
            "persona": persona,
            "total": total,
            "fooled": fooled,
            "fool_rate": fool_rate,
        })

    entries.sort(key=lambda e: (e["fool_rate"] is not None, e["fool_rate"] or 0), reverse=True)

    nickname = request.cookies.get("nickname")
    user_stats = None
    if nickname:
        user_total = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nickname
        ).scalar() or 0
        user_correct = db.query(func.count(Evaluation.id)).filter(
            Evaluation.evaluator_nickname == nickname,
            Evaluation.is_correct == True,
        ).scalar() or 0
        if user_total:
            user_stats = {
                "total": user_total,
                "correct": user_correct,
                "accuracy": round(user_correct / user_total * 100, 1),
            }

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "entries": entries,
            "min_evaluations": MIN_EVALUATIONS,
            "nickname": nickname,
            "user_stats": user_stats,
        },
    )
