from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Question

router = APIRouter()


@router.post("/questions/add")
async def add_question(
    request: Request,
    character_id: int = Form(...),
    text: str = Form(...),
    real_answer: str = Form(""),
    db: Session = Depends(get_db),
):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/", status_code=303)

    q = Question(
        character_id=character_id,
        text=text.strip(),
        real_answer=real_answer.strip() or None,
        added_by=nickname,
        approved=False,
    )
    db.add(q)
    db.commit()
    return RedirectResponse(url=f"/character/{character_id}", status_code=303)


@router.post("/questions/{question_id}/approve")
def approve_question(request: Request, question_id: int, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/", status_code=303)
    q = db.get(Question, question_id)
    if q:
        q.approved = True
        db.commit()
        return RedirectResponse(url=f"/character/{q.character_id}", status_code=303)
    return RedirectResponse(url="/characters", status_code=303)


@router.post("/questions/{question_id}/delete")
def delete_question(request: Request, question_id: int, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/", status_code=303)
    q = db.get(Question, question_id)
    if q:
        char_id = q.character_id
        db.delete(q)
        db.commit()
        return RedirectResponse(url=f"/character/{char_id}", status_code=303)
    return RedirectResponse(url="/characters", status_code=303)
