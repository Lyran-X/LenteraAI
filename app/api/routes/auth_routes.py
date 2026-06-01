from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user, require_roles
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth_schema import AccessTokenResponse, LoginRequest, MessageResponse, RegisterRequest, TokenResponse
from app.schemas.user_schema import UserPublic, UserRole


router = APIRouter(prefix="/auth", tags=["Auth"])
protected_router = APIRouter(prefix="/protected", tags=["Protected"])


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.lower().strip()
    return db.scalar(select(User).where(func.lower(User.email) == normalized_email))


def create_user_access_token(user: User) -> str:
    return create_access_token(
        subject=str(user.id),
        extra_claims={"role": user.role},
    )


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account.",
        )

    return user


def build_access_token_response(user: User) -> AccessTokenResponse:
    return AccessTokenResponse(access_token=create_user_access_token(user))


def build_token_response(user: User) -> TokenResponse:
    return TokenResponse(access_token=create_user_access_token(user), user=user)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    email = payload.email.lower().strip()
    role = payload.role.value

    if role == UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin accounts must be created by an existing administrator.",
        )

    if get_user_by_email(db, email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        )

    user = User(
        name=payload.name.strip(),
        email=email,
        hashed_password=get_password_hash(payload.password),
        role=role,
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
    return build_token_response(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = authenticate_user(db, payload.email, payload.password)
    return build_token_response(user)


@router.post("/token", response_model=AccessTokenResponse)
def swagger_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    user = authenticate_user(db, form_data.username, form_data.password)
    return build_access_token_response(user)


@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_active_user)) -> User:
    return current_user


@router.post("/logout", response_model=MessageResponse)
def logout() -> MessageResponse:
    return MessageResponse(message="Logout is handled on the frontend by removing the access token.")


@protected_router.get("/student", response_model=MessageResponse)
def student_area(
    current_user: User = Depends(require_roles("student", "teacher", "admin")),
) -> MessageResponse:
    return MessageResponse(message=f"Hello {current_user.name}, you can access the student area.")


@protected_router.get("/admin", response_model=MessageResponse)
def admin_area(current_user: User = Depends(require_roles("admin"))) -> MessageResponse:
    return MessageResponse(message=f"Hello {current_user.name}, you can access the admin area.")