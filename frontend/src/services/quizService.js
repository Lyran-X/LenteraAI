import api, { HEAVY_REQUEST_TIMEOUT } from './api'

const toSnakeQuestionType = (value) => {
  const normalized = String(value ?? 'multiple_choice').trim().toLowerCase().replace(/[\s/]+/g, '_')
  if (normalized === 'multiple_choice') return 'multiple_choice'
  if (normalized === 'true_false') return 'true_false'
  if (normalized === 'short_answer') return 'short_answer'
  return ['multiple_choice', 'true_false', 'short_answer'].includes(normalized) ? normalized : 'multiple_choice'
}

const normalizeLanguage = (value) => {
  const normalized = String(value ?? 'id').trim().toLowerCase()
  return normalized === 'en' ? 'en' : 'id'
}

const normalizeOptionalText = (value) => {
  if (value === null || value === undefined) return undefined
  const normalized = String(value).trim()
  return normalized || undefined
}

const normalizeGeneratePayload = (payload = {}) => {
  const sourceType = payload.source_type ?? payload.sourceType ?? payload.source ?? 'topic'
  const documentId = payload.document_id ?? payload.documentId ?? payload.source_id ?? payload.sourceId ?? null
  const topic = normalizeOptionalText(payload.topic ?? payload.documentTitle)
  const focusTopic = normalizeOptionalText(payload.focus_topic ?? payload.focusTopic)

  const normalized = {
    source_type: sourceType,
    difficulty: String(payload.difficulty ?? 'medium').toLowerCase(),
    question_type: toSnakeQuestionType(payload.question_type ?? payload.questionType),
    language: normalizeLanguage(payload.language ?? payload.quizLanguage),
    total_questions: Number(payload.total_questions ?? payload.totalQuestions ?? payload.count ?? 5),
  }

  if (topic) normalized.topic = topic
  if (focusTopic) normalized.focus_topic = focusTopic
  if (documentId) {
    normalized.document_id = documentId
    normalized.source_id = documentId
  }

  return normalized
}

const normalizeAnswers = (answers) => {
  if (Array.isArray(answers)) return answers
  if (answers && typeof answers === 'object') {
    return Object.entries(answers).map(([questionId, answer]) => ({
      question_id: questionId,
      user_answer: answer,
    }))
  }
  return []
}

export const generateQuiz = async (payload) => {
  const response = await api.post('/quizzes/generate', normalizeGeneratePayload(payload), { timeout: HEAVY_REQUEST_TIMEOUT })
  return response.data
}

export const getQuizzes = async () => {
  const response = await api.get('/quizzes')
  return response.data
}

export const getQuiz = async (quizId) => {
  const response = await api.get(`/quizzes/${quizId}`)
  return response.data
}

export const submitQuiz = async (quizId, answers) => {
  const payload = Array.isArray(answers?.answers) ? answers : { answers: normalizeAnswers(answers) }
  const response = await api.post(`/quizzes/${quizId}/submit`, payload)
  return response.data
}

export const getRecentAttempts = async () => {
  const response = await api.get('/quizzes/attempts/recent')
  return response.data
}

export const getQuizAttempts = async (quizId) => {
  const response = await api.get(`/quizzes/${quizId}/attempts`)
  return response.data
}

export const getQuizHistory = getRecentAttempts

export default {
  generateQuiz,
  getQuizzes,
  getQuiz,
  submitQuiz,
  getRecentAttempts,
  getQuizAttempts,
}