import uuid
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StudyPlanGenerateRequest(BaseModel):
    learning_goal: str = Field(min_length=3, max_length=500)
    subject: str = Field(min_length=2, max_length=160)
    topic: str = Field(min_length=2, max_length=160)
    deadline_date: date | None = None
    study_duration_per_day: int = Field(default=45, ge=10, le=480)
    understanding_level: str = Field(default="beginner", min_length=2, max_length=80)
    preferred_learning_style: str = Field(default="step_by_step", min_length=2, max_length=120)
    weak_topics: list[str] = Field(default_factory=list)

    @field_validator("weak_topics", mode="before")
    @classmethod
    def normalize_weak_topics(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [topic.strip() for topic in value.split(",") if topic.strip()]
        if isinstance(value, list):
            return [str(topic).strip() for topic in value if str(topic).strip()]
        return []


class StudyPlanItemUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=2000)
    estimated_minutes: int | None = Field(default=None, ge=5, le=300)
    priority: Priority | None = None
    recommended_resource: str | None = Field(default=None, max_length=500)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped:
            raise ValueError("Title cannot be empty.")
        return stripped

    @field_validator("description", "recommended_resource")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class StudyPlanItemRead(BaseModel):
    id: uuid.UUID
    day_number: int
    title: str
    description: str | None = None
    estimated_minutes: int | None = None
    priority: Priority = Priority.MEDIUM
    recommended_resource: str | None = None
    is_completed: bool
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class StudyPlanRead(BaseModel):
    id: uuid.UUID
    title: str
    description: str | None = None
    learning_goal: str | None = None
    subject: str | None = None
    topic: str | None = None
    deadline_date: date | None = None
    study_duration_per_day: int | None = None
    understanding_level: str | None = None
    preferred_learning_style: str | None = None
    weak_topics: list[str] = Field(default_factory=list)
    status: str
    progress_percentage: int
    generation_message: str | None = None
    items: list[StudyPlanItemRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

