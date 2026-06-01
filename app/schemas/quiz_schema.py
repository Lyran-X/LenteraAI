import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class QuizSourceType(str, Enum):
    TOPIC = "topic"
    DOCUMENT = "document"
    MIXED = "mixed"


class QuizDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    ADAPTIVE = "adaptive"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"


class QuizGenerateRequest(BaseModel):
    source_type: QuizSourceType = QuizSourceType.TOPIC
    source_id: uuid.UUID | None = None
    document_id: uuid.UUID | None = None
    topic: str | None = Field(default=None, max_length=180)
    focus_topic: str | None = Field(default=None, max_length=180)
    difficulty: QuizDifficulty = QuizDifficulty.MEDIUM
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE
    language: str = Field(default="id")
    total_questions: int = Field(default=5, ge=1, le=20)

    @field_validator("language", mode="before")
    @classmethod
    def validate_language(cls, value: object) -> str:
        normalized = str(value or "id").strip().lower()
        if normalized not in {"id", "en"}:
            raise ValueError("language must be either id or en.")
        return normalized

    @field_validator("topic", "focus_topic", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @model_validator(mode="after")
    def validate_source_requirements(self) -> "QuizGenerateRequest":
        if self.source_type == QuizSourceType.DOCUMENT:
            if not (self.document_id or self.source_id):
                raise ValueError("document_id or source_id is required for document quizzes.")
            return self

        if not self.topic:
            raise ValueError("topic is required for topic quizzes.")
        if len(self.topic) < 2:
            raise ValueError("topic must be at least 2 characters.")
        return self


class QuizQuestionRead(BaseModel):
    id: uuid.UUID
    question_text: str
    question_type: QuestionType
    options: list[str] = Field(default_factory=list)
    correct_answer: str | None = None
    explanation: str | None = None
    topic: str | None = None
    difficulty: str
    order_index: int
    created_at: datetime
    updated_at: datetime


class QuizRead(BaseModel):
    id: uuid.UUID
    title: str
    source_type: str
    source_id: uuid.UUID | None = None
    topic: str | None = None
    difficulty: str
    question_type: QuestionType
    language: str = "id"
    total_questions: int
    generation_message: str | None = None
    questions: list[QuizQuestionRead] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class QuizSubmitAnswer(BaseModel):
    question_id: uuid.UUID
    user_answer: str | bool | int | float

    @field_validator("user_answer", mode="before")
    @classmethod
    def normalize_answer(cls, value: object) -> str:
        return str(value).strip()


class QuizSubmitRequest(BaseModel):
    answers: list[QuizSubmitAnswer]


class QuizAnswerResult(BaseModel):
    question_id: uuid.UUID
    question_text: str
    user_answer: str
    correct_answer: str
    is_correct: bool
    similarity_score: float | None = None
    feedback: str | None = None
    explanation: str | None = None
    topic: str | None = None


class QuizAttemptRead(BaseModel):
    id: uuid.UUID
    quiz_id: uuid.UUID
    quiz_title: str | None = None
    score: float
    total_questions: int
    correct_count: int
    wrong_count: int
    weak_topics: list[str] = Field(default_factory=list)
    recommended_review: list[str] = Field(default_factory=list)
    answers: list[QuizAnswerResult] = Field(default_factory=list)
    started_at: datetime
    submitted_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
