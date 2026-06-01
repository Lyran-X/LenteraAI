import uuid
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


TutorMode = Literal[
    "explain_simply",
    "step_by_step",
    "socratic",
    "give_example",
    "practice_question",
]
AnswerLength = Literal["concise", "balanced", "detailed"]
QuizDifficulty = Literal["easy", "medium", "hard", "adaptive"]


class ProfilePreferences(BaseModel):
    preferred_learning_style: str = "step_by_step"
    daily_study_duration: str = "45"
    preferred_quiz_difficulty: QuizDifficulty = "adaptive"
    target_subject: str | None = None
    reminder_time: str | None = None


class AISettings(BaseModel):
    default_tutor_mode: TutorMode = "explain_simply"
    answer_length: AnswerLength = "balanced"
    citation_required: bool = True
    socratic_mode_enabled: bool = False


class ProfileResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: str
    avatar_url: str | None = None
    learning_level: str | None = None
    current_streak: int = 0
    completed_quizzes: int = 0
    preferences: ProfilePreferences = Field(default_factory=ProfilePreferences)
    ai_settings: AISettings = Field(default_factory=AISettings)

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    learning_level: str | None = Field(default=None, max_length=120)
    target_subject: str | None = Field(default=None, max_length=160)
    preferred_learning_style: str | None = Field(default=None, max_length=80)
    daily_study_duration: str | int | None = Field(default=None)
    preferred_quiz_difficulty: QuizDifficulty | None = None
    reminder_time: str | None = Field(default=None, max_length=16)


class AISettingsUpdateRequest(BaseModel):
    default_tutor_mode: TutorMode | None = None
    answer_length: AnswerLength | None = None
    citation_required: bool | None = None
    socratic_mode_enabled: bool | None = None


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class ProfileMessageResponse(BaseModel):
    message: str


class ProfileExportResponse(BaseModel):
    profile: ProfileResponse
    notes_count: int
    quizzes_summary: dict[str, Any]
    study_plans_summary: dict[str, Any]