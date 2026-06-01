from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


class AnalyticsSummary(BaseModel):
    average_score: float
    total_quizzes: int
    total_attempts: int
    active_study_plans: int
    completed_study_plans: int
    study_streak: int
    retention_score: int
    saved_notes_count: int
    ai_tutor_sessions_count: int
    ai_tutor_messages_count: int
    study_plan_progress_average: int


class ScoreTrendPoint(BaseModel):
    date: date
    average_score: float
    attempts: int


class TopicMasteryPoint(BaseModel):
    topic: str
    accuracy: float
    correct: int
    total: int


class WeakTopicPoint(BaseModel):
    topic: str
    accuracy: float
    recommendation: str


class RecentQuizPerformance(BaseModel):
    attempt_id: str
    quiz_id: str
    quiz_title: str
    topic: str | None = None
    difficulty: str | None = None
    score: float
    submitted_at: datetime | None = None


class ActivePlanOverview(BaseModel):
    id: str
    title: str
    status: str
    progress_percentage: int
    total_items: int
    completed_items: int


class StudyPlanOverview(BaseModel):
    average_progress: int
    active_plan: ActivePlanOverview | None = None


class AnalyticsInsight(BaseModel):
    type: Literal["recommendation", "warning", "positive", "info"]
    title: str
    message: str


class DashboardAnalytics(BaseModel):
    summary: AnalyticsSummary
    score_trend: list[ScoreTrendPoint] = Field(default_factory=list)
    topic_mastery: list[TopicMasteryPoint] = Field(default_factory=list)
    weak_topics: list[WeakTopicPoint] = Field(default_factory=list)
    recent_quizzes: list[RecentQuizPerformance] = Field(default_factory=list)
    study_plan_overview: StudyPlanOverview
    insights: list[AnalyticsInsight] = Field(default_factory=list)