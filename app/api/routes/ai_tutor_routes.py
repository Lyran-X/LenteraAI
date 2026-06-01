import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth_schema import MessageResponse
from app.schemas.chat_schema import (
    ChatMessageCreate,
    ChatMessageExchange,
    ChatSessionCreate,
    ChatSessionDetail,
    ChatSessionRead,
    SaveMessageToNoteRequest,
)
from app.schemas.note_schema import SavedNoteRead
from app.services.ai_tutor_service import ai_tutor_service


router = APIRouter(prefix="/ai-tutor", tags=["AI Tutor"])


@router.get("/context")
def get_ai_tutor_context(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    return {
        "feature": "ai-tutor",
        "user_id": str(current_user.id),
        "role": current_user.role,
        "message": "AI Tutor endpoints scope all data to current_user.id.",
    }


@router.post("/sessions", response_model=ChatSessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatSessionRead:
    return ai_tutor_service.create_session(db=db, current_user=current_user, payload=payload)


@router.get("/sessions", response_model=list[ChatSessionRead])
def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ChatSessionRead]:
    return ai_tutor_service.get_sessions(db=db, current_user=current_user)


@router.get("/sessions/{session_id}", response_model=ChatSessionDetail)
def get_session_detail(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatSessionDetail:
    return ai_tutor_service.get_session_detail(db=db, current_user=current_user, session_id=session_id)


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageExchange)
def send_message(
    session_id: uuid.UUID,
    payload: ChatMessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatMessageExchange:
    return ai_tutor_service.send_message(
        db=db,
        current_user=current_user,
        session_id=session_id,
        payload=payload,
    )


@router.post("/messages/{message_id}/save-note", response_model=SavedNoteRead, status_code=status.HTTP_201_CREATED)
def save_message_to_note(
    message_id: uuid.UUID,
    payload: SaveMessageToNoteRequest | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return ai_tutor_service.save_message_to_note(
        db=db,
        current_user=current_user,
        message_id=message_id,
        payload=payload or SaveMessageToNoteRequest(),
    )


@router.delete("/sessions/{session_id}", response_model=MessageResponse)
def delete_session(
    session_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> MessageResponse:
    ai_tutor_service.delete_session(db=db, current_user=current_user, session_id=session_id)
    return MessageResponse(message="AI Tutor session deleted.")