import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import BACKEND_ROOT
from app.core.security import get_password_hash, verify_password
from app.models.chat import AIChatMessage
from app.models.note import SavedNote
from app.models.quiz import Quiz, QuizAttempt
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.user import User
from app.schemas.profile_schema import (
    AISettings,
    AISettingsUpdateRequest,
    ChangePasswordRequest,
    ProfileExportResponse,
    ProfileMessageResponse,
    ProfilePreferences,
    ProfileResponse,
    ProfileUpdateRequest,
)


AVATAR_DIR = BACKEND_ROOT / "uploads" / "avatars"
MAX_AVATAR_BYTES = 2 * 1024 * 1024
ALLOWED_AVATAR_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
}

DEFAULT_PREFERENCES: dict[str, Any] = {
    "preferred_learning_style": "step_by_step",
    "daily_study_duration": "45",
    "preferred_quiz_difficulty": "adaptive",
    "target_subject": None,
    "reminder_time": None,
}

DEFAULT_AI_SETTINGS: dict[str, Any] = {
    "default_tutor_mode": "explain_simply",
    "answer_length": "balanced",
    "citation_required": True,
    "socratic_mode_enabled": False,
}


class ProfileService:
    def get_profile(self, db: Session, user: User) -> ProfileResponse:
        return self._build_profile_response(db=db, user=user)

    def update_profile(self, db: Session, user: User, payload: ProfileUpdateRequest) -> ProfileResponse:
        data = payload.model_dump(exclude_unset=True)
        metadata = self._metadata(user)
        profile = dict(metadata.get("profile") or {})
        preferences = dict(metadata.get("preferences") or {})

        if "name" in data and data["name"] is not None:
            user.name = data["name"].strip()

        if "learning_level" in data:
            profile["learning_level"] = self._clean_optional_string(data["learning_level"])

        preference_fields = {
            "target_subject",
            "preferred_learning_style",
            "daily_study_duration",
            "preferred_quiz_difficulty",
            "reminder_time",
        }
        for field in preference_fields:
            if field not in data:
                continue
            value = data[field]
            if field == "daily_study_duration" and value is not None:
                preferences[field] = str(value).strip()
            else:
                preferences[field] = self._clean_optional_string(value) if isinstance(value, str) or value is None else value

        metadata["profile"] = profile
        metadata["preferences"] = preferences
        user.metadata_ = metadata
        db.add(user)
        db.commit()
        db.refresh(user)
        return self._build_profile_response(db=db, user=user)

    def update_ai_settings(self, db: Session, user: User, payload: AISettingsUpdateRequest) -> ProfileResponse:
        data = payload.model_dump(exclude_unset=True)
        metadata = self._metadata(user)
        ai_settings = dict(metadata.get("ai_settings") or {})
        ai_settings.update({key: value for key, value in data.items() if value is not None})
        metadata["ai_settings"] = ai_settings
        user.metadata_ = metadata
        db.add(user)
        db.commit()
        db.refresh(user)
        return self._build_profile_response(db=db, user=user)

    async def upload_avatar(self, db: Session, user: User, file: UploadFile) -> ProfileResponse:
        content_type = file.content_type or ""
        extension = ALLOWED_AVATAR_TYPES.get(content_type)
        if not extension:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported avatar type. Please upload JPG or PNG.",
            )

        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Avatar file is empty.",
            )
        if len(content) > MAX_AVATAR_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Avatar file is too large. Maximum size is 2 MB.",
            )

        AVATAR_DIR.mkdir(parents=True, exist_ok=True)
        self._delete_avatar_file(user.avatar_url)
        filename = f"{user.id}_{int(time.time())}{extension}"
        avatar_path = AVATAR_DIR / filename
        avatar_path.write_bytes(content)

        user.avatar_url = f"/uploads/avatars/{filename}"
        db.add(user)
        db.commit()
        db.refresh(user)
        return self._build_profile_response(db=db, user=user)

    def delete_avatar(self, db: Session, user: User) -> ProfileResponse:
        self._delete_avatar_file(user.avatar_url)
        user.avatar_url = None
        db.add(user)
        db.commit()
        db.refresh(user)
        return self._build_profile_response(db=db, user=user)

    def change_password(self, db: Session, user: User, payload: ChangePasswordRequest) -> ProfileMessageResponse:
        if not verify_password(payload.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )

        user.hashed_password = get_password_hash(payload.new_password)
        db.add(user)
        db.commit()
        return ProfileMessageResponse(message="Password updated successfully")

    def export_learning_data(self, db: Session, user: User) -> ProfileExportResponse:
        profile = self._build_profile_response(db=db, user=user)
        notes_count = self._count_notes(db=db, user_id=user.id)
        total_quizzes = db.scalar(select(func.count()).select_from(Quiz).where(Quiz.user_id == user.id)) or 0
        completed_quizzes = self._completed_quizzes(db=db, user_id=user.id)
        average_score = db.scalar(
            select(func.avg(QuizAttempt.percentage)).where(
                QuizAttempt.user_id == user.id,
                QuizAttempt.submitted_at.isnot(None),
            )
        )
        total_plans = db.scalar(select(func.count()).select_from(StudyPlan).where(StudyPlan.user_id == user.id)) or 0
        active_plans = db.scalar(
            select(func.count()).select_from(StudyPlan).where(
                StudyPlan.user_id == user.id,
                StudyPlan.status == "active",
            )
        ) or 0
        completed_plans = db.scalar(
            select(func.count()).select_from(StudyPlan).where(
                StudyPlan.user_id == user.id,
                StudyPlan.status == "completed",
            )
        ) or 0

        return ProfileExportResponse(
            profile=profile,
            notes_count=int(notes_count),
            quizzes_summary={
                "total_quizzes": int(total_quizzes),
                "completed_quizzes": int(completed_quizzes),
                "average_score": round(float(average_score or 0), 2),
            },
            study_plans_summary={
                "total_plans": int(total_plans),
                "active_plans": int(active_plans),
                "completed_plans": int(completed_plans),
            },
        )

    def _build_profile_response(self, db: Session, user: User) -> ProfileResponse:
        metadata = self._metadata(user)
        profile = dict(metadata.get("profile") or {})
        preferences = {**DEFAULT_PREFERENCES, **dict(metadata.get("preferences") or {})}
        ai_settings = {**DEFAULT_AI_SETTINGS, **dict(metadata.get("ai_settings") or {})}

        return ProfileResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            avatar_url=user.avatar_url,
            learning_level=profile.get("learning_level"),
            current_streak=self._current_streak(db=db, user_id=user.id),
            completed_quizzes=self._completed_quizzes(db=db, user_id=user.id),
            preferences=ProfilePreferences(**preferences),
            ai_settings=AISettings(**ai_settings),
        )

    def _metadata(self, user: User) -> dict[str, Any]:
        return dict(user.metadata_ or {})

    def _clean_optional_string(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _completed_quizzes(self, db: Session, user_id: Any) -> int:
        return int(
            db.scalar(
                select(func.count()).select_from(QuizAttempt).where(
                    QuizAttempt.user_id == user_id,
                    QuizAttempt.submitted_at.isnot(None),
                )
            )
            or 0
        )

    def _count_notes(self, db: Session, user_id: Any) -> int:
        return int(db.scalar(select(func.count()).select_from(SavedNote).where(SavedNote.user_id == user_id)) or 0)

    def _current_streak(self, db: Session, user_id: Any) -> int:
        activity_dates: set[date] = set()

        quiz_dates = db.scalars(
            select(QuizAttempt.submitted_at).where(
                QuizAttempt.user_id == user_id,
                QuizAttempt.submitted_at.isnot(None),
            )
        ).all()
        item_dates = db.scalars(
            select(StudyPlanItem.completed_at).where(
                StudyPlanItem.user_id == user_id,
                StudyPlanItem.completed_at.isnot(None),
            )
        ).all()
        message_dates = db.scalars(
            select(AIChatMessage.created_at).where(AIChatMessage.user_id == user_id)
        ).all()

        for value in [*quiz_dates, *item_dates, *message_dates]:
            if value:
                activity_dates.add(value.date())

        streak = 0
        cursor = date.today()
        for _ in range(365):
            if cursor not in activity_dates:
                break
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def _delete_avatar_file(self, avatar_url: str | None) -> None:
        if not avatar_url or not avatar_url.startswith("/uploads/avatars/"):
            return
        avatar_path = AVATAR_DIR / Path(avatar_url).name
        try:
            avatar_path.unlink(missing_ok=True)
        except OSError:
            return


profile_service = ProfileService()