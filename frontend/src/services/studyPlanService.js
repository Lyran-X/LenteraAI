import api, { HEAVY_REQUEST_TIMEOUT, isNotFoundError } from './api'

const splitWeakTopics = (value) => {
  if (Array.isArray(value)) return value.filter(Boolean).map((topic) => String(topic).trim()).filter(Boolean)
  if (typeof value === 'string') return value.split(',').map((topic) => topic.trim()).filter(Boolean)
  return []
}

const toMinutes = (value) => {
  if (typeof value === 'number') return value
  if (typeof value === 'string') {
    const match = value.match(/\d+/)
    return match ? Number(match[0]) : 45
  }
  return 45
}

const normalizeGeneratePayload = (payload = {}) => ({
  learning_goal: payload.learning_goal ?? payload.learningGoal ?? payload.goal ?? '',
  subject: payload.subject ?? payload.course ?? 'General Study',
  topic: payload.topic ?? 'Core Topic',
  deadline_date: payload.deadline_date ?? payload.deadlineDate ?? payload.deadline ?? null,
  study_duration_per_day: toMinutes(payload.study_duration_per_day ?? payload.studyDurationPerDay ?? payload.duration),
  understanding_level: payload.understanding_level ?? payload.understandingLevel ?? payload.level ?? 'beginner',
  preferred_learning_style: payload.preferred_learning_style ?? payload.preferredLearningStyle ?? payload.learningStyle ?? 'step_by_step',
  weak_topics: splitWeakTopics(payload.weak_topics ?? payload.weakTopics),
})

export const generateStudyPlan = async (payload) => {
  const response = await api.post('/study-plans/generate', normalizeGeneratePayload(payload), { timeout: HEAVY_REQUEST_TIMEOUT })
  return response.data
}

export const getStudyPlans = async () => {
  const response = await api.get('/study-plans')
  return response.data
}

export const getActiveStudyPlan = async () => {
  try {
    const response = await api.get('/study-plans/active')
    return response.data
  } catch (error) {
    if (isNotFoundError(error)) return null
    throw error
  }
}

export const getStudyPlan = async (planId) => {
  const response = await api.get(`/study-plans/${planId}`)
  return response.data
}

export const completeItem = async (itemId) => {
  const response = await api.patch(`/study-plans/items/${itemId}/complete`)
  return response.data
}

export const uncompleteItem = async (itemId) => {
  const response = await api.patch(`/study-plans/items/${itemId}/uncomplete`)
  return response.data
}
export const updateStudyPlanItem = async (itemId, payload) => {
  const response = await api.patch(`/study-plans/items/${itemId}`, payload)
  return response.data
}

export const deleteStudyPlanItem = async (itemId) => {
  const response = await api.delete(`/study-plans/items/${itemId}`)
  return response.data
}

export const deleteStudyPlan = async (planId) => {
  const response = await api.delete(`/study-plans/${planId}`)
  return response.data
}

export const deletePlan = deleteStudyPlan
export const createStudyPlan = generateStudyPlan
export const completeStudyPlanItem = (itemId, completed = true) => (completed ? completeItem(itemId) : uncompleteItem(itemId))

export default {
  generateStudyPlan,
  getStudyPlans,
  getActiveStudyPlan,
  getStudyPlan,
  completeItem,
  uncompleteItem,
  updateStudyPlanItem,
  deleteStudyPlanItem,
  deleteStudyPlan,
  deletePlan,
}

