import { createRouter, createWebHistory } from 'vue-router'

import DashboardLayout from '@/layouts/DashboardLayout.vue'
import PublicLayout from '@/layouts/PublicLayout.vue'
import Landing from '@/landing_project/landing.vue'
import Login from '@/landing_project/auth/Login.vue'
import Register from '@/landing_project/auth/Register.vue'
import ForgotPassword from '@/landing_project/auth/ForgotPassword.vue'
import NotFound from '@/landing_project/pages/NotFound.vue'
import PrivacyPolicy from '@/landing_project/pages/PrivacyPolicy.vue'
import Supports from '@/landing_project/pages/Supports.vue'
import TermsOfUse from '@/landing_project/pages/TermsOfUse.vue'
import { useAuthStore } from '@/stores/authStore'
import AiTutor from '@/views/AiTutor.vue'
import DashboardOverview from '@/views/DashboardOverview.vue'
import DocumentLab from '@/views/DocumentLab.vue'
import ProfileSettings from '@/views/ProfileSettings.vue'
import ProgressInsight from '@/views/ProgressInsight.vue'
import QuizArena from '@/views/QuizArena.vue'
import SavedNotes from '@/views/SavedNotes.vue'
import SmartPlan from '@/views/SmartPlan.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: PublicLayout,
      children: [
        { path: '', name: 'Landing', component: Landing },
        { path: 'login', name: 'Login', component: Login, meta: { publicOnly: true } },
        { path: 'register', name: 'Register', component: Register, meta: { publicOnly: true } },
        { path: 'forgot-password', name: 'ForgotPassword', component: ForgotPassword, meta: { publicOnly: true } },
        { path: 'terms', name: 'TermsOfUse', component: TermsOfUse },
        { path: 'privacy', name: 'PrivacyPolicy', component: PrivacyPolicy },
        { path: 'supports', name: 'Supports', component: Supports },
      ],
    },
    {
      path: '/dashboard',
      component: DashboardLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'DashboardOverview',
          component: DashboardOverview,
          meta: { title: 'Dashboard Overview', eyebrow: 'Today in EduPath' },
        },
        {
          path: 'ai-tutor',
          name: 'AiTutor',
          component: AiTutor,
          meta: { title: 'AI Tutor', eyebrow: 'Ask and learn' },
        },
        {
          path: 'document-lab',
          name: 'DocumentLab',
          component: DocumentLab,
          meta: { title: 'Document Lab', eyebrow: 'RAG workspace' },
        },
        {
          path: 'smart-plan',
          name: 'SmartPlan',
          component: SmartPlan,
          meta: { title: 'Smart Plan', eyebrow: 'Personal roadmap' },
        },
        {
          path: 'quiz-arena',
          name: 'QuizArena',
          component: QuizArena,
          meta: { title: 'Quiz Arena', eyebrow: 'Practice mode' },
        },
        {
          path: 'progress',
          name: 'ProgressInsight',
          component: ProgressInsight,
          meta: { title: 'Progress Insight', eyebrow: 'Learning analytics' },
        },
        {
          path: 'notes',
          name: 'SavedNotes',
          component: SavedNotes,
          meta: { title: 'Saved Notes', eyebrow: 'Knowledge vault' },
        },
        {
          path: 'settings',
          name: 'ProfileSettings',
          component: ProfileSettings,
          meta: { title: 'Profile Settings', eyebrow: 'Account preferences' },
        },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
  ],
})

const authRedirect = (targetPath: string) => ({
  name: 'Login',
  query: { redirect: targetPath },
})

const ensureCurrentUser = async (authStore: ReturnType<typeof useAuthStore>) => {
  if (!authStore.token) return false
  if (!authStore.user) {
    await authStore.fetchCurrentUser()
  }
  return Boolean(authStore.user)
}

router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some((route) => route.meta.requiresAuth)
  const publicOnly = to.matched.some((route) => route.meta.publicOnly)
  const allowedRoles = to.matched.flatMap((route) => (Array.isArray(route.meta.roles) ? route.meta.roles : [])) as string[]

  if (requiresAuth) {
    if (!authStore.token) {
      return authRedirect(to.fullPath)
    }

    try {
      const hasCurrentUser = await ensureCurrentUser(authStore)
      if (!hasCurrentUser) {
        return authRedirect(to.fullPath)
      }
    } catch {
      authStore.logout()
      return authRedirect(to.fullPath)
    }

    if (allowedRoles.length > 0 && !allowedRoles.includes(authStore.user?.role)) {
      return { name: 'DashboardOverview' }
    }
  }

  if (publicOnly && authStore.token) {
    try {
      await ensureCurrentUser(authStore)
    } catch {
      authStore.logout()
      return true
    }

    if (authStore.isAuthenticated) {
      return { name: 'DashboardOverview' }
    }
  }

  return true
})

export default router