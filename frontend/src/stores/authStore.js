import { defineStore } from 'pinia'
import { authService } from '@/services/authService'

const TOKEN_STORAGE_KEY = 'edupath_token'
const USER_STORAGE_KEY = 'edupath_user'

const canUseStorage = () => typeof window !== 'undefined' && Boolean(window.localStorage)

const readStoredUser = () => {
  if (!canUseStorage()) return null

  try {
    const rawUser = window.localStorage.getItem(USER_STORAGE_KEY)
    return rawUser ? JSON.parse(rawUser) : null
  } catch {
    window.localStorage.removeItem(USER_STORAGE_KEY)
    return null
  }
}

const readStoredToken = () => {
  if (!canUseStorage()) return null
  return window.localStorage.getItem(TOKEN_STORAGE_KEY)
}

const persistSession = (token, user) => {
  if (!canUseStorage()) return
  window.localStorage.setItem(TOKEN_STORAGE_KEY, token)
  window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))
}

const clearStoredSession = () => {
  if (!canUseStorage()) return
  window.localStorage.removeItem(TOKEN_STORAGE_KEY)
  window.localStorage.removeItem(USER_STORAGE_KEY)
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: readStoredToken(),
    user: readStoredUser(),
    initialized: false,
    loading: false,
    error: null,
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token && state.user),
    userRole: (state) => state.user?.role ?? null,
  },

  actions: {
    setSession(session) {
      this.token = session.access_token
      this.user = session.user
      this.error = null
      this.initialized = true
      persistSession(session.access_token, session.user)
    },

    clearSession() {
      this.token = null
      this.user = null
      this.error = null
      this.initialized = true
      clearStoredSession()
    },

    async register(payload) {
      this.loading = true
      this.error = null

      try {
        const session = await authService.register(payload)
        this.setSession(session)
        return session
      } catch (error) {
        this.clearSession()
        this.error = error.apiMessage ?? error.message ?? 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async login(credentials) {
      this.loading = true
      this.error = null

      try {
        const session = await authService.login(credentials)
        this.setSession(session)
        return session
      } catch (error) {
        this.clearSession()
        this.error = error.apiMessage ?? error.message ?? 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    updateUserProfile(partialUser) {
      this.user = {
        ...(this.user || {}),
        ...partialUser,
      }

      if (canUseStorage()) {
        window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(this.user))
      }
    },

    async fetchCurrentUser() {
      if (!this.token) {
        this.clearSession()
        return null
      }

      this.loading = true
      this.error = null

      try {
        const user = await authService.me()
        this.user = user
        this.initialized = true

        if (canUseStorage()) {
          window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user))
        }

        return user
      } catch (error) {
        this.clearSession()
        this.error = error.apiMessage ?? error.message ?? 'Session expired'
        throw error
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.clearSession()
    },
  },
})