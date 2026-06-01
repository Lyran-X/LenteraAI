<template>
  <aside class="fixed inset-y-0 left-0 z-40 hidden w-64 bg-[#060c24] p-3 lg:block">
    <div class="flex h-full min-w-0 flex-col overflow-hidden rounded-3xl border border-white/10 bg-[#060c24] p-3">
      <RouterLink to="/dashboard" class="mb-6 flex min-w-0 items-center justify-center border-0 bg-transparent p-0 shadow-none ring-0" aria-label="LenteraAI dashboard home">
        <img :src="lenteraLogo" alt="LenteraAI" class="pointer-events-none mx-auto block h-auto w-[170px] max-w-full select-none object-contain" draggable="false" />
      </RouterLink>

      <nav class="thin-scrollbar mt-5 flex-1 space-y-1 overflow-y-auto pr-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.to"
          class="group flex min-h-11 min-w-0 items-center gap-3 rounded-2xl border px-3.5 py-3 text-sm font-medium transition duration-200"
          :class="isActiveRoute(item) ? 'border-cyan-300/25 bg-gradient-to-r from-cyan-400/15 to-violet-500/15 text-white shadow-lg shadow-cyan-950/20' : 'border-transparent text-slate-400 hover:bg-white/[0.06] hover:text-white'"
          :aria-current="isActiveRoute(item) ? 'page' : undefined"
        >
          <span
            class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border transition duration-200"
            :class="isActiveRoute(item) ? 'border-cyan-300/20 bg-cyan-400/10 text-cyan-200' : 'border-transparent bg-white/[0.03] text-slate-500 group-hover:bg-white/[0.07] group-hover:text-cyan-100'"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path :d="item.icon" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </span>
          <span class="truncate">{{ item.name }}</span>
        </RouterLink>
      </nav>

      <div class="mt-4 rounded-2xl border border-cyan-300/16 bg-cyan-300/8 p-3.5">
        <div class="flex items-center justify-between gap-2">
          <p class="text-sm font-semibold text-white">Focus Mode</p>
          <span v-if="focusLoading" class="h-1.5 w-1.5 shrink-0 animate-pulse rounded-full bg-cyan-300" />
        </div>
        <p class="mt-1 truncate text-xs leading-5 text-slate-400">{{ focusSubtitle }}</p>
        <div class="mt-3 h-2 overflow-hidden rounded-full bg-slate-800">
          <div
            class="h-2 rounded-full bg-gradient-to-r from-cyan-300 via-blue-400 to-violet-400 transition-all duration-500"
            :class="focusLoading ? 'animate-pulse' : ''"
            :style="focusProgressStyle"
          />
        </div>
        <div class="mt-2 flex items-center justify-between gap-3 text-[11px] font-medium text-slate-500">
          <span class="truncate">{{ focusSourceLabel }}</span>
          <span class="shrink-0 text-cyan-100/80">{{ focusProgress }}%</span>
        </div>
      </div>
    </div>
  </aside>

  <nav class="fixed inset-x-3 bottom-3 z-50 lg:hidden">
    <div class="glass-panel thin-scrollbar flex gap-1 overflow-x-auto rounded-2xl p-2">
      <RouterLink
        v-for="item in navItems"
        :key="item.name"
        :to="item.to"
        class="flex min-w-18 flex-col items-center justify-center gap-1 rounded-xl border px-2.5 py-2 text-xs font-medium transition duration-200"
        :class="isActiveRoute(item) ? 'border-cyan-300/25 bg-gradient-to-r from-cyan-400/15 to-violet-500/15 text-white' : 'border-transparent text-slate-400 hover:bg-white/[0.06] hover:text-white'"
        :aria-current="isActiveRoute(item) ? 'page' : undefined"
      >
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path :d="item.icon" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <span class="max-w-16 truncate">{{ item.shortName }}</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import lenteraLogo from '@/assets/brand/lenteraai-logo.png'
import { getDashboardAnalytics } from '@/services/analyticsService'
import { getActiveStudyPlan } from '@/services/studyPlanService'

type NavItem = {
  name: string
  shortName: string
  to: string
  icon: string
}

type StudyPlanItem = {
  id?: string
  is_completed?: boolean
}

type StudyPlan = {
  id?: string
  title?: string
  progress_percentage?: number | string | null
  items?: StudyPlanItem[]
}

type AnalyticsSummary = {
  study_streak?: number | string | null
  retention_score?: number | string | null
  average_score?: number | string | null
}

const route = useRoute()

const navItems: NavItem[] = [
  { name: 'Overview', shortName: 'Home', to: '/dashboard', icon: 'M4 13h6V4H4v9Zm10 7h6V4h-6v16ZM4 20h6v-3H4v3Z' },
  { name: 'AI Tutor', shortName: 'Tutor', to: '/dashboard/ai-tutor', icon: 'M12 4a7 7 0 0 0-7 7v2a4 4 0 0 0 4 4h1l2 3 2-3h1a4 4 0 0 0 4-4v-2a7 7 0 0 0-7-7Z' },
  { name: 'Document Lab', shortName: 'Docs', to: '/dashboard/document-lab', icon: 'M7 3h7l5 5v13H7V3Zm7 0v5h5M10 13h6M10 17h4' },
  { name: 'Smart Plan', shortName: 'Plan', to: '/dashboard/smart-plan', icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01' },
  { name: 'Quiz Arena', shortName: 'Quiz', to: '/dashboard/quiz-arena', icon: 'M12 3 4 7v6c0 5 8 8 8 8s8-3 8-8V7l-8-4Zm-2 8h4M10 15h4' },
  { name: 'Progress Insight', shortName: 'Stats', to: '/dashboard/progress', icon: 'M4 19V9M10 19V5M16 19v-7M22 19H2' },
  { name: 'Saved Notes', shortName: 'Notes', to: '/dashboard/notes', icon: 'M6 3h12v18l-6-3-6 3V3Z' },
  { name: 'Profile Settings', shortName: 'Profile', to: '/dashboard/settings', icon: 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm7 9a7 7 0 0 0-14 0' },
]

const focusLoading = ref(false)
const focusError = ref(false)
const activeStudyPlan = ref<StudyPlan | null>(null)
const analyticsSummary = ref<AnalyticsSummary | null>(null)

const clampPercent = (value: unknown) => {
  const numeric = Number(value ?? 0)
  if (!Number.isFinite(numeric)) return 0
  return Math.max(0, Math.min(100, Math.round(numeric)))
}

const planItems = computed(() => (Array.isArray(activeStudyPlan.value?.items) ? activeStudyPlan.value?.items ?? [] : []))
const totalTasks = computed(() => planItems.value.length)
const completedTasks = computed(() => planItems.value.filter((item) => Boolean(item.is_completed)).length)
const remainingTasks = computed(() => Math.max(0, totalTasks.value - completedTasks.value))
const planProgress = computed(() => {
  const backendProgress = activeStudyPlan.value?.progress_percentage
  if (backendProgress !== null && backendProgress !== undefined) return clampPercent(backendProgress)
  return totalTasks.value > 0 ? clampPercent((completedTasks.value / totalTasks.value) * 100) : 0
})

const fallbackProgress = computed(() => {
  const retentionScore = analyticsSummary.value?.retention_score
  if (retentionScore !== null && retentionScore !== undefined) return clampPercent(retentionScore)
  return clampPercent(analyticsSummary.value?.average_score)
})

const focusProgress = computed(() => {
  if (focusLoading.value) return 36
  if (focusError.value) return 0
  if (activeStudyPlan.value) return planProgress.value
  if (analyticsSummary.value) return fallbackProgress.value
  return 0
})

const focusProgressStyle = computed(() => ({ width: `${focusProgress.value}%` }))

const focusSubtitle = computed(() => {
  if (focusLoading.value) return 'Loading focus...'
  if (focusError.value) return 'Focus data unavailable'

  if (activeStudyPlan.value) {
    if (totalTasks.value === 0) return 'Plan is ready'
    if (remainingTasks.value === 0) return 'All quests completed'
    return `${remainingTasks.value} ${remainingTasks.value === 1 ? 'quest' : 'quests'} left this plan`
  }

  if (analyticsSummary.value) {
    const streak = Number(analyticsSummary.value.study_streak ?? 0)
    if (Number.isFinite(streak) && streak > 0) return `${Math.round(streak)} day streak`
  }

  return 'Create your first roadmap'
})

const focusSourceLabel = computed(() => {
  if (focusLoading.value) return 'Syncing data'
  if (focusError.value) return 'Try again later'
  if (activeStudyPlan.value) return 'Active plan'
  if (analyticsSummary.value) return 'Learning score'
  return 'No active plan'
})

const loadFocusMode = async () => {
  focusLoading.value = true
  focusError.value = false

  const [planResult, analyticsResult] = await Promise.allSettled([getActiveStudyPlan(), getDashboardAnalytics()])

  if (planResult.status === 'fulfilled') {
    activeStudyPlan.value = planResult.value
  } else {
    activeStudyPlan.value = null
    console.error('Focus Mode active plan request failed:', planResult.reason)
  }

  if (analyticsResult.status === 'fulfilled') {
    analyticsSummary.value = analyticsResult.value?.summary ?? analyticsResult.value ?? null
  } else {
    analyticsSummary.value = null
    console.error('Focus Mode analytics request failed:', analyticsResult.reason)
  }

  focusError.value = planResult.status === 'rejected' && analyticsResult.status === 'rejected'
  focusLoading.value = false
}

const isActiveRoute = (item: NavItem) => {
  if (item.to === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(item.to)
}

watch(
  () => route.path,
  (newPath, oldPath) => {
    if (newPath !== oldPath && (newPath === '/dashboard' || newPath.startsWith('/dashboard/smart-plan'))) {
      void loadFocusMode()
    }
  },
)

onMounted(() => {
  void loadFocusMode()
})
</script>