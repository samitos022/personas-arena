import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import engine, SessionLocal
from models import Base, Character, Question
from routers import arena, characters, leaderboard, persona, questions
from seed_data import CHARACTERS, QUESTIONS

logger = logging.getLogger("arena")


def _seed(db):
    """Populate characters and questions if the DB is empty."""
    if db.query(Character).count() > 0:
        return

    logger.info("Empty DB detected — running seed data.")
    char_map: dict[str, Character] = {}
    for c in CHARACTERS:
        char = Character(name=c["name"], slug=c["slug"], created_by="system")
        db.add(char)
        db.flush()
        char_map[c["slug"]] = char

    for slug, text, real_answer in QUESTIONS:
        db.add(Question(
            character_id=char_map[slug].id,
            text=text,
            real_answer=real_answer,
            added_by="system",
            approved=True,
        ))

    db.commit()
    logger.info("Seed complete: %d characters, %d questions.", len(char_map), len(QUESTIONS))


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        try:
            _seed(db)
        finally:
            db.close()
    except Exception:
        logger.exception("Startup DB init failed — app will still start.")
    yield


app = FastAPI(title="Personas Arena", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(characters.router)
app.include_router(questions.router)
app.include_router(persona.router)
app.include_router(arena.router)
app.include_router(leaderboard.router)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, next: str = ""):
    nickname = request.cookies.get("nickname")
    return templates.TemplateResponse(
        "home.html", {"request": request, "nickname": nickname, "next": next}
    )


@app.post("/nickname")
async def save_nickname(request: Request):
    form = await request.form()
    nickname = str(form.get("nickname", "")).strip()[:80]
    api_key = str(form.get("openrouter_key", "")).strip()
    next_url = str(form.get("next", "")).strip() or "/"
    if not next_url.startswith("/"):
        next_url = "/"
    if not nickname:
        return RedirectResponse(url="/", status_code=303)
    response = RedirectResponse(url=f"/{next_url.lstrip('/')}", status_code=303)
    response.set_cookie("nickname", nickname, max_age=60 * 60 * 24 * 365, httponly=True)
    if api_key:
        response.set_cookie("openrouter_key", api_key, max_age=60 * 60 * 24 * 365, httponly=True)
    return response


@app.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("nickname")
    response.delete_cookie("openrouter_key")
    return response
