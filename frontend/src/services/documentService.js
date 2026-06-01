import api, { HEAVY_REQUEST_TIMEOUT } from './api'

export const getDocuments = async () => {
  const response = await api.get('/documents')
  return response.data
}

export const uploadDocument = async ({ file, title, onUploadProgress } = {}) => {
  if (!file) {
    throw new Error('A document file is required.')
  }

  const formData = new FormData()
  formData.append('file', file)

  if (title) {
    formData.append('title', title)
  }

  const response = await api.post('/documents', formData, {
    timeout: HEAVY_REQUEST_TIMEOUT,
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress,
  })

  return response.data
}

export const askDocumentQuestion = async (documentId, payload) => {
  const response = await api.post(`/documents/${documentId}/ask`, payload)
  return response.data
}

export const summarizeDocument = async (documentId) => {
  const response = await api.post(`/documents/${documentId}/summarize`)
  return response.data
}

export const deleteDocument = async (documentId) => {
  const response = await api.delete(`/documents/${documentId}`)
  return response.data
}
