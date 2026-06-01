import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    original_filename: str
    mime_type: str
    file_size_bytes: int
    status: str
    page_count: int | None = None
    word_count: int | None = None
    summary: str | None = None
    chunks_count: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DocumentChunkRead(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    chunk_index: int
    content: str
    token_count: int | None = None
    page_start: int | None = None
    page_end: int | None = None

    model_config = ConfigDict(from_attributes=True)


class DocumentAskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=10)


class DocumentCitation(BaseModel):
    chunk_id: uuid.UUID
    page_start: int | None = None
    page_end: int | None = None
    score: float
    excerpt: str
    vector_id: str | None = None


class DocumentAskResponse(BaseModel):
    document_id: uuid.UUID
    question: str
    answer: str
    citations: list[DocumentCitation]
    used_chunks: int
    model_provider: str
    model_name: str

class DocumentDeleteResponse(BaseModel):
    message: str
    document_id: uuid.UUID

