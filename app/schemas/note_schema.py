import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


DB_TO_API_SOURCE_TYPE = {
    "manual": "manual",
    "ai_message": "ai_tutor",
    "document": "document_qa",
    "document_chunk": "document_qa",
    "quiz_review": "quiz",
}


class NoteSourceType(str, Enum):
    AI_TUTOR = "ai_tutor"
    DOCUMENT_QA = "document_qa"
    QUIZ = "quiz"
    MANUAL = "manual"


def public_note_source_type(value: object) -> str:
    source_type = str(value or "manual").strip()
    return DB_TO_API_SOURCE_TYPE.get(source_type, source_type)


def note_source_id_from_value(value: object) -> uuid.UUID | None:
    if isinstance(value, dict):
        for key in (
            "source_id",
            "source_chat_message_id",
            "source_document_id",
            "source_chunk_id",
            "source_quiz_id",
            "source_quiz_attempt_id",
        ):
            if value.get(key):
                return value[key]
        return None

    for attr in (
        "source_chat_message_id",
        "source_document_id",
        "source_chunk_id",
        "source_quiz_id",
        "source_quiz_attempt_id",
    ):
        source_id = getattr(value, attr, None)
        if source_id:
            return source_id
    return None


def normalize_tags(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        value = [value]

    normalized: list[str] = []
    seen: set[str] = set()
    for item in value:
        tag = str(item).strip()
        if not tag:
            continue
        key = tag.lower()
        if key in seen:
            continue
        seen.add(key)
        normalized.append(tag[:48])
    return normalized[:12]


class SavedNoteRead(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    source_type: str
    source_id: uuid.UUID | None = None
    source_chat_message_id: uuid.UUID | None = None
    source_document_id: uuid.UUID | None = None
    source_chunk_id: uuid.UUID | None = None
    source_quiz_id: uuid.UUID | None = None
    source_quiz_attempt_id: uuid.UUID | None = None
    tags: list[str] = Field(default_factory=list)
    is_pinned: bool
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="before")
    @classmethod
    def map_orm_note(cls, value: object) -> object:
        if isinstance(value, dict):
            mapped = dict(value)
            mapped["source_type"] = public_note_source_type(mapped.get("source_type"))
            mapped.setdefault("source_id", note_source_id_from_value(mapped))
            mapped.setdefault("metadata", mapped.get("metadata_") or {})
            mapped["tags"] = normalize_tags(mapped.get("tags"))
            return mapped

        if hasattr(value, "source_type"):
            return {
                "id": getattr(value, "id"),
                "title": getattr(value, "title"),
                "content": getattr(value, "content"),
                "source_type": public_note_source_type(getattr(value, "source_type", "manual")),
                "source_id": note_source_id_from_value(value),
                "source_chat_message_id": getattr(value, "source_chat_message_id", None),
                "source_document_id": getattr(value, "source_document_id", None),
                "source_chunk_id": getattr(value, "source_chunk_id", None),
                "source_quiz_id": getattr(value, "source_quiz_id", None),
                "source_quiz_attempt_id": getattr(value, "source_quiz_attempt_id", None),
                "tags": normalize_tags(getattr(value, "tags", None)),
                "is_pinned": bool(getattr(value, "is_pinned", False)),
                "metadata": getattr(value, "metadata_", None) or {},
                "created_at": getattr(value, "created_at"),
                "updated_at": getattr(value, "updated_at"),
            }
        return value

    model_config = ConfigDict(from_attributes=True)


class SavedNoteCreate(BaseModel):
    title: str = Field(min_length=2, max_length=180)
    content: str = Field(min_length=1)
    source_type: NoteSourceType = NoteSourceType.MANUAL
    source_id: uuid.UUID | None = None
    tags: list[str] = Field(default_factory=list, max_length=12)
    is_pinned: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "content", mode="before")
    @classmethod
    def normalize_text(cls, value: object) -> str:
        return str(value or "").strip()

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_note_tags(cls, value: object) -> list[str]:
        return normalize_tags(value)


class SavedNoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    content: str | None = Field(default=None, min_length=1)
    source_type: NoteSourceType | None = None
    source_id: uuid.UUID | None = None
    tags: list[str] | None = Field(default=None, max_length=12)
    is_pinned: bool | None = None
    metadata: dict[str, Any] | None = None

    @field_validator("title", "content", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        return normalized or None

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_optional_tags(cls, value: object) -> list[str] | None:
        if value is None:
            return None
        return normalize_tags(value)


class SaveMessageNoteRequest(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=180)
    tags: list[str] = Field(default_factory=lambda: ["ai-tutor"], max_length=12)
    is_pinned: bool = False

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_save_message_tags(cls, value: object) -> list[str]:
        return normalize_tags(value) or ["ai-tutor"]


class SavedNoteDeleteResponse(BaseModel):
    message: str
    note_id: uuid.UUID