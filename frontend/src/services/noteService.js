import api, { handleApiError } from './api'

export const mockNotes = [
  {
    id: 'note-1',
    title: 'Matrix transformation summary',
    source: 'AI Tutor',
    tags: ['matrix', 'linear algebra'],
    createdAt: 'Today',
    content:
      'A matrix can rotate, scale, shear, or project vectors depending on its columns. To understand the transformation, inspect where the basis vectors land after multiplication.',
  },
  {
    id: 'note-2',
    title: 'Document QA citation on eigenvectors',
    source: 'Document QA',
    tags: ['eigenvector', 'document'],
    createdAt: 'Yesterday',
    content:
      'Eigenvectors keep their direction after a matrix transformation, while their magnitude may change. The source chunk emphasized direction preservation as the key signal.',
  },
  {
    id: 'note-3',
    title: 'Quiz explanation for rank',
    source: 'Quiz',
    tags: ['rank', 'quiz-review'],
    createdAt: 'May 24',
    content:
      'Matrix rank is the number of pivot columns after row reduction. A common mistake is counting non-zero entries instead of independent columns.',
  },
]

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const getNotes = async (params = {}) => {
  try {
    const response = await api.get('/notes', { params })
    return response.data
  } catch (error) {
    return handleApiError(error, mockNotes, 'notes')
  }
}

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const createNote = async (payload) => {
  try {
    const response = await api.post('/notes', payload)
    return response.data
  } catch (error) {
    const fallback = {
      id: `note-${Date.now()}`,
      title: payload?.title ?? 'Saved AI answer',
      source: payload?.source ?? 'AI Tutor',
      tags: payload?.tags ?? ['saved'],
      createdAt: 'Just now',
      content: payload?.content ?? 'Prototype note content.',
      __mock: true,
    }

    return handleApiError(error, fallback, 'note')
  }
}

// TODO: replace mock fallback after backend Prompt 14-18 is implemented.
export const deleteNote = async (noteId) => {
  try {
    const response = await api.delete(`/notes/${noteId}`)
    return response.data
  } catch (error) {
    return handleApiError(error, { success: true, id: noteId, __mock: true }, 'note delete')
  }
}
