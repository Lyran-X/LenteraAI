import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'

export function useAuth() {
  const authStore = useAuthStore()
  const { token, user, loading, error, initialized, isAuthenticated, userRole } = storeToRefs(authStore)

  return {
    authStore,
    token,
    user,
    loading,
    error,
    initialized,
    isAuthenticated,
    userRole,
    login: authStore.login,
    register: authStore.register,
    fetchCurrentUser: authStore.fetchCurrentUser,
    logout: authStore.logout,
  }
}