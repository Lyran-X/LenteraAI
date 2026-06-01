import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.core.security import get_password_hash
from app.db.database import get_db
from app.models.user import User
from app.schemas.profile_schema import (
    AISettingsUpdateRequest,
    ChangePasswordRequest,
    ProfileExportResponse,
    ProfileMessageResponse,
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.schemas.user import UserCreate, UserRead
from app.services.profile_service import profile_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me/profile", response_model=ProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileResponse:
    return profile_service.get_profile(db=db, user=current_user)


@router.patch("/me/profile", response_model=ProfileResponse)
def update_my_profile(
    payload: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileResponse:
    return profile_service.update_profile(db=db, user=current_user, payload=payload)


@router.patch("/me/ai-settings", response_model=ProfileResponse)
def update_my_ai_settings(
    payload: AISettingsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileResponse:
    return profile_service.update_ai_settings(db=db, user=current_user, payload=payload)


@router.post("/me/avatar", response_model=ProfileResponse)
async def upload_my_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileResponse:
    return await profile_service.upload_avatar(db=db, user=current_user, file=file)


@router.delete("/me/avatar", response_model=ProfileResponse)
def delete_my_avatar(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileResponse:
    return profile_service.delete_avatar(db=db, user=current_user)


@router.patch("/me/password", response_model=ProfileMessageResponse)
def change_my_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileMessageResponse:
    return profile_service.change_password(db=db, user=current_user, payload=payload)


@router.get("/me/export", response_model=ProfileExportResponse)
def export_my_learning_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ProfileExportResponse:
    return profile_service.export_learning_data(db=db, user=current_user)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _current_admin: User = Depends(require_roles("admin")),
) -> User:
    email = payload.email.lower().strip()
    existing_user = db.scalar(select(User).where(func.lower(User.email) == email))

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        hashed_password=get_password_hash(payload.password),
        role=payload.role.value,
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        ) from exc

    db.refresh(user)
    return user


@router.get("", response_model=list[UserRead])
def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    _current_admin: User = Depends(require_roles("admin")),
) -> list[User]:
    statement = select(User).order_by(User.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    _current_admin: User = Depends(require_roles("admin")),
) -> User:
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user