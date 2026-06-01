import api from './api'

const normalizeParams = (params = {}) => {
  const normalized = {}

  if (params.search) normalized.search = String(params.search).trim()
  if (params.source_type) normalized.source_type = params.source_type
  if (params.pinned !== undefined && params.pinned !== null && params.pinned !== '') normalized.pinned = params.pinned
  if (params.limit) normalized.limit = params.limit

  return normalized
}

export const getNotes = async (params = {}) => {
  const response = await api.get('/notes', { params: normalizeParams(params) })
  return response.data
}

export const getNote = async (noteId) => {
  const response = await api.get(`/notes/${noteId}`)
  return response.data
}

export const createNote = async (payload) => {
  const response = await api.post('/notes', payload)
  return response.data
}

export const updateNote = async (noteId, payload) => {
  const response = await api.patch(`/notes/${noteId}`, payload)
  return response.data
}

export const deleteNote = async (noteId) => {
  const response = await api.delete(`/notes/${noteId}`)
  return response.data
}

export const pinNote = async (noteId) => {
  const response = await api.patch(`/notes/${noteId}/pin`)
  return response.data
}

export const unpinNote = async (noteId) => {
  const response = await api.patch(`/notes/${noteId}/unpin`)
  return response.data
}

export default {
  getNotes,
  getNote,
  createNote,
  updateNote,
  deleteNote,
  pinNote,
  unpinNote,
}