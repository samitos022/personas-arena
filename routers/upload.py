import json
from fastapi import APIRouter, Depends, Form, Request, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models import Persona, Phrase

MIN_WORDS = 20
MIN_PHRASES_PER_TYPE = 3

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload")
async def upload_persona(
    request: Request,
    persona_name: str = Form(...),
    real_person: str = Form(...),
    nickname: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    error = None
    try:
        raw = await file.read()
        phrases_data = json.loads(raw)

        if not isinstance(phrases_data, list):
            raise ValueError("Il JSON deve essere un array.")

        valid: list[dict] = []
        for item in phrases_data:
            if not isinstance(item, dict) or "text" not in item or "type" not in item:
                continue
            if item["type"] not in ("ai", "real"):
                continue
            words = len(item["text"].split())
            if words < MIN_WORDS:
                continue
            valid.append({"text": item["text"].strip(), "type": item["type"], "word_count": words})

        ai_count = sum(1 for p in valid if p["type"] == "ai")
        real_count = sum(1 for p in valid if p["type"] == "real")

        if ai_count < MIN_PHRASES_PER_TYPE or real_count < MIN_PHRASES_PER_TYPE:
            raise ValueError(
                f"Servono almeno {MIN_PHRASES_PER_TYPE} frasi AI e {MIN_PHRASES_PER_TYPE} reali "
                f"con almeno {MIN_WORDS} parole ciascuna. "
                f"Trovate: {ai_count} AI, {real_count} reali."
            )

        persona = Persona(
            name=persona_name.strip(),
            real_person=real_person.strip(),
            uploaded_by=nickname.strip(),
        )
        db.add(persona)
        db.flush()

        for p in valid:
            db.add(Phrase(persona_id=persona.id, **p))

        db.commit()
        return RedirectResponse(url=f"/persona/{persona.id}", status_code=303)

    except (json.JSONDecodeError, ValueError) as exc:
        error = str(exc)

    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "error": error},
        status_code=422,
    )
