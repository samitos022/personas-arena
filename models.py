from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float,
    DateTime, ForeignKey, CheckConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    real_person = Column(String(120), nullable=False)
    uploaded_by = Column(String(80), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    phrases = relationship("Phrase", back_populates="persona", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="persona")


class Phrase(Base):
    __tablename__ = "phrases"

    id = Column(Integer, primary_key=True)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    text = Column(Text, nullable=False)
    type = Column(String(4), nullable=False)   # "ai" | "real"
    word_count = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("type IN ('ai', 'real')", name="ck_phrase_type"),
    )

    persona = relationship("Persona", back_populates="phrases")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    evaluator_nickname = Column(String(80), nullable=False)
    persona_id = Column(Integer, ForeignKey("personas.id"), nullable=False)
    ai_phrase_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    real_phrase_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    chosen_id = Column(Integer, ForeignKey("phrases.id"), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    persona = relationship("Persona", back_populates="evaluations")
    ai_phrase = relationship("Phrase", foreign_keys=[ai_phrase_id])
    real_phrase = relationship("Phrase", foreign_keys=[real_phrase_id])
    chosen_phrase = relationship("Phrase", foreign_keys=[chosen_id])
