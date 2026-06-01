import uuid
from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.chat import AIChatMessage, AIChatSession
from app.models.note import SavedNote
from app.models.user import User
from app.schemas.chat_schema import (
    ChatMessageCreate,
    ChatMessageExchange,
    ChatMessageRead,
    ChatSessionCreate,
    ChatSessionDetail,
    ChatSessionRead,
    SaveMessageToNoteRequest,
    TutorMode,
)
from app.schemas.note_schema import SavedNoteRead
from app.services.llm_service import LLMMessage, build_tutor_system_prompt, llm_service


class AITutorService:
    def create_session(self, db: Session, current_user: User, payload: ChatSessionCreate) -> ChatSessionRead:
        tutor_mode = payload.tutor_mode
        session = AIChatSession(
            user_id=current_user.id,
            title=(payload.title or "New Chat").strip(),
            session_type="general_tutor",
            model_provider=None,
            model_name=None,
            system_prompt=build_tutor_system_prompt(tutor_mode),
            metadata_={"tutor_mode": tutor_mode.value},
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return self._to_session_read(db, session)

    def get_sessions(self, db: Session, current_user: User) -> list[ChatSessionRead]:
        sessions = db.scalars(
            select(AIChatSession)
            .where(AIChatSession.user_id == current_user.id)
            .order_by(AIChatSession.last_message_at.desc().nullslast(), AIChatSession.created_at.desc())
        ).all()
        return [self._to_session_read(db, session) for session in sessions]

    def get_session_detail(self, db: Session, current_user: User, session_id: uuid.UUID) -> ChatSessionDetail:
        session = self._get_user_session(db, current_user, session_id)
        messages = self._get_session_messages(db, session.id)
        session_read = self._to_session_read(db, session)
        return ChatSessionDetail(**session_read.model_dump(), messages=[self._to_message_read(message) for message in messages])

    def send_message(
        self,
        db: Session,
        current_user: User,
        session_id: uuid.UUID,
        payload: ChatMessageCreate,
    ) -> ChatMessageExchange:
        session = self._get_user_session(db, current_user, session_id)
        tutor_mode = payload.tutor_mode or self._session_tutor_mode(session)
        existing_messages = self._get_session_messages(db, session.id)
        next_sequence = self._next_sequence_number(db, session.id)
        now = datetime.now(UTC)

        user_message = AIChatMessage(
            session_id=session.id,
            user_id=current_user.id,
            sequence_number=next_sequence,
            role="user",
            content=payload.content.strip(),
            citations=[],
            metadata_={"tutor_mode": tutor_mode.value},
        )
        db.add(user_message)
        db.flush()

        socratic_assistant_turn_count = self._socratic_assistant_turn_count(existing_messages) if tutor_mode == TutorMode.SOCRATIC else 0
        llm_result = llm_service.generate_tutor_response(
            tutor_mode=tutor_mode,
            user_message=user_message.content,
            history=[
                LLMMessage(role=message.role, content=message.content)
                for message in existing_messages
                if message.role in {"user", "assistant"}
            ],
            socratic_assistant_turn_count=socratic_assistant_turn_count,
        )

        assistant_message = AIChatMessage(
            session_id=session.id,
            user_id=current_user.id,
            sequence_number=next_sequence + 1,
            role="assistant",
            content=llm_result.content,
            model_provider=llm_result.provider,
            model_name=llm_result.model,
            prompt_tokens=llm_result.prompt_tokens,
            completion_tokens=llm_result.completion_tokens,
            total_tokens=llm_result.total_tokens,
            latency_ms=llm_result.latency_ms,
            citations=[],
            metadata_={"tutor_mode": tutor_mode.value, "socratic_assistant_turn_count": socratic_assistant_turn_count + 1 if tutor_mode == TutorMode.SOCRATIC else None, **llm_result.metadata},
        )
        db.add(assistant_message)

        session.last_message_at = now
        session.model_provider = llm_result.provider
        session.model_name = llm_result.model
        session.system_prompt = build_tutor_system_prompt(tutor_mode, socratic_assistant_turn_count + 1 if tutor_mode == TutorMode.SOCRATIC else 0)
        session.metadata_ = {**(session.metadata_ or {}), "tutor_mode": tutor_mode.value}
        if session.title == "New Chat":
            session.title = self._title_from_message(user_message.content)

        db.commit()
        db.refresh(session)
        db.refresh(user_message)
        db.refresh(assistant_message)

        return ChatMessageExchange(
            session=self._to_session_read(db, session),
            user_message=self._to_message_read(user_message),
            assistant_message=self._to_message_read(assistant_message),
        )

    def save_message_to_note(
        self,
        db: Session,
        current_user: User,
        message_id: uuid.UUID,
        payload: SaveMessageToNoteRequest,
    ) -> SavedNoteRead:
        message = db.scalar(
            select(AIChatMessage).where(
                AIChatMessage.id == message_id,
                AIChatMessage.user_id == current_user.id,
            )
        )
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found.",
            )

        if message.role != "assistant":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only AI tutor answers can be saved as notes.",
            )

        session = self._get_user_session(db, current_user, message.session_id)
        note = SavedNote(
            user_id=current_user.id,
            title=(payload.title or f"AI Tutor Note - {session.title}").strip(),
            content=message.content,
            source_type="ai_message",
            source_chat_message_id=message.id,
            tags=payload.tags or ["ai-tutor"],
            is_pinned=payload.is_pinned,
            metadata_={"session_id": str(session.id), "message_id": str(message.id)},
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        return SavedNoteRead.model_validate(note)

    def delete_session(self, db: Session, current_user: User, session_id: uuid.UUID) -> None:
        session = self._get_user_session(db, current_user, session_id)
        db.delete(session)
        db.commit()

    def _get_user_session(self, db: Session, current_user: User, session_id: uuid.UUID) -> AIChatSession:
        session = db.scalar(
            select(AIChatSession).where(
                AIChatSession.id == session_id,
                AIChatSession.user_id == current_user.id,
            )
        )
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI Tutor session not found.",
            )
        return session

    def _get_session_messages(self, db: Session, session_id: uuid.UUID) -> list[AIChatMessage]:
        return list(
            db.scalars(
                select(AIChatMessage)
                .where(AIChatMessage.session_id == session_id)
                .order_by(AIChatMessage.sequence_number.asc(), AIChatMessage.created_at.asc())
            ).all()
        )

    def _socratic_assistant_turn_count(self, messages: list[AIChatMessage]) -> int:
        return sum(
            1
            for message in messages
            if message.role == "assistant"
            and (message.metadata_ or {}).get("tutor_mode") == TutorMode.SOCRATIC.value
        )

    def _next_sequence_number(self, db: Session, session_id: uuid.UUID) -> int:
        max_sequence = db.scalar(
            select(func.max(AIChatMessage.sequence_number)).where(AIChatMessage.session_id == session_id)
        )
        return int(max_sequence if max_sequence is not None else -1) + 1

    def _messages_count(self, db: Session, session_id: uuid.UUID) -> int:
        count = db.scalar(select(func.count(AIChatMessage.id)).where(AIChatMessage.session_id == session_id))
        return int(count or 0)

    def _session_tutor_mode(self, session: AIChatSession) -> TutorMode:
        raw_mode = (session.metadata_ or {}).get("tutor_mode", TutorMode.EXPLAIN_SIMPLY.value)
        try:
            return TutorMode(raw_mode)
        except ValueError:
            return TutorMode.EXPLAIN_SIMPLY

    def _to_session_read(self, db: Session, session: AIChatSession) -> ChatSessionRead:
        return ChatSessionRead(
            id=session.id,
            title=session.title,
            session_type=session.session_type,
            model_provider=session.model_provider,
            model_name=session.model_name,
            tutor_mode=self._session_tutor_mode(session),
            messages_count=self._messages_count(db, session.id),
            last_message_at=session.last_message_at,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def _to_message_read(self, message: AIChatMessage) -> ChatMessageRead:
        return ChatMessageRead(
            id=message.id,
            session_id=message.session_id,
            role=message.role,
            content=message.content,
            sequence_number=message.sequence_number,
            model_provider=message.model_provider,
            model_name=message.model_name,
            prompt_tokens=message.prompt_tokens,
            completion_tokens=message.completion_tokens,
            total_tokens=message.total_tokens,
            latency_ms=message.latency_ms,
            citations=message.citations or [],
            created_at=message.created_at,
            updated_at=message.updated_at,
        )

    def _title_from_message(self, content: str) -> str:
        words = content.strip().split()
        title = " ".join(words[:8])
        if len(words) > 8:
            title = f"{title}..."
        return title or "New Chat"


ai_tutor_service = AITutorService()




