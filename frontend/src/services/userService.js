import api from './api'

const normalizeUserPayload = (payload) => ({
  email: payload.email,
  name: payload.name ?? payload.full_name ?? payload.fullName,
  password: payload.password,
  role: payload.role ?? 'student',
})

export const getUsers = async (params = {}) => {
  try {
    const response = await api.get('/users', { params })
    return response.data
  } catch (error) {
    console.error('Failed to fetch users from backend', error.apiMessage ?? error.message)
    throw error
  }
}

export const createUser = async (payload) => {
  try {
    const response = await api.post('/users', normalizeUserPayload(payload))
    return response.data
  } catch (error) {
    console.error('Failed to create user in backend', error.apiMessage ?? error.message)
    throw error
  }
}

export const getUserById = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch user from backend', error.apiMessage ?? error.message)
    throw error
  }
}