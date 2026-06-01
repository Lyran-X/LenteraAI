import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.note_schema import (
    NoteSourceType,
    SavedNoteCreate,
    SavedNoteDeleteResponse,
    SavedNoteRead,
    SavedNoteUpdate,
)
from app.services.note_service import note_service


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("/context")
def get_notes_context(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    return {
        "feature": "notes",
        "user_id": str(current_user.id),
        "role": current_user.role,
        "message": "Notes CRUD endpoints use user_id from current_user only.",
    }


@router.get("", response_model=list[SavedNoteRead])
def list_notes(
    search: str | None = Query(default=None, min_length=1, max_length=120),
    source_type: NoteSourceType | None = Query(default=None),
    pinned: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[SavedNoteRead]:
    return note_service.list_notes(
        db=db,
        current_user=current_user,
        search=search,
        source_type=source_type,
        pinned=pinned,
        limit=limit,
    )


@router.post("", response_model=SavedNoteRead, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: SavedNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return note_service.create_note(db=db, current_user=current_user, payload=payload)


@router.get("/{note_id}", response_model=SavedNoteRead)
def get_note(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return note_service.get_note(db=db, current_user=current_user, note_id=note_id)


@router.patch("/{note_id}", response_model=SavedNoteRead)
def update_note(
    note_id: uuid.UUID,
    payload: SavedNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return note_service.update_note(db=db, current_user=current_user, note_id=note_id, payload=payload)


@router.delete("/{note_id}", response_model=SavedNoteDeleteResponse)
def delete_note(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteDeleteResponse:
    return note_service.delete_note(db=db, current_user=current_user, note_id=note_id)


@router.patch("/{note_id}/pin", response_model=SavedNoteRead)
def pin_note(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return note_service.pin_note(db=db, current_user=current_user, note_id=note_id)


@router.patch("/{note_id}/unpin", response_model=SavedNoteRead)
def unpin_note(
    note_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> SavedNoteRead:
    return note_service.unpin_note(db=db, current_user=current_user, note_id=note_id)