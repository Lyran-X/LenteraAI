import api from './api'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
const AVATAR_UPLOAD_TIMEOUT = 60000

export const API_ORIGIN = (() => {
  try {
    return new URL(API_BASE_URL).origin
  } catch {
    return API_BASE_URL.replace(/\/api\/?$/, '')
  }
})()

export const getAssetUrl = (path) => {
  if (!path) return ''
  if (/^https?:\/\//i.test(path)) return path
  const normalizedPath = String(path).startsWith('/') ? path : `/${path}`
  return `${API_ORIGIN}${normalizedPath}`
}

export const getProfile = async () => {
  const response = await api.get('/users/me/profile')
  return response.data
}

export const updateProfile = async (payload) => {
  const response = await api.patch('/users/me/profile', payload)
  return response.data
}

export const updateAiSettings = async (payload) => {
  const response = await api.patch('/users/me/ai-settings', payload)
  return response.data
}

export const uploadAvatar = async (file) => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post('/users/me/avatar', formData, {
    timeout: AVATAR_UPLOAD_TIMEOUT,
  })
  return response.data
}

export const deleteAvatar = async () => {
  const response = await api.delete('/users/me/avatar')
  return response.data
}

export const changePassword = async (payload) => {
  const response = await api.patch('/users/me/password', payload)
  return response.data
}

export const exportLearningData = async () => {
  const response = await api.get('/users/me/export')
  return response.data
}

export default {
  getProfile,
  updateProfile,
  updateAiSettings,
  uploadAvatar,
  deleteAvatar,
  changePassword,
  exportLearningData,
  getAssetUrl,
}