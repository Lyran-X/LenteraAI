import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.quiz_schema import QuizAttemptRead, QuizGenerateRequest, QuizRead, QuizSubmitRequest
from app.services.quiz_service import quiz_service


router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.get("/context")
def get_quiz_context(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    return {
        "feature": "quizzes",
        "user_id": str(current_user.id),
        "role": current_user.role,
        "message": "Quiz endpoints scope all data to current_user.id.",
    }


@router.post("/generate", response_model=QuizRead)
def generate_quiz(
    payload: QuizGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizRead:
    return quiz_service.generate_quiz(db=db, current_user=current_user, payload=payload)


@router.get("", response_model=list[QuizRead])
def get_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[QuizRead]:
    return quiz_service.get_quizzes(db=db, current_user=current_user)


@router.get("/attempts/recent", response_model=list[QuizAttemptRead])
def get_recent_attempts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[QuizAttemptRead]:
    return quiz_service.get_recent_attempts(db=db, current_user=current_user)


@router.get("/{quiz_id}", response_model=QuizRead)
def get_quiz(
    quiz_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizRead:
    return quiz_service.get_quiz(db=db, current_user=current_user, quiz_id=quiz_id)


@router.post("/{quiz_id}/submit", response_model=QuizAttemptRead)
def submit_quiz(
    quiz_id: uuid.UUID,
    payload: QuizSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuizAttemptRead:
    return quiz_service.submit_quiz(db=db, current_user=current_user, quiz_id=quiz_id, payload=payload)


@router.get("/{quiz_id}/attempts", response_model=list[QuizAttemptRead])
def get_quiz_attempts(
    quiz_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[QuizAttemptRead]:
    return quiz_service.get_quiz_attempts(db=db, current_user=current_user, quiz_id=quiz_id)