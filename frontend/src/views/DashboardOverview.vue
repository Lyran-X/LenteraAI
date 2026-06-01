<template>
  <div class="w-full min-w-0 space-y-6 overflow-x-hidden sm:space-y-7">
    <section class="grid min-w-0 items-stretch gap-5 xl:grid-cols-[minmax(0,1.45fr)_minmax(18rem,0.75fr)] xl:gap-6">
      <div class="glass-panel min-w-0 overflow-hidden rounded-3xl p-5 sm:p-6">
        <div class="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div class="max-w-3xl">
            <p class="text-sm font-semibold uppercase tracking-[0.16em] text-cyan-200/80">Dashboard overview</p>
            <h2 class="mt-4 text-2xl font-semibold tracking-normal text-white sm:text-3xl xl:text-4xl">
              {{ welcomeHeading }}
              <span class="block text-gradient">Your learning dashboard is focused on progress, weak topics, and next actions.</span>
            </h2>
            <p class="mt-5 max-w-2xl text-sm leading-6 text-slate-300 sm:text-base">
              Analytics are calculated from your quizzes, study plans, saved notes, and AI Tutor activity.
            </p>
            <div class="mt-4 flex flex-wrap gap-2">
              <span v-if="isDashboardLoading" class="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold text-cyan-100">Loading analytics</span>
              <span v-else-if="dashboardApiNotice" class="rounded-full border border-white/10 bg-white/[0.06] px-3 py-1 text-xs font-medium text-slate-300">{{ dashboardApiNotice }}</span>
            </div>
          </div>

          <div class="flex w-full flex-col gap-3 sm:w-auto sm:flex-row lg:flex-col">
            <RouterLink to="/dashboard/ai-tutor" class="inline-flex min-h-12 w-full min-w-[150px] items-center justify-center whitespace-nowrap rounded-xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-5 py-3 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition hover:brightness-110 sm:w-[150px]">
              Start Learning
            </RouterLink>
            <RouterLink class="inline-flex min-h-12 w-full min-w-[150px] items-center justify-center whitespace-nowrap rounded-xl border border-white/12 bg-white/8 px-5 py-3 text-sm font-semibold text-slate-100 transition hover:bg-white/12 sm:w-[150px]" to="/dashboard/smart-plan">
              View Plan
            </RouterLink>
          </div>
        </div>

        <div class="mt-6 grid min-w-0 gap-3 sm:grid-cols-2 2xl:grid-cols-3">
          <div v-for="target in todayTargets" :key="target.label" class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.055] p-4 transition duration-200 hover:border-cyan-300/25 hover:bg-white/[0.08]">
            <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">{{ target.label }}</p>
            <p class="mt-2 text-sm font-medium text-white">{{ target.value }}</p>
          </div>
        </div>
      </div>

      <GlassCard padding="p-5 sm:p-6" extra-class="flex min-w-0 flex-col justify-between h-full">
        <div class="flex flex-1 flex-col justify-center">
          <div class="flex justify-center">
            <span class="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-3 py-1 text-sm font-medium text-emerald-200">Rule-based</span>
          </div>
          <div class="mt-5 text-center">
            <p class="text-sm font-medium text-slate-400">Retention score</p>
            <p class="mt-3 text-5xl font-semibold text-white">{{ percent(summary.retention_score) }}</p>
          </div>
          <div class="mx-auto mt-7 w-full max-w-sm">
            <div class="h-3 rounded-full bg-slate-800/80">
              <div class="h-3 rounded-full bg-gradient-to-r from-cyan-300 via-blue-400 to-violet-400 transition-all duration-500" :style="{ width: `${summary.retention_score ?? 0}%` }" />
            </div>
          </div>
        </div>

        <div class="mt-6 rounded-2xl border border-cyan-300/14 bg-cyan-300/[0.06] p-4">
          <p class="text-sm font-semibold text-white">Next best action</p>
          <p class="mt-2 text-sm leading-6 text-slate-300">{{ primaryInsight.message }}</p>
        </div>
      </GlassCard>
    </section>

    <section class="grid min-w-0 gap-4 sm:grid-cols-2 2xl:grid-cols-4">
      <StatCard v-for="stat in dashboardStats" :key="stat.label" :label="stat.label" :value="stat.value" :trend="stat.trend" :caption="stat.caption" :accent="stat.accent" :icon="stat.icon" :value-class="stat.valueClass" :trend-positive="stat.trendPositive" />
    </section>

    <section class="grid min-w-0 items-stretch gap-5 xl:grid-cols-[minmax(0,1.35fr)_minmax(360px,0.9fr)] xl:gap-6">
      <GlassCard padding="p-5 sm:p-6" extra-class="min-w-0 h-full">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-sm font-medium text-amber-200/80">Weak topics</p>
            <h3 class="mt-1 text-xl font-semibold text-white">Needs review</h3>
          </div>
          <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">{{ weakTopics.length }} topics</span>
        </div>

        <div v-if="weakTopics.length === 0" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
          No weak topics detected yet.
        </div>
        <div v-else class="mt-5 space-y-4">
          <div class="grid gap-3 sm:grid-cols-2 2xl:grid-cols-3">
            <div v-for="topic in paginatedWeakTopics" :key="topic.name" class="min-w-0 rounded-2xl border border-white/8 bg-white/[0.045] p-4 transition duration-200 hover:border-amber-300/25 hover:bg-white/[0.07]">
              <div class="flex items-start justify-between gap-3">
                <div class="min-w-0">
                  <p class="line-clamp-1 font-semibold text-white">{{ topic.name }}</p>
                  <p class="mt-1 line-clamp-2 text-sm leading-5 text-slate-500">{{ topic.reason }}</p>
                </div>
                <p class="shrink-0 text-sm font-semibold text-amber-200">{{ topic.score }}%</p>
              </div>
              <div class="mt-4 h-2 rounded-full bg-slate-800">
                <div class="h-2 rounded-full bg-gradient-to-r from-amber-300 via-cyan-300 to-blue-400 transition-all duration-300" :style="{ width: `${topic.score}%` }" />
              </div>
              <RouterLink to="/dashboard/ai-tutor" class="mt-4 inline-flex min-h-9 w-full items-center justify-center rounded-xl border border-white/10 bg-white/[0.055] px-3 text-sm font-semibold text-slate-200 transition hover:border-cyan-300/30 hover:bg-cyan-300/10 hover:text-cyan-100">
                Review Topic
              </RouterLink>
            </div>
          </div>

          <div v-if="weakTopicsTotalPages > 1" class="flex flex-wrap items-center justify-center gap-2 pt-1">
            <button class="pagination-button" type="button" :disabled="weakTopicsPage === 1" @click="prevWeakTopicsPage">Previous</button>
            <button v-for="page in visibleWeakTopicPages" :key="page" class="pagination-number" :class="weakTopicsPage === page ? 'pagination-number-active' : ''" type="button" @click="goToWeakTopicsPage(page)">
              {{ page }}
            </button>
            <button class="pagination-button" type="button" :disabled="weakTopicsPage === weakTopicsTotalPages" @click="nextWeakTopicsPage">Next</button>
          </div>
        </div>
      </GlassCard>

      <GlassCard padding="p-5 sm:p-6" extra-class="min-w-0 h-full">
        <div class="flex h-full flex-col">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Quick actions</p>
            <h3 class="mt-1 text-xl font-semibold text-white">Jump back in</h3>
            <p class="mt-2 text-sm leading-6 text-slate-400">Choose the next learning action based on your analytics.</p>
          </div>

          <div class="flex flex-1 flex-col justify-center pt-5">
            <div class="grid min-w-0 gap-3 sm:grid-cols-2 xl:grid-cols-1 2xl:grid-cols-2">
              <RouterLink v-for="action in quickActions" :key="action.title" :to="action.to" class="group min-w-0 rounded-2xl border border-white/8 bg-white/[0.045] p-3.5 transition duration-200 hover:border-cyan-300/30 hover:bg-white/[0.075]">
                <div class="flex items-start gap-3">
                  <div :class="['flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border', action.iconClass]">
                    <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                      <path :d="action.icon" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                    </svg>
                  </div>
                  <div class="min-w-0">
                    <p class="font-semibold text-white">{{ action.title }}</p>
                    <p class="mt-1 text-sm leading-5 text-slate-500">{{ action.caption }}</p>
                  </div>
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid min-w-0 items-stretch gap-5 xl:grid-cols-[minmax(0,1.1fr)_minmax(20rem,0.9fr)] xl:gap-6">
      <GlassCard padding="p-5 sm:p-6" extra-class="min-w-0 h-full">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Recent quizzes</p>
            <h3 class="mt-1 text-xl font-semibold text-white">Latest attempts</h3>
          </div>
          <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">{{ recentQuizzes.length }} attempts</span>
        </div>

        <div v-if="recentQuizzes.length === 0" class="mt-6 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
          Submit a quiz to populate recent performance.
        </div>
        <div v-else class="mt-6 space-y-4">
          <div class="divide-y divide-white/8">
            <div v-for="quiz in paginatedRecentQuizzes" :key="quiz.id" class="grid min-w-0 gap-4 py-4 md:grid-cols-[minmax(0,1fr)_5rem_7rem] md:items-center">
              <div class="min-w-0">
                <p class="truncate font-medium text-white">{{ quiz.topic }}</p>
                <p class="mt-1 text-sm text-slate-400">{{ quiz.difficulty }} / {{ quiz.date }}</p>
              </div>
              <p class="text-left text-sm font-medium text-slate-300 md:text-right">{{ quiz.score }}%</p>
              <span :class="['w-fit rounded-full px-3 py-1 text-xs font-semibold', quiz.score >= 80 ? 'bg-emerald-300/10 text-emerald-100' : 'bg-amber-300/10 text-amber-100']">{{ quiz.score >= 80 ? 'On track' : 'Review' }}</span>
            </div>
          </div>

          <div v-if="recentQuizzesTotalPages > 1" class="flex flex-wrap items-center justify-center gap-2 pt-1">
            <button class="pagination-button" type="button" :disabled="recentQuizzesPage === 1" @click="prevRecentQuizzesPage">Previous</button>
            <button v-for="page in visibleRecentQuizPages" :key="page" class="pagination-number" :class="recentQuizzesPage === page ? 'pagination-number-active' : ''" type="button" @click="goToRecentQuizzesPage(page)">
              {{ page }}
            </button>
            <button class="pagination-button" type="button" :disabled="recentQuizzesPage === recentQuizzesTotalPages" @click="nextRecentQuizzesPage">Next</button>
          </div>
        </div>
      </GlassCard>

      <GlassCard padding="p-5 sm:p-6" extra-class="min-w-0 h-full">
        <div class="flex h-full min-h-[22rem] flex-col justify-center gap-5">
          <div class="flex items-center justify-between gap-3">
            <div>
              <p class="text-sm font-medium text-violet-200/80">Insights</p>
              <h3 class="mt-1 text-xl font-semibold text-white">Recommendations</h3>
            </div>
            <span class="rounded-full border border-amber-300/20 bg-amber-300/10 px-3 py-1 text-sm font-medium text-amber-100">{{ insights.length }}</span>
          </div>

          <div class="space-y-3">
            <div v-for="insight in insights" :key="`${insight.title}-${insight.message}`" class="rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <p class="text-sm font-semibold text-white">{{ insight.title }}</p>
              <p class="mt-2 text-sm leading-6 text-slate-300">{{ insight.message }}</p>
            </div>
          </div>

          <RouterLink class="inline-flex min-h-11 items-center justify-center rounded-xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-4 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition hover:brightness-110" to="/dashboard/ai-tutor">
            Ask AI Tutor
          </RouterLink>
        </div>
      </GlassCard>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import GlassCard from '../components/GlassCard.vue'
import StatCard from '../components/StatCard.vue'
import { getDashboardAnalytics } from '../services/analyticsService'
import { getProfile } from '../services/profileService'
import { useAuthStore } from '../stores/authStore'

const WEAK_TOPICS_PAGE_SIZE = 6
const RECENT_QUIZZES_PAGE_SIZE = 4

type WeakTopicCard = {
  name: string
  score: number
  reason: string
}

type RecentQuizCard = {
  id: string
  topic: string
  score: number
  difficulty: string
  date: string
}
const authStore = useAuthStore()
const dashboard = ref<any | null>(null)
const profileName = ref('')
const weakTopicsPage = ref(1)
const recentQuizzesPage = ref(1)
const isDashboardLoading = ref(false)
const dashboardApiNotice = ref('')

const fallbackSummary = {
  average_score: 0,
  total_quizzes: 0,
  total_attempts: 0,
  active_study_plans: 0,
  completed_study_plans: 0,
  study_streak: 0,
  retention_score: 0,
  saved_notes_count: 0,
  ai_tutor_sessions_count: 0,
}

const summary = computed(() => dashboard.value?.summary ?? fallbackSummary)
const insights = computed(() => dashboard.value?.insights?.length ? dashboard.value.insights : [{ title: 'Start your learning loop', message: 'Generate a quiz or study plan to unlock personalized recommendations.' }])
const primaryInsight = computed(() => insights.value[0])
const cleanDisplayName = (value: unknown) => {
  const name = String(value ?? '').trim()
  return name && !['undefined', 'null'].includes(name.toLowerCase()) ? name : ''
}
const displayName = computed(() => cleanDisplayName(profileName.value) || cleanDisplayName(authStore.user?.name))
const welcomeHeading = computed(() => (displayName.value ? `Welcome back, ${displayName.value}` : 'Welcome back'))
const percent = (value: unknown) => `${Math.round(Number(value ?? 0))}%`
const formatDate = (value?: string) => {
  if (!value) return 'Recent'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return 'Recent'
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(parsed)
}
const paginate = <T,>(items: T[], page: number, pageSize: number) => items.slice((page - 1) * pageSize, page * pageSize)
const totalPagesFor = (items: unknown[], pageSize: number) => Math.max(1, Math.ceil(items.length / pageSize))
const clampPage = (page: number, totalPages: number) => Math.min(Math.max(page, 1), Math.max(totalPages, 1))
const pageNumbers = (currentPage: number, totalPages: number) => {
  if (totalPages <= 5) return Array.from({ length: totalPages }, (_, index) => index + 1)
  const start = Math.max(1, Math.min(currentPage - 2, totalPages - 4))
  return Array.from({ length: 5 }, (_, index) => start + index)
}

const todayTargets = computed(() => [
  { label: 'Average score', value: percent(summary.value.average_score) },
  { label: 'Quiz attempts', value: `${summary.value.total_attempts} attempts from ${summary.value.total_quizzes} quizzes` },
  { label: 'Study streak', value: `${summary.value.study_streak} day streak` },
])

const activeStudyPlans = computed(() => Number(summary.value.active_study_plans ?? 0))
const completedStudyPlans = computed(() => Number(summary.value.completed_study_plans ?? 0))
const totalStudyPlans = computed(() => activeStudyPlans.value + completedStudyPlans.value)
const studyPlansTrend = computed(() => (
  totalStudyPlans.value > 0
    ? `${activeStudyPlans.value} active · ${completedStudyPlans.value} completed`
    : 'No study plans yet'
))

const dashboardStats = computed(() => [
  { label: 'Average Quiz Score', value: percent(summary.value.average_score), trend: `${summary.value.total_attempts} attempts`, caption: 'All submitted quizzes', accent: 'cyan' as const, icon: 'chart' as const, valueClass: '', trendPositive: true },
  { label: 'Study Plans', value: `${totalStudyPlans.value} total`, trend: studyPlansTrend.value, caption: 'Current user plans', accent: 'blue' as const, icon: 'plans' as const, valueClass: '', trendPositive: true },
  { label: 'Saved Notes', value: String(summary.value.saved_notes_count), trend: 'notes', caption: 'Saved learning notes', accent: 'violet' as const, icon: 'notes' as const, valueClass: 'pl-2', trendPositive: true },
  { label: 'AI Tutor Sessions', value: String(summary.value.ai_tutor_sessions_count), trend: 'sessions', caption: 'Protected tutor activity', accent: 'amber' as const, icon: 'tutor' as const, valueClass: 'pl-2', trendPositive: true },
])

const weakTopics = computed<WeakTopicCard[]>(() => (dashboard.value?.weak_topics ?? []).map((topic: any) => ({
  name: topic.topic ?? 'Untitled topic',
  score: Math.round(Number(topic.accuracy ?? 0)),
  reason: topic.recommendation ?? 'Review this topic with AI Tutor and retry a focused quiz.',
})))

const recentQuizzes = computed<RecentQuizCard[]>(() => (dashboard.value?.recent_quizzes ?? []).map((quiz: any, index: number) => ({
  id: quiz.attempt_id ?? quiz.id ?? `${quiz.quiz_id ?? 'quiz'}-${index}`,
  topic: quiz.topic ?? quiz.quiz_title ?? 'Quiz attempt',
  score: Math.round(Number(quiz.score ?? 0)),
  difficulty: quiz.difficulty ?? 'medium',
  date: formatDate(quiz.submitted_at),
})))

const weakTopicsTotalPages = computed(() => totalPagesFor(weakTopics.value, WEAK_TOPICS_PAGE_SIZE))
const paginatedWeakTopics = computed(() => paginate(weakTopics.value, weakTopicsPage.value, WEAK_TOPICS_PAGE_SIZE))
const visibleWeakTopicPages = computed(() => pageNumbers(weakTopicsPage.value, weakTopicsTotalPages.value))
const recentQuizzesTotalPages = computed(() => totalPagesFor(recentQuizzes.value, RECENT_QUIZZES_PAGE_SIZE))
const paginatedRecentQuizzes = computed(() => paginate(recentQuizzes.value, recentQuizzesPage.value, RECENT_QUIZZES_PAGE_SIZE))
const visibleRecentQuizPages = computed(() => pageNumbers(recentQuizzesPage.value, recentQuizzesTotalPages.value))

const goToWeakTopicsPage = (page: number) => {
  weakTopicsPage.value = clampPage(page, weakTopicsTotalPages.value)
}
const nextWeakTopicsPage = () => goToWeakTopicsPage(weakTopicsPage.value + 1)
const prevWeakTopicsPage = () => goToWeakTopicsPage(weakTopicsPage.value - 1)

const goToRecentQuizzesPage = (page: number) => {
  recentQuizzesPage.value = clampPage(page, recentQuizzesTotalPages.value)
}
const nextRecentQuizzesPage = () => goToRecentQuizzesPage(recentQuizzesPage.value + 1)
const prevRecentQuizzesPage = () => goToRecentQuizzesPage(recentQuizzesPage.value - 1)

const quickActions = [
  { title: 'Ask AI Tutor', caption: 'Get a guided explanation', to: '/dashboard/ai-tutor', iconClass: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-100', icon: 'M12 4a7 7 0 0 0-7 7v2a4 4 0 0 0 4 4h1l2 3 2-3h1a4 4 0 0 0 4-4v-2a7 7 0 0 0-7-7Z' },
  { title: 'Upload Document', caption: 'Prepare notes for RAG', to: '/dashboard/document-lab', iconClass: 'border-blue-300/25 bg-blue-300/10 text-blue-100', icon: 'M12 16V4m0 0 5 5m-5-5-5 5M4 16v3h16v-3' },
  { title: 'Generate Quiz', caption: 'Practice weak topics', to: '/dashboard/quiz-arena', iconClass: 'border-violet-300/25 bg-violet-300/10 text-violet-100', icon: 'M12 3 4 7v6c0 5 8 8 8s8-3 8-8V7l-8-4Zm-2 8h4M10 15h4' },
  { title: 'Create Study Plan', caption: 'Build a new roadmap', to: '/dashboard/smart-plan', iconClass: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-100', icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01' },
]

const loadProfileName = async () => {
  try {
    const profile = await getProfile()
    profileName.value = cleanDisplayName(profile?.name)
  } catch {
    profileName.value = ''
  }
}

const resetPagination = () => {
  weakTopicsPage.value = 1
  recentQuizzesPage.value = 1
}

onMounted(async () => {
  isDashboardLoading.value = true
  const profilePromise = loadProfileName()
  try {
    dashboard.value = await getDashboardAnalytics()
    dashboardApiNotice.value = 'Analytics loaded from backend'
    resetPagination()
  } catch (error: any) {
    dashboardApiNotice.value = error.apiMessage ?? 'Analytics currently unavailable'
  } finally {
    isDashboardLoading.value = false
    await profilePromise
  }
})
</script>

<style scoped>
.pagination-button {
  min-height: 2.25rem;
  border-radius: 0.75rem;
  border: 1px solid rgb(255 255 255 / 0.1);
  background: rgb(255 255 255 / 0.05);
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: rgb(203 213 225);
  transition: background-color 160ms ease, opacity 160ms ease;
}

.pagination-button:hover:not(:disabled) {
  background: rgb(255 255 255 / 0.1);
}

.pagination-button:disabled {
  cursor: not-allowed;
  opacity: 0.4;
}

.pagination-number {
  height: 2.25rem;
  min-width: 2.25rem;
  border-radius: 0.75rem;
  border: 1px solid rgb(255 255 255 / 0.1);
  background: rgb(255 255 255 / 0.05);
  padding: 0 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: rgb(203 213 225);
  transition: background-color 160ms ease, border-color 160ms ease, color 160ms ease;
}

.pagination-number:hover {
  background: rgb(255 255 255 / 0.1);
}

.pagination-number-active {
  border-color: rgb(103 232 249 / 0.35);
  background: rgb(103 232 249 / 0.15);
  color: rgb(207 250 254);
}
</style>