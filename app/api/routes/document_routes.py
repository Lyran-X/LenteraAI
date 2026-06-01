import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.document import DocumentAskRequest, DocumentAskResponse, DocumentDeleteResponse, DocumentRead
from app.services.document_service import document_service


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document(
    title: str | None = Form(default=None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DocumentRead:
    return await document_service.upload_document(
        db=db,
        user_id=current_user.id,
        file=file,
        title=title,
    )


@router.get("", response_model=list[DocumentRead])
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[DocumentRead]:
    return document_service.get_documents(db=db, user_id=current_user.id)


@router.delete("/{document_id}", response_model=DocumentDeleteResponse)
def delete_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DocumentDeleteResponse:
    return document_service.delete_document(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
    )

@router.post("/{document_id}/ask", response_model=DocumentAskResponse)
def ask_document(
    document_id: uuid.UUID,
    payload: DocumentAskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DocumentAskResponse:
    return document_service.ask_document(
        db=db,
        document_id=document_id,
        user_id=current_user.id,
        question=payload.question,
        top_k=payload.top_k,
    )
