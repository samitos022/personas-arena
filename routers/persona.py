import httpx
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Template, TemplateSyntaxError
from sqlalchemy.orm import Session

from database import get_db
from models import Character, Persona, Phrase, Question

router = APIRouter()
templates = Jinja2Templates(directory="templates")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

AVAILABLE_MODELS = [
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-haiku",
    "meta-llama/llama-3.1-70b-instruct",
    "google/gemini-flash-1.5",
    "mistralai/mistral-7b-instruct",
    "deepseek/deepseek-chat",
]


@router.get("/create")
def create_page(request: Request, character_id: int | None = None, db: Session = Depends(get_db)):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/?next=create")
    api_key = request.cookies.get("openrouter_key", "")
    characters = db.query(Character).order_by(Character.name).all()
    selected = db.get(Character, character_id) if character_id else None
    return templates.TemplateResponse(
        "create_persona.html",
        {
            "request": request,
            "nickname": nickname,
            "api_key_set": bool(api_key),
            "characters": characters,
            "selected_character": selected,
            "models": AVAILABLE_MODELS,
        },
    )


@router.post("/create")
async def create_persona(
    request: Request,
    character_id: int = Form(...),
    prompt_template: str = Form(...),
    model: str = Form(...),
    openrouter_key: str = Form(""),
    db: Session = Depends(get_db),
):
    nickname = request.cookies.get("nickname")
    if not nickname:
        return RedirectResponse(url="/", status_code=303)

    api_key = openrouter_key.strip() or request.cookies.get("openrouter_key", "")
    if not api_key:
        characters = db.query(Character).order_by(Character.name).all()
        return templates.TemplateResponse(
            "create_persona.html",
            {
                "request": request,
                "nickname": nickname,
                "api_key_set": False,
                "characters": characters,
                "selected_character": db.get(Character, character_id),
                "models": AVAILABLE_MODELS,
                "error": "OpenRouter API key required.",
            },
            status_code=422,
        )

    char = db.get(Character, character_id)
    if not char:
        return RedirectResponse(url="/create", status_code=303)

    model_short = model.split("/")[-1]
    persona_name = f"{char.slug} | {nickname} | {model_short}"

    persona = Persona(
        character_id=character_id,
        name=persona_name,
        prompt_template=prompt_template.strip(),
        model=model,
        created_by=nickname,
    )
    db.add(persona)
    db.flush()

    questions = db.query(Question).filter(
        Question.character_id == character_id,
        Question.approved == True,
    ).all()

    errors: list[str] = []
    for question in questions:
        try:
            system_prompt = Template(prompt_template).render(question=question.text)
            text = await _call_openrouter(api_key, model, system_prompt, question.text)
            db.add(Phrase(persona_id=persona.id, question_id=question.id, text=text))
        except TemplateSyntaxError as e:
            errors.append(f"Template error: {e}")
            break
        except Exception as e:
            errors.append(f"Q#{question.id}: {e}")

    db.commit()

    resp = RedirectResponse(url=f"/persona/{persona.id}", status_code=303)
    resp.set_cookie("openrouter_key", api_key, max_age=60 * 60 * 24 * 365, httponly=True)
    return resp


@router.get("/persona/{persona_id}")
def persona_detail(request: Request, persona_id: int, db: Session = Depends(get_db)):
    persona = db.get(Persona, persona_id)
    if not persona:
        return RedirectResponse(url="/leaderboard")
    nickname = request.cookies.get("nickname")
    phrases_with_q = [(p.question, p) for p in persona.phrases]
    return templates.TemplateResponse(
        "persona.html",
        {
            "request": request,
            "persona": persona,
            "phrases_with_q": phrases_with_q,
            "nickname": nickname,
        },
    )


async def _call_openrouter(api_key: str, model: str, system_prompt: str, question: str) -> str:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
            },
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
