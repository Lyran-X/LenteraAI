import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.note_schema import SavedNoteRead, SaveMessageNoteRequest


class TutorMode(str, Enum):
    EXPLAIN_SIMPLY = "explain_simply"
    STEP_BY_STEP = "step_by_step"
    SOCRATIC = "socratic"
    GIVE_EXAMPLE = "give_example"
    PRACTICE_QUESTION = "practice_question"


class ChatSessionCreate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    tutor_mode: TutorMode = TutorMode.EXPLAIN_SIMPLY


class ChatSessionRead(BaseModel):
    id: uuid.UUID
    title: str
    session_type: str
    model_provider: str | None = None
    model_name: str | None = None
    tutor_mode: TutorMode
    messages_count: int = 0
    last_message_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ChatMessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    tutor_mode: TutorMode | None = None


class ChatMessageRead(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID
    role: str
    content: str
    sequence_number: int
    model_provider: str | None = None
    model_name: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    latency_ms: int | None = None
    citations: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class ChatSessionDetail(ChatSessionRead):
    messages: list[ChatMessageRead] = Field(default_factory=list)


class ChatMessageExchange(BaseModel):
    session: ChatSessionRead
    user_message: ChatMessageRead
    assistant_message: ChatMessageRead


class SaveMessageToNoteRequest(SaveMessageNoteRequest):
    pass


class SaveMessageToNoteResponse(SavedNoteRead):
    pass