import api from './api'

export const authService = {
  async register(payload) {
    const response = await api.post('/auth/register', payload)
    return response.data
  },

  async login(credentials) {
    const response = await api.post('/auth/login', credentials)
    return response.data
  },

  async me() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async logout() {
    const response = await api.post('/auth/logout')
    return response.data
  },
}

export default authService