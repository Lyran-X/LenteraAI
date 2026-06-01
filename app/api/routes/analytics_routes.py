from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.analytics_schema import (
    AnalyticsSummary,
    DashboardAnalytics,
    RecentQuizPerformance,
    ScoreTrendPoint,
    TopicMasteryPoint,
    WeakTopicPoint,
)
from app.services.analytics_service import analytics_service


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/context")
def get_analytics_context(current_user: User = Depends(get_current_active_user)) -> dict[str, str]:
    return {
        "feature": "analytics",
        "user_id": str(current_user.id),
        "role": current_user.role,
        "message": "Analytics endpoints aggregate existing rows scoped to current_user.id.",
    }


@router.get("/summary", response_model=AnalyticsSummary)
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AnalyticsSummary:
    return analytics_service.get_summary(db=db, current_user=current_user)


@router.get("/score-trend", response_model=list[ScoreTrendPoint])
def get_score_trend(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ScoreTrendPoint]:
    return analytics_service.get_score_trend(db=db, current_user=current_user)


@router.get("/topic-mastery", response_model=list[TopicMasteryPoint])
def get_topic_mastery(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[TopicMasteryPoint]:
    return analytics_service.get_topic_mastery(db=db, current_user=current_user)


@router.get("/weak-topics", response_model=list[WeakTopicPoint])
def get_weak_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[WeakTopicPoint]:
    return analytics_service.get_weak_topics(db=db, current_user=current_user)


@router.get("/recent-quizzes", response_model=list[RecentQuizPerformance])
def get_recent_quizzes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[RecentQuizPerformance]:
    return analytics_service.get_recent_quizzes(db=db, current_user=current_user)


@router.get("/dashboard", response_model=DashboardAnalytics)
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DashboardAnalytics:
    return analytics_service.get_dashboard(db=db, current_user=current_user)
