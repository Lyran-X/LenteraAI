import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, Text, func, text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class LearningAnalytics(Base):
    __tablename__ = "learning_analytics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    activity_date: Mapped[date] = mapped_column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    source_document_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("uploaded_documents.id", ondelete="SET NULL"))
    last_quiz_attempt_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("quiz_attempts.id", ondelete="SET NULL"))
    study_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    ai_questions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    quiz_attempt_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    questions_answered: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    wrong_answers: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    avg_quiz_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    mastery_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    weakness_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    is_weak_topic: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default=text("false"))
    recommended_action: Mapped[str | None] = mapped_column(Text)
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, nullable=False, default=dict, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="analytics")