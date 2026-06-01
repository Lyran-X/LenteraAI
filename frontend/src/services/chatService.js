import api, { handleApiError } from './api'

export const mockChatSessions = [
  {
    id: 'session-linear-algebra',
    title: 'Linear Algebra Review',
    topic: 'Matrix transformations',
    preview: 'Explain why order matters in matrix multiplication.',
    mode: 'Explain Simply',
    updatedAt: 'Today 09:12',
  },
  {
    id: 'session-socratic',
    title: 'Socratic Eigenvectors',
    topic: 'Eigenvectors',
    preview: 'Guide me with questions instead of direct answers.',
    mode: 'Socratic Mode',
    updatedAt: 'Yesterday',
  },
  {
    id: 'session-physics',
    title: 'Physics Practice',
    topic: 'Motion formulas',
    preview: 'Generate a practice question about acceleration.',
    mode: 'Practice Question',
    updatedAt: 'May 24',
  },
]

export const mockChatMessages = [
  {
    id: 'msg-1',
    sessionId: 'session-linear-algebra',
    role: 'assistant',
    mode: 'Explain Simply',
    content:
      'Hi Alya, I can help you break down matrix transformations, quiz mistakes, or document concepts.',
    createdAt: '09:12',
  },
  {
    id: 'msg-2',
    sessionId: 'session-linear-algebra',
    role: 'user',
    mode: 'Explain Simply',
    content: 'Why does matrix multiplication order matter?',
    createdAt: '09:13',
  },
  {
    id: 'msg-3',
    sessionId: 'session-linear-algebra',
    role: 'assistant',
    mode: 'Explain Simply',
    content:
      'Matrix multiplication order matters because each matrix represents an action. Doing action A then B can land you somewhere different than doing B then A.',
    createdAt: '09:13',
  },
]

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const getChatSessions = async () => {
  try {
    const response = await api.get('/chat/sessions')
    return response.data
  } catch (error) {
    return handleApiError(error, mockChatSessions, 'chat sessions')
  }
}

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const createChatSession = async (payload = {}) => {
  try {
    const response = await api.post('/chat/sessions', payload)
    return response.data
  } catch (error) {
    const fallback = {
      id: `session-${Date.now()}`,
      title: payload.title ?? 'New AI Tutor Session',
      topic: payload.topic ?? 'General learning',
      preview: 'Prototype session created locally.',
      mode: payload.mode ?? 'Explain Simply',
      updatedAt: 'Just now',
      __mock: true,
    }

    return handleApiError(error, fallback, 'chat session')
  }
}

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const getChatMessages = async (sessionId) => {
  try {
    const response = await api.get(`/chat/sessions/${sessionId}/messages`)
    return response.data
  } catch (error) {
    const fallback = mockChatMessages.filter((message) => message.sessionId === sessionId)
    return handleApiError(error, fallback.length ? fallback : mockChatMessages, 'chat messages')
  }
}

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const sendChatMessage = async (sessionId, payload) => {
  try {
    const response = await api.post(`/chat/sessions/${sessionId}/messages`, payload)
    return response.data
  } catch (error) {
    const mode = payload?.mode ?? 'Explain Simply'
    const question = payload?.content ?? payload?.message ?? 'Can you help me study this topic?'
    const fallback = {
      id: `msg-${Date.now()}`,
      sessionId,
      role: 'assistant',
      mode,
      content: `Prototype AI response in ${mode}: ${question}\n\nStart with the core idea, connect it to one example, then check your understanding with a quick question.`,
      createdAt: 'Just now',
      __mock: true,
    }

    return handleApiError(error, fallback, 'chat message')
  }
}
