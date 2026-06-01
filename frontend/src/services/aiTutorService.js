import api from './api'

const isDev = import.meta.env.DEV

const debugLog = (...args) => {
  if (isDev) console.log(...args)
}

const debugError = (...args) => {
  if (isDev) console.error(...args)
}

export const aiTutorService = {
  async createSession(payload = {}) {
    const response = await api.post('/ai-tutor/sessions', payload)
    return response.data
  },

  async getSessions() {
    const response = await api.get('/ai-tutor/sessions')
    return response.data
  },

  async getSession(sessionId) {
    const response = await api.get(`/ai-tutor/sessions/${sessionId}`)
    return response.data
  },

  async sendMessage(sessionId, payload) {
    const safePayload = {
      content: payload?.content ?? '',
      tutor_mode: payload?.tutor_mode,
    }

    debugLog('[AI Tutor] sendMessage payload', {
      sessionId,
      payload: safePayload,
    })

    try {
      const response = await api.post(`/ai-tutor/sessions/${sessionId}/messages`, safePayload)
      debugLog('[AI Tutor] sendMessage response', response.data)
      return response.data
    } catch (error) {
      debugError('[AI Tutor] sendMessage error', {
        status: error?.response?.status,
        message: error?.apiMessage ?? error?.message,
        data: error?.response?.data,
      })
      throw error
    }
  },

  async saveMessageToNote(messageId, payload = {}) {
    const response = await api.post(`/ai-tutor/messages/${messageId}/save-note`, payload)
    return response.data
  },

  async deleteSession(sessionId) {
    const response = await api.delete(`/ai-tutor/sessions/${sessionId}`)
    return response.data
  },
}

export const createSession = aiTutorService.createSession
export const getSessions = aiTutorService.getSessions
export const getSession = aiTutorService.getSession
export const sendMessage = aiTutorService.sendMessage
export const saveMessageToNote = aiTutorService.saveMessageToNote
export const deleteSession = aiTutorService.deleteSession

export default aiTutorService


