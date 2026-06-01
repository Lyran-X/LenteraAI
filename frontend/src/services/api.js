import axios from 'axios'

const TOKEN_STORAGE_KEY = 'edupath_token'
const USER_STORAGE_KEY = 'edupath_user'

export const DEFAULT_REQUEST_TIMEOUT = 10000
export const HEAVY_REQUEST_TIMEOUT = 120000
export const REQUEST_TIMEOUT_MESSAGE = 'Request took too long. The file may still be processing. Please try again with a smaller file or wait a moment.'

const readToken = () => {
  if (typeof window === 'undefined') return null
  return window.localStorage.getItem(TOKEN_STORAGE_KEY)
}

const clearStoredSession = () => {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(TOKEN_STORAGE_KEY)
  window.localStorage.removeItem(USER_STORAGE_KEY)
}

const extractApiMessage = (error) => {
  if (error?.code === 'ECONNABORTED') {
    return REQUEST_TIMEOUT_MESSAGE
  }

  const detail = error.response?.data?.detail

  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || item.message || String(item)).join(', ')
  }

  return detail || error.message || 'API request failed'
}

const removeContentTypeHeader = (headers) => {
  if (!headers) return

  if (typeof headers.delete === 'function') {
    headers.delete('Content-Type')
    headers.delete('content-type')
    return
  }

  delete headers['Content-Type']
  delete headers['content-type']
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: DEFAULT_REQUEST_TIMEOUT,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  config.headers = config.headers ?? {}
  config.headers['X-Client'] = 'edupath-ai-frontend'

  if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
    removeContentTypeHeader(config.headers)
  }

  const token = readToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    error.apiMessage = extractApiMessage(error)

    if (error.response?.status === 401) {
      clearStoredSession()
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('edupath:unauthorized'))
      }
    }

    return Promise.reject(error)
  },
)

export const isTimeoutError = (error) => error?.code === 'ECONNABORTED'

export const isNotFoundError = (error) => error?.response?.status === 404

export const isNetworkError = (error) => !error?.response

export const isBackendNotReadyError = (error) => {
  const status = error?.response?.status
  return status === 501 || status === 503 || status === 504
}

export const shouldUseMockFallback = (error) =>
  isNotFoundError(error) ||
  isNetworkError(error) ||
  isBackendNotReadyError(error) ||
  isTimeoutError(error)

export const cloneMock = (value) => {
  if (typeof structuredClone === 'function') {
    return structuredClone(value)
  }

  return JSON.parse(JSON.stringify(value))
}

export const handleApiError = (error, fallback, label = 'data') => {
  if (shouldUseMockFallback(error)) {
    console.warn(`Using mock ${label} because backend endpoint is not ready yet`)
    return cloneMock(fallback)
  }

  console.error(`${label} request failed`, error.apiMessage ?? error.message)
  throw error
}

export default api
