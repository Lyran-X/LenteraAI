import api from './api'

const toPercentText = (value) => `${Math.round(Number(value ?? 0))}%`

const toLegacySummary = (summary = {}) => ({
  ...summary,
  averageScore: summary.averageScore ?? toPercentText(summary.average_score),
  studyTime: summary.studyTime ?? `${summary.study_streak ?? 0}d streak`,
  completedPlans: summary.completedPlans ?? summary.completed_study_plans ?? 0,
  retentionScore: summary.retentionScore ?? toPercentText(summary.retention_score),
})

export const getSummary = async () => {
  const response = await api.get('/analytics/summary')
  return response.data
}

export const getScoreTrend = async () => {
  const response = await api.get('/analytics/score-trend')
  return response.data
}

export const getTopicMastery = async () => {
  const response = await api.get('/analytics/topic-mastery')
  return response.data
}

export const getWeakTopics = async () => {
  const response = await api.get('/analytics/weak-topics')
  return response.data
}

export const getRecentQuizzes = async () => {
  const response = await api.get('/analytics/recent-quizzes')
  return response.data
}

export const getDashboardAnalytics = async () => {
  const response = await api.get('/analytics/dashboard')
  return response.data
}

export const getAnalyticsSummary = async () => toLegacySummary(await getSummary())

export default {
  getSummary,
  getScoreTrend,
  getTopicMastery,
  getWeakTopics,
  getRecentQuizzes,
  getDashboardAnalytics,
  getAnalyticsSummary,
}

