from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Character, Question

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/characters")
def list_characters(request: Request, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    chars = db.query(Character).order_by(Character.name).all()
    return templates.TemplateResponse(
        "characters.html",
        {"request": request, "characters": chars, "nickname": nickname},
    )


@router.get("/character/{character_id}")
def character_detail(request: Request, character_id: int, db: Session = Depends(get_db)):
    char = db.get(Character, character_id)
    if not char:
        return RedirectResponse(url="/characters")
    nickname = request.cookies.get("nickname")
    approved_qs = [q for q in char.questions if q.approved]
    pending_qs = [q for q in char.questions if not q.approved]
    return templates.TemplateResponse(
        "character.html",
        {
            "request": request,
            "character": char,
            "approved_questions": approved_qs,
            "pending_questions": pending_qs,
            "nickname": nickname,
        },
    )


@router.post("/character/create")
async def create_character(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/", status_code=303)

    name = name.strip()
    slug = name.lower().replace(" ", "-")

    existing = db.query(Character).filter(Character.slug == slug).first()
    if existing:
        return RedirectResponse(url=f"/character/{existing.id}", status_code=303)

    char = Character(name=name, slug=slug, created_by=nickname)
    db.add(char)
    db.commit()
    return RedirectResponse(url=f"/character/{char.id}", status_code=303)
