from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from statistics import mean

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.chat import AIChatMessage, AIChatSession
from app.models.note import SavedNote
from app.models.quiz import Quiz, QuizAnswer, QuizAttempt, QuizQuestion
from app.models.study_plan import StudyPlan, StudyPlanItem
from app.models.user import User
from app.schemas.analytics_schema import (
    ActivePlanOverview,
    AnalyticsInsight,
    AnalyticsSummary,
    DashboardAnalytics,
    RecentQuizPerformance,
    ScoreTrendPoint,
    StudyPlanOverview,
    TopicMasteryPoint,
    WeakTopicPoint,
)


class AnalyticsService:
    def get_summary(self, db: Session, current_user: User) -> AnalyticsSummary:
        attempts = self._get_attempts(db, current_user)
        quizzes_count = self._count_quizzes(db, current_user)
        plans = self._get_plans(db, current_user)
        saved_notes_count = self._count_saved_notes(db, current_user)
        ai_sessions_count = self._count_ai_sessions(db, current_user)
        ai_messages_count = self._count_ai_messages(db, current_user)
        study_streak = self._study_streak(db, current_user, attempts, plans)
        average_score = self._average_score(attempts)
        progress_average = self._study_plan_progress_average(plans)

        return AnalyticsSummary(
            average_score=average_score,
            total_quizzes=quizzes_count,
            total_attempts=len(attempts),
            active_study_plans=sum(1 for plan in plans if plan.status == "active"),
            completed_study_plans=sum(1 for plan in plans if plan.status == "completed" or self._plan_progress(plan) == 100),
            study_streak=study_streak,
            retention_score=self._retention_score(average_score, study_streak),
            saved_notes_count=saved_notes_count,
            ai_tutor_sessions_count=ai_sessions_count,
            ai_tutor_messages_count=ai_messages_count,
            study_plan_progress_average=progress_average,
        )

    def get_score_trend(self, db: Session, current_user: User) -> list[ScoreTrendPoint]:
        attempts = self._get_attempts(db, current_user)
        grouped_scores: dict[date, list[float]] = defaultdict(list)
        for attempt in attempts:
            activity_date = self._attempt_date(attempt)
            if activity_date:
                grouped_scores[activity_date].append(self._attempt_score(attempt))

        return [
            ScoreTrendPoint(
                date=activity_date,
                average_score=round(mean(scores), 2),
                attempts=len(scores),
            )
            for activity_date, scores in sorted(grouped_scores.items())
        ]

    def get_topic_mastery(self, db: Session, current_user: User) -> list[TopicMasteryPoint]:
        stats = self._topic_stats(db, current_user)
        return [
            TopicMasteryPoint(
                topic=topic,
                accuracy=round((values["correct"] / values["total"]) * 100, 2) if values["total"] else 0,
                correct=values["correct"],
                total=values["total"],
            )
            for topic, values in sorted(stats.items(), key=lambda item: item[0].lower())
        ]

    def get_weak_topics(self, db: Session, current_user: User) -> list[WeakTopicPoint]:
        mastery = self.get_topic_mastery(db, current_user)
        weak_topics = {
            item.topic: item.accuracy
            for item in mastery
            if item.accuracy < 70
        }

        for attempt in self._get_attempts(db, current_user):
            for topic in attempt.weak_topics or []:
                weak_topics.setdefault(topic, 0)
            metadata = attempt.metadata_ or {}
            for topic in metadata.get("weak_topics", []) if isinstance(metadata.get("weak_topics"), list) else []:
                weak_topics.setdefault(str(topic), 0)

        return [
            WeakTopicPoint(
                topic=topic,
                accuracy=round(accuracy, 2),
                recommendation=f"Review {topic} with AI Tutor and retry a focused quiz.",
            )
            for topic, accuracy in sorted(weak_topics.items(), key=lambda item: item[1])
        ]

    def get_recent_quizzes(self, db: Session, current_user: User, limit: int = 10) -> list[RecentQuizPerformance]:
        attempts = db.scalars(
            select(QuizAttempt)
            .options(selectinload(QuizAttempt.quiz))
            .where(QuizAttempt.user_id == current_user.id)
            .order_by(QuizAttempt.created_at.desc())
            .limit(limit)
        ).all()
        return [self._to_recent_quiz(attempt) for attempt in attempts]

    def get_dashboard(self, db: Session, current_user: User) -> DashboardAnalytics:
        summary = self.get_summary(db, current_user)
        score_trend = self.get_score_trend(db, current_user)
        topic_mastery = self.get_topic_mastery(db, current_user)
        weak_topics = self.get_weak_topics(db, current_user)
        recent_quizzes = self.get_recent_quizzes(db, current_user, limit=5)
        plans = self._get_plans(db, current_user)
        study_plan_overview = self._study_plan_overview(plans)
        insights = self._build_insights(summary, weak_topics)

        return DashboardAnalytics(
            summary=summary,
            score_trend=score_trend,
            topic_mastery=topic_mastery,
            weak_topics=weak_topics,
            recent_quizzes=recent_quizzes,
            study_plan_overview=study_plan_overview,
            insights=insights,
        )

    def _count_quizzes(self, db: Session, current_user: User) -> int:
        return int(db.scalar(select(func.count(Quiz.id)).where(Quiz.user_id == current_user.id)) or 0)

    def _count_saved_notes(self, db: Session, current_user: User) -> int:
        return int(db.scalar(select(func.count(SavedNote.id)).where(SavedNote.user_id == current_user.id)) or 0)

    def _count_ai_sessions(self, db: Session, current_user: User) -> int:
        return int(db.scalar(select(func.count(AIChatSession.id)).where(AIChatSession.user_id == current_user.id)) or 0)

    def _count_ai_messages(self, db: Session, current_user: User) -> int:
        return int(db.scalar(select(func.count(AIChatMessage.id)).where(AIChatMessage.user_id == current_user.id)) or 0)

    def _get_attempts(self, db: Session, current_user: User) -> list[QuizAttempt]:
        return list(
            db.scalars(
                select(QuizAttempt)
                .options(selectinload(QuizAttempt.quiz), selectinload(QuizAttempt.answers).selectinload(QuizAnswer.question))
                .where(QuizAttempt.user_id == current_user.id)
                .order_by(QuizAttempt.created_at.desc())
            ).all()
        )

    def _get_plans(self, db: Session, current_user: User) -> list[StudyPlan]:
        return list(
            db.scalars(
                select(StudyPlan)
                .options(selectinload(StudyPlan.items))
                .where(StudyPlan.user_id == current_user.id)
                .order_by(StudyPlan.created_at.desc())
            ).all()
        )

    def _topic_stats(self, db: Session, current_user: User) -> dict[str, dict[str, int]]:
        attempts = self._get_attempts(db, current_user)
        stats: dict[str, dict[str, int]] = defaultdict(lambda: {"correct": 0, "total": 0})
        for attempt in attempts:
            for answer in attempt.answers or []:
                question = answer.question
                if not question:
                    continue
                topic = self._question_topic(question, attempt.quiz)
                stats[topic]["total"] += 1
                if answer.is_correct:
                    stats[topic]["correct"] += 1
        return stats

    def _question_topic(self, question: QuizQuestion, quiz: Quiz | None = None) -> str:
        metadata = question.metadata_ or {}
        return str(question.topic or metadata.get("topic") or (quiz.topic if quiz else None) or "General").strip()

    def _average_score(self, attempts: list[QuizAttempt]) -> float:
        if not attempts:
            return 0
        return round(mean(self._attempt_score(attempt) for attempt in attempts), 2)

    def _attempt_score(self, attempt: QuizAttempt) -> float:
        value = attempt.percentage if attempt.percentage is not None else attempt.score
        return float(value or 0)

    def _attempt_date(self, attempt: QuizAttempt) -> date | None:
        timestamp = attempt.submitted_at or attempt.created_at or attempt.started_at
        return timestamp.date() if timestamp else None

    def _to_recent_quiz(self, attempt: QuizAttempt) -> RecentQuizPerformance:
        quiz = attempt.quiz
        return RecentQuizPerformance(
            attempt_id=str(attempt.id),
            quiz_id=str(attempt.quiz_id),
            quiz_title=quiz.title if quiz else "Quiz",
            topic=quiz.topic if quiz else None,
            difficulty=(quiz.metadata_ or {}).get("requested_difficulty") or quiz.difficulty if quiz else None,
            score=self._attempt_score(attempt),
            submitted_at=attempt.submitted_at or attempt.created_at,
        )

    def _study_plan_overview(self, plans: list[StudyPlan]) -> StudyPlanOverview:
        active_plan = next((plan for plan in plans if plan.status == "active"), None)
        return StudyPlanOverview(
            average_progress=self._study_plan_progress_average(plans),
            active_plan=self._to_active_plan(active_plan) if active_plan else None,
        )

    def _to_active_plan(self, plan: StudyPlan) -> ActivePlanOverview:
        total_items = len(plan.items or [])
        completed_items = sum(1 for item in plan.items or [] if item.status == "done")
        return ActivePlanOverview(
            id=str(plan.id),
            title=plan.title,
            status=plan.status,
            progress_percentage=self._plan_progress(plan),
            total_items=total_items,
            completed_items=completed_items,
        )

    def _study_plan_progress_average(self, plans: list[StudyPlan]) -> int:
        relevant_plans = [plan for plan in plans if plan.status in {"active", "completed"}]
        if not relevant_plans:
            return 0
        return round(mean(self._plan_progress(plan) for plan in relevant_plans))

    def _plan_progress(self, plan: StudyPlan) -> int:
        items = plan.items or []
        if not items:
            return 0
        completed_items = sum(1 for item in items if item.status == "done")
        return round((completed_items / len(items)) * 100)

    def _study_streak(
        self,
        db: Session,
        current_user: User,
        attempts: list[QuizAttempt],
        plans: list[StudyPlan],
    ) -> int:
        activity_dates: set[date] = set()
        for attempt in attempts:
            activity_date = self._attempt_date(attempt)
            if activity_date:
                activity_dates.add(activity_date)

        for plan in plans:
            for item in plan.items or []:
                if item.completed_at:
                    activity_dates.add(item.completed_at.date())

        session_dates = db.scalars(
            select(AIChatSession.created_at).where(AIChatSession.user_id == current_user.id)
        ).all()
        for timestamp in session_dates:
            if timestamp:
                activity_dates.add(timestamp.date())

        message_dates = db.scalars(
            select(AIChatMessage.created_at).where(AIChatMessage.user_id == current_user.id)
        ).all()
        for timestamp in message_dates:
            if timestamp:
                activity_dates.add(timestamp.date())

        today = datetime.now(UTC).date()
        streak = 0
        cursor = today
        while cursor in activity_dates:
            streak += 1
            cursor -= timedelta(days=1)
        return streak

    def _retention_score(self, average_score: float, study_streak: int) -> int:
        if average_score <= 0 and study_streak <= 0:
            return 0
        return round((average_score * 0.6) + ((min(study_streak, 7) / 7) * 100 * 0.4))

    def _build_insights(self, summary: AnalyticsSummary, weak_topics: list[WeakTopicPoint]) -> list[AnalyticsInsight]:
        insights: list[AnalyticsInsight] = []
        if summary.total_attempts == 0:
            insights.append(
                AnalyticsInsight(
                    type="recommendation",
                    title="Generate your first quiz",
                    message="Start with a short quiz so EduPath can measure your current understanding.",
                )
            )
            return insights

        if summary.average_score < 70:
            topic = weak_topics[0].topic if weak_topics else "your weakest topics"
            insights.append(
                AnalyticsInsight(
                    type="recommendation",
                    title="Review weak topics",
                    message=f"Your average quiz score is below 70. Review {topic} with AI Tutor and retry a focused quiz.",
                )
            )

        if summary.study_streak == 0:
            insights.append(
                AnalyticsInsight(
                    type="info",
                    title="Restart your study streak",
                    message="Complete one study task or submit a quiz today to restart your learning streak.",
                )
            )

        if not weak_topics and summary.average_score >= 80:
            insights.append(
                AnalyticsInsight(
                    type="positive",
                    title="Strong performance",
                    message="Your quiz performance is strong. Keep challenging yourself with harder adaptive quizzes.",
                )
            )

        if not insights:
            insights.append(
                AnalyticsInsight(
                    type="recommendation",
                    title="Keep the rhythm",
                    message="Continue alternating concept review, short quizzes, and saved notes for steady progress.",
                )
            )
        return insights


analytics_service = AnalyticsService()