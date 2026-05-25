from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    DateTime, ForeignKey, CheckConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, unique=True)   # "Donald Trump"
    slug = Column(String(80), nullable=False, unique=True)    # "donald-trump"
    created_by = Column(String(80), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    questions = relationship("Question", back_populates="character", cascade="all, delete-orphan")
    personas = relationship("Persona", back_populates="character", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    text = Column(Text, nullable=False)
    real_answer = Column(Text, nullable=True)   # if present → AI vs Real mode enabled
    added_by = Column(String(80), nullable=False)
    approved = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    character = relationship("Character", back_populates="questions")
    phrases = relationship("Phrase", back_populates="question", cascade="all, delete-orphan")


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    name = Column(String(200), nullable=False)       # "trump | sam | gpt-4o-mini"
    prompt_template = Column(Text, nullable=False)
    model = Column(String(120), nullable=False)      # OpenRouter model ID
    created_by = Column(String(80), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    character = relationship("Character", back_populates="personas")
    phrases = relationship("Phrase", back_populates="persona", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="persona", foreign_keys="Evaluation.persona_id")


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(Text, nullable=False)

    persona = relationship("Persona", back_populates="phrases")
    question = relationship("Question", back_populates="phrases")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    evaluator_nickname = Column(String(80), nullable=False)
    mode = Column(String(12), nullable=False)                          # "ai_vs_real" | "ai_vs_ai"
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    phrase_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("phrases.id"), nullable=True)   # ai_vs_ai only
    picked_ai = Column(Boolean, nullable=True)    # ai_vs_real: True = chose AI (wrong)
    winner_id = Column(Integer, ForeignKey("phrases.id"), nullable=True)     # ai_vs_ai: winning phrase
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        CheckConstraint("mode IN ('ai_vs_real', 'ai_vs_ai')", name="ck_eval_mode"),
    )

    persona = relationship("Persona", back_populates="evaluations", foreign_keys=[persona_id])
    question = relationship("Question")
    phrase = relationship("Phrase", foreign_keys=[phrase_id])
    opponent = relationship("Phrase", foreign_keys=[opponent_id])
    winner = relationship("Phrase", foreign_keys=[winner_id])
