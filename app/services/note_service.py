import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.chat import AIChatMessage
from app.models.document import DocumentChunk, UploadedDocument
from app.models.note import SavedNote
from app.models.quiz import Quiz, QuizAttempt
from app.models.user import User
from app.schemas.note_schema import (
    NoteSourceType,
    SavedNoteCreate,
    SavedNoteDeleteResponse,
    SavedNoteRead,
    SavedNoteUpdate,
    note_source_id_from_value,
    public_note_source_type,
)


API_TO_DB_SOURCE_TYPE = {
    NoteSourceType.MANUAL.value: "manual",
    NoteSourceType.AI_TUTOR.value: "ai_message",
    NoteSourceType.DOCUMENT_QA.value: "document",
    NoteSourceType.QUIZ.value: "quiz_review",
}

FILTER_SOURCE_TYPES = {
    NoteSourceType.MANUAL.value: ["manual"],
    NoteSourceType.AI_TUTOR.value: ["ai_message"],
    NoteSourceType.DOCUMENT_QA.value: ["document", "document_chunk"],
    NoteSourceType.QUIZ.value: ["quiz_review"],
}


class NoteService:
    def list_notes(
        self,
        db: Session,
        current_user: User,
        *,
        search: str | None = None,
        source_type: NoteSourceType | None = None,
        pinned: bool | None = None,
        limit: int = 50,
    ) -> list[SavedNoteRead]:
        statement = select(SavedNote).where(SavedNote.user_id == current_user.id)

        if source_type is not None:
            statement = statement.where(SavedNote.source_type.in_(FILTER_SOURCE_TYPES[source_type.value]))

        if pinned is not None:
            statement = statement.where(SavedNote.is_pinned == pinned)

        if search:
            normalized_search = search.strip()
            if normalized_search:
                pattern = f"%{normalized_search}%"
                statement = statement.where(
                    or_(
                        SavedNote.title.ilike(pattern),
                        SavedNote.content.ilike(pattern),
                        func.array_to_string(SavedNote.tags, " ").ilike(pattern),
                    )
                )

        notes = db.scalars(
            statement.order_by(SavedNote.is_pinned.desc(), SavedNote.created_at.desc()).limit(limit)
        ).all()
        return [SavedNoteRead.model_validate(note) for note in notes]

    def get_note(self, db: Session, current_user: User, note_id: uuid.UUID) -> SavedNoteRead:
        return SavedNoteRead.model_validate(self._get_user_note(db, current_user, note_id))

    def create_note(self, db: Session, current_user: User, payload: SavedNoteCreate) -> SavedNoteRead:
        source_type = payload.source_type.value
        note = SavedNote(
            user_id=current_user.id,
            title=payload.title,
            content=payload.content,
            tags=payload.tags,
            is_pinned=payload.is_pinned,
            metadata_=self._build_metadata(payload.metadata, source_type, payload.source_id),
        )
        self._apply_source(db, current_user, note, source_type, payload.source_id)

        db.add(note)
        db.commit()
        db.refresh(note)
        return SavedNoteRead.model_validate(note)

    def update_note(self, db: Session, current_user: User, note_id: uuid.UUID, payload: SavedNoteUpdate) -> SavedNoteRead:
        note = self._get_user_note(db, current_user, note_id)
        data = payload.model_dump(exclude_unset=True)

        if "title" in data and data["title"] is not None:
            note.title = data["title"]
        if "content" in data and data["content"] is not None:
            note.content = data["content"]
        if "tags" in data and data["tags"] is not None:
            note.tags = data["tags"]
        if "is_pinned" in data and data["is_pinned"] is not None:
            note.is_pinned = bool(data["is_pinned"])
        if "metadata" in data and data["metadata"] is not None:
            note.metadata_ = self._build_metadata(data["metadata"], public_note_source_type(note.source_type), self._current_source_id(note))

        if "source_type" in data or "source_id" in data:
            raw_source_type = data.get("source_type") or public_note_source_type(note.source_type)
            source_type = raw_source_type.value if isinstance(raw_source_type, NoteSourceType) else str(raw_source_type)
            source_id = data.get("source_id") if "source_id" in data else None
            if "source_id" not in data and "source_type" not in data:
                source_id = self._current_source_id(note)
            self._apply_source(db, current_user, note, source_type, source_id)
            note.metadata_ = self._build_metadata(note.metadata_, source_type, source_id)

        db.commit()
        db.refresh(note)
        return SavedNoteRead.model_validate(note)

    def delete_note(self, db: Session, current_user: User, note_id: uuid.UUID) -> SavedNoteDeleteResponse:
        note = self._get_user_note(db, current_user, note_id)
        db.delete(note)
        db.commit()
        return SavedNoteDeleteResponse(message="Note deleted successfully", note_id=note_id)

    def pin_note(self, db: Session, current_user: User, note_id: uuid.UUID) -> SavedNoteRead:
        return self._set_pinned(db, current_user, note_id, True)

    def unpin_note(self, db: Session, current_user: User, note_id: uuid.UUID) -> SavedNoteRead:
        return self._set_pinned(db, current_user, note_id, False)

    def _set_pinned(self, db: Session, current_user: User, note_id: uuid.UUID, is_pinned: bool) -> SavedNoteRead:
        note = self._get_user_note(db, current_user, note_id)
        note.is_pinned = is_pinned
        db.commit()
        db.refresh(note)
        return SavedNoteRead.model_validate(note)

    def _get_user_note(self, db: Session, current_user: User, note_id: uuid.UUID) -> SavedNote:
        note = db.scalar(select(SavedNote).where(SavedNote.id == note_id, SavedNote.user_id == current_user.id))
        if not note:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")
        return note

    def _apply_source(
        self,
        db: Session,
        current_user: User,
        note: SavedNote,
        source_type: str,
        source_id: uuid.UUID | None,
    ) -> None:
        normalized_source_type = source_type if source_type in API_TO_DB_SOURCE_TYPE else NoteSourceType.MANUAL.value
        note.source_type = API_TO_DB_SOURCE_TYPE[normalized_source_type]
        self._clear_source_fields(note)

        if not source_id:
            return

        if normalized_source_type == NoteSourceType.AI_TUTOR.value:
            message = db.scalar(
                select(AIChatMessage).where(AIChatMessage.id == source_id, AIChatMessage.user_id == current_user.id)
            )
            if not message:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="AI Tutor message source not found.")
            note.source_chat_message_id = message.id
            return

        if normalized_source_type == NoteSourceType.DOCUMENT_QA.value:
            document = db.scalar(
                select(UploadedDocument).where(UploadedDocument.id == source_id, UploadedDocument.user_id == current_user.id)
            )
            if document:
                note.source_type = "document"
                note.source_document_id = document.id
                return

            chunk = db.scalar(
                select(DocumentChunk).where(DocumentChunk.id == source_id, DocumentChunk.user_id == current_user.id)
            )
            if chunk:
                note.source_type = "document_chunk"
                note.source_document_id = chunk.document_id
                note.source_chunk_id = chunk.id
                return

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document source not found.")

        if normalized_source_type == NoteSourceType.QUIZ.value:
            quiz = db.scalar(select(Quiz).where(Quiz.id == source_id, Quiz.user_id == current_user.id))
            if quiz:
                note.source_quiz_id = quiz.id
                return

            attempt = db.scalar(select(QuizAttempt).where(QuizAttempt.id == source_id, QuizAttempt.user_id == current_user.id))
            if attempt:
                note.source_quiz_id = attempt.quiz_id
                note.source_quiz_attempt_id = attempt.id
                return

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz source not found.")

    def _clear_source_fields(self, note: SavedNote) -> None:
        note.source_chat_message_id = None
        note.source_document_id = None
        note.source_chunk_id = None
        note.source_quiz_id = None
        note.source_quiz_attempt_id = None

    def _current_source_id(self, note: SavedNote) -> uuid.UUID | None:
        return note_source_id_from_value(note)

    def _build_metadata(self, metadata: dict[str, Any] | None, source_type: str, source_id: uuid.UUID | None) -> dict[str, Any]:
        normalized: dict[str, Any] = dict(metadata or {})
        normalized["api_source_type"] = source_type
        if source_id:
            normalized["source_id"] = str(source_id)
        else:
            normalized.pop("source_id", None)
        return normalized


note_service = NoteService()