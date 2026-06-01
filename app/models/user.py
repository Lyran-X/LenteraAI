import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="student",
        server_default="student",
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=text("true"),
    )
    avatar_url: Mapped[str | None] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        nullable=False,
        default=dict,
        server_default=text("'{}'::jsonb"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    uploaded_documents: Mapped[list["UploadedDocument"]] = relationship(
        "UploadedDocument",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    chat_sessions: Mapped[list["AIChatSession"]] = relationship(
        "AIChatSession",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    chat_messages: Mapped[list["AIChatMessage"]] = relationship(
        "AIChatMessage",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    study_plans: Mapped[list["StudyPlan"]] = relationship(
        "StudyPlan",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    quiz_attempts: Mapped[list["QuizAttempt"]] = relationship(
        "QuizAttempt",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    saved_notes: Mapped[list["SavedNote"]] = relationship(
        "SavedNote",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    analytics: Mapped[list["LearningAnalytics"]] = relationship(
        "LearningAnalytics",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )