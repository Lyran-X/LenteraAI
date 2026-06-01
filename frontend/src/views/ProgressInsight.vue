<template>
  <div class="w-full min-w-0 space-y-5 overflow-x-hidden xl:space-y-6">
    <div v-if="isLoading" class="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm font-medium text-cyan-100">
      Loading analytics from EduPath AI...
    </div>
    <div v-else-if="errorMessage" class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100">
      {{ errorMessage }}
    </div>

    <section class="grid min-w-0 gap-4 sm:grid-cols-2 2xl:grid-cols-4">
      <GlassCard v-for="item in summaryCards" :key="item.label" padding="p-4 sm:p-5" extra-class="min-w-0">
        <div class="flex items-start justify-between gap-4">
          <div class="min-w-0">
            <p class="text-sm font-medium text-slate-400">{{ item.label }}</p>
            <p class="mt-2 text-2xl font-semibold text-white sm:text-3xl">{{ item.value }}</p>
          </div>
          <span :class="['shrink-0 rounded-full border px-3 py-1 text-xs font-semibold', item.badgeClass]">{{ item.trend }}</span>
        </div>
        <p class="mt-4 text-sm leading-6 text-slate-500">{{ item.caption }}</p>
      </GlassCard>
    </section>

    <section class="grid min-w-0 grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1.25fr)_minmax(20rem,0.75fr)] xl:gap-6">
      <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0 overflow-hidden">
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div class="min-w-0">
            <p class="text-sm font-medium text-cyan-200/80">Score trend</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Quiz performance over time</h2>
          </div>
          <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-xs font-semibold text-slate-300">{{ scoreTrend.length }} days</span>
        </div>

        <div v-if="scoreTrend.length === 0" class="mt-6 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
          No quiz trend data yet.
        </div>
        <div v-else class="mt-6 min-w-0 rounded-3xl border border-white/8 bg-slate-950/30 p-4 sm:p-5">
          <div class="relative min-w-0 overflow-hidden rounded-2xl bg-gradient-to-br from-cyan-300/[0.07] via-blue-500/[0.04] to-violet-500/[0.07] p-2">
            <svg class="h-72 w-full overflow-visible" :viewBox="chartViewBox" role="img" aria-label="Quiz score trend line chart">
              <defs>
                <linearGradient id="scoreLineGradient" x1="0" x2="1" y1="0" y2="0">
                  <stop offset="0%" stop-color="#67e8f9" />
                  <stop offset="55%" stop-color="#3b82f6" />
                  <stop offset="100%" stop-color="#a78bfa" />
                </linearGradient>
                <linearGradient id="scoreAreaGradient" x1="0" x2="0" y1="0" y2="1">
                  <stop offset="0%" stop-color="#67e8f9" stop-opacity="0.28" />
                  <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0.02" />
                </linearGradient>
              </defs>

              <g v-for="line in yAxisLines" :key="line.label">
                <line :x1="chartPlot.left" :x2="chartPlot.right" :y1="line.y" :y2="line.y" stroke="rgba(148, 163, 184, 0.14)" stroke-width="1" />
                <text :x="chartPlot.left - 12" :y="line.y + 4" text-anchor="end" class="fill-slate-500 text-[11px]">{{ line.label }}</text>
              </g>

              <path v-if="chartAreaPath" :d="chartAreaPath" fill="url(#scoreAreaGradient)" />
              <path :d="chartLinePath" fill="none" stroke="url(#scoreLineGradient)" stroke-linecap="round" stroke-linejoin="round" stroke-width="4" />

              <g v-for="point in chartPoints" :key="point.id">
                <line :x1="point.x" :x2="point.x" :y1="chartPlot.bottom" :y2="point.y" stroke="rgba(103, 232, 249, 0.08)" stroke-width="1" />
                <circle :cx="point.x" :cy="point.y" r="7" fill="#020617" stroke="#67e8f9" stroke-width="3" />
                <circle :cx="point.x" :cy="point.y" r="3" fill="#a78bfa" />
                <text :x="point.x" :y="point.y - 14" text-anchor="middle" class="fill-cyan-100 text-[11px] font-semibold">{{ point.score }}%</text>
                <text :x="point.x" :y="chartPlot.bottom + 24" text-anchor="middle" class="fill-slate-400 text-[11px]">{{ point.day }}</text>
                <text :x="point.x" :y="chartPlot.bottom + 39" text-anchor="middle" class="fill-slate-600 text-[10px]">{{ point.attempts }} attempts</text>
              </g>
            </svg>
          </div>
        </div>
      </GlassCard>

      <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
        <p class="text-sm font-medium text-violet-200/80">AI Insight</p>
        <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Performance summary</h2>
        <p class="mt-4 text-sm leading-6 text-slate-300">{{ aiInsight.summary }}</p>

        <div class="mt-5 rounded-2xl border border-cyan-300/16 bg-cyan-300/8 p-4">
          <p class="text-sm font-semibold text-white">Next best step</p>
          <p class="mt-2 text-sm leading-6 text-slate-400">{{ aiInsight.nextStep }}</p>
        </div>

        <div class="mt-5 flex flex-wrap gap-2">
          <span v-for="tag in aiInsight.tags" :key="tag" class="rounded-full border border-white/10 bg-white/[0.06] px-3 py-1 text-xs font-medium text-slate-300">{{ tag }}</span>
        </div>
      </GlassCard>
    </section>

    <section class="grid min-w-0 grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1fr)_minmax(20rem,0.9fr)] xl:gap-6">
      <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
        <div class="flex items-center justify-between gap-4">
          <div class="min-w-0">
            <p class="text-sm font-medium text-blue-200/80">Topic mastery</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Mastery by topic</h2>
          </div>
          <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs text-slate-400">{{ topicMastery.length }} topics</span>
        </div>

        <div v-if="topicMastery.length === 0" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
          Topic mastery appears after submitted quiz answers.
        </div>
        <div v-else class="mt-5 space-y-4">
          <article v-for="topic in paginatedTopicMastery" :key="topic.name" class="min-w-0 rounded-2xl border border-white/8 bg-white/[0.045] p-4">
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <p class="break-words font-semibold text-white">{{ topic.name }}</p>
                <p class="mt-1 text-sm text-slate-500">{{ topic.activity }}</p>
              </div>
              <span :class="['shrink-0 rounded-full px-3 py-1 text-xs font-semibold', getStatusClass(topic.status)]">{{ topic.status }}</span>
            </div>
            <div class="mt-4 flex items-center gap-3">
              <div class="h-2 min-w-0 flex-1 rounded-full bg-slate-800">
                <div class="h-2 rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500 transition-all duration-300" :style="{ width: `${topic.score}%` }" />
              </div>
              <span class="w-10 text-right text-sm font-semibold text-white">{{ topic.score }}%</span>
            </div>
          </article>

          <div v-if="topicTotalPages > 1" class="flex flex-wrap items-center justify-center gap-2 pt-2">
            <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="topicPage === 1" @click="prevTopicPage">
              Previous
            </button>
            <button
              v-for="page in visibleTopicPages"
              :key="page"
              class="h-9 min-w-9 rounded-xl border px-3 text-xs font-semibold transition"
              :class="topicPage === page ? 'border-cyan-300/30 bg-cyan-300/15 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/10'"
              type="button"
              @click="goToTopicPage(page)"
            >
              {{ page }}
            </button>
            <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="topicPage === topicTotalPages" @click="nextTopicPage">
              Next
            </button>
          </div>
        </div>
      </GlassCard>

      <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
        <div class="flex items-center justify-between gap-4">
          <div class="min-w-0">
            <p class="text-sm font-medium text-amber-200/80">Weakness map</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Highest risk topics</h2>
          </div>
          <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs text-slate-400">{{ weaknessMap.length }} topics</span>
        </div>

        <div v-if="weaknessMap.length === 0" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
          No weak topics detected.
        </div>
        <div v-else class="mt-5 space-y-4">
          <article v-for="weakness in paginatedWeakTopics" :key="weakness.topic" class="rounded-2xl border border-amber-300/16 bg-amber-300/[0.055] p-4">
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0">
                <p class="break-words font-semibold text-white">{{ weakness.topic }}</p>
                <p class="mt-2 text-sm leading-6 text-slate-400">{{ weakness.reason }}</p>
              </div>
              <span class="shrink-0 rounded-full bg-amber-300/10 px-3 py-1 text-xs font-semibold text-amber-100">{{ weakness.risk }}%</span>
            </div>
            <p class="mt-3 text-sm font-medium leading-6 text-cyan-100">{{ weakness.action }}</p>
          </article>

          <div v-if="weakTotalPages > 1" class="flex flex-wrap items-center justify-center gap-2 pt-2">
            <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="weakPage === 1" @click="prevWeakPage">
              Previous
            </button>
            <button
              v-for="page in visibleWeakPages"
              :key="page"
              class="h-9 min-w-9 rounded-xl border px-3 text-xs font-semibold transition"
              :class="weakPage === page ? 'border-cyan-300/30 bg-cyan-300/15 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/10'"
              type="button"
              @click="goToWeakPage(page)"
            >
              {{ page }}
            </button>
            <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="weakPage === weakTotalPages" @click="nextWeakPage">
              Next
            </button>
          </div>
        </div>
      </GlassCard>
    </section>

    <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div class="min-w-0">
          <p class="text-sm font-medium text-cyan-200/80">Recent quiz performance</p>
          <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Latest attempts</h2>
        </div>
        <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-xs text-slate-400">{{ recentQuizzes.length }} attempts</span>
      </div>

      <div v-if="recentQuizzes.length === 0" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center text-sm text-slate-400">
        No recent quiz attempts yet.
      </div>
      <div v-else class="mt-5 space-y-4">
        <div class="overflow-x-auto">
          <table class="w-full min-w-[720px] border-separate border-spacing-y-2 text-left text-sm">
            <thead class="text-xs uppercase tracking-[0.14em] text-slate-500">
              <tr>
                <th class="px-4 py-2 font-semibold">Topic</th>
                <th class="px-4 py-2 font-semibold">Score</th>
                <th class="px-4 py-2 font-semibold">Difficulty</th>
                <th class="px-4 py-2 font-semibold">Date</th>
                <th class="px-4 py-2 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="quiz in paginatedRecentQuizzes" :key="quiz.id" class="rounded-2xl bg-white/[0.045] text-slate-300">
                <td class="rounded-l-2xl px-4 py-3 font-medium text-white">{{ quiz.topic }}</td>
                <td class="px-4 py-3">{{ quiz.score }}%</td>
                <td class="px-4 py-3 capitalize">{{ quiz.difficulty }}</td>
                <td class="px-4 py-3">{{ quiz.date }}</td>
                <td class="rounded-r-2xl px-4 py-3">
                  <span :class="['rounded-full px-3 py-1 text-xs font-semibold', quiz.score >= 80 ? 'bg-emerald-300/10 text-emerald-100' : 'bg-amber-300/10 text-amber-100']">{{ quiz.score >= 80 ? 'On track' : 'Review' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="recentQuizTotalPages > 1" class="flex flex-wrap items-center justify-center gap-2 pt-1">
          <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="recentQuizPage === 1" @click="prevRecentQuizPage">
            Previous
          </button>
          <button
            v-for="page in visibleRecentQuizPages"
            :key="page"
            class="h-9 min-w-9 rounded-xl border px-3 text-xs font-semibold transition"
            :class="recentQuizPage === page ? 'border-cyan-300/30 bg-cyan-300/15 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/10'"
            type="button"
            @click="goToRecentQuizPage(page)"
          >
            {{ page }}
          </button>
          <button class="rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40" type="button" :disabled="recentQuizPage === recentQuizTotalPages" @click="nextRecentQuizPage">
            Next
          </button>
        </div>
      </div>
    </GlassCard>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

import GlassCard from '../components/GlassCard.vue'
import { getRecentQuizzes, getScoreTrend, getSummary, getTopicMastery, getWeakTopics } from '../services/analyticsService'

type MasteryStatus = 'Strong' | 'Moderate' | 'Weak'

const TOPIC_PAGE_SIZE = 6
const WEAK_PAGE_SIZE = 5
const RECENT_QUIZ_PAGE_SIZE = 5
const CHART_WIDTH = 640
const CHART_HEIGHT = 280
const chartPlot = { left: 44, right: 612, top: 24, bottom: 226 }

const summary = ref<any | null>(null)
const rawScoreTrend = ref<any[]>([])
const rawTopicMastery = ref<any[]>([])
const rawWeakTopics = ref<any[]>([])
const rawRecentQuizzes = ref<any[]>([])
const topicPage = ref(1)
const weakPage = ref(1)
const recentQuizPage = ref(1)
const isLoading = ref(false)
const errorMessage = ref('')

const percent = (value: unknown) => `${Math.round(Number(value ?? 0))}%`
const clampScore = (value: unknown) => Math.min(100, Math.max(0, Math.round(Number(value ?? 0))))
const formatDate = (value?: string) => {
  if (!value) return 'Recent'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return 'Recent'
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(parsed)
}
const statusFor = (score: number): MasteryStatus => (score >= 80 ? 'Strong' : score >= 70 ? 'Moderate' : 'Weak')
const paginate = <T,>(items: T[], page: number, pageSize: number) => items.slice((page - 1) * pageSize, page * pageSize)
const totalPagesFor = (items: unknown[], pageSize: number) => Math.max(1, Math.ceil(items.length / pageSize))
const clampPage = (page: number, totalPages: number) => Math.min(Math.max(page, 1), Math.max(totalPages, 1))
const pageNumbers = (currentPage: number, totalPages: number) => {
  if (totalPages <= 5) return Array.from({ length: totalPages }, (_, index) => index + 1)
  const start = Math.max(1, Math.min(currentPage - 2, totalPages - 4))
  return Array.from({ length: 5 }, (_, index) => start + index)
}

const summaryCards = computed(() => [
  { label: 'Average Score', value: percent(summary.value?.average_score), trend: `${summary.value?.total_attempts ?? 0} attempts`, caption: 'Across submitted quiz attempts.', badgeClass: 'border-emerald-300/20 bg-emerald-300/10 text-emerald-100' },
  { label: 'Study Streak', value: `${summary.value?.study_streak ?? 0}d`, trend: 'current', caption: 'Consecutive days with learning activity.', badgeClass: 'border-cyan-300/20 bg-cyan-300/10 text-cyan-100' },
  { label: 'Completed Plans', value: String(summary.value?.completed_study_plans ?? 0), trend: `${summary.value?.active_study_plans ?? 0} active`, caption: 'Study plans completed or fully checked off.', badgeClass: 'border-violet-300/20 bg-violet-300/10 text-violet-100' },
  { label: 'Retention Score', value: percent(summary.value?.retention_score), trend: 'rule-based', caption: 'Estimated from score and streak.', badgeClass: 'border-blue-300/20 bg-blue-300/10 text-blue-100' },
])

const scoreTrend = computed(() => rawScoreTrend.value.map((point, index) => ({
  id: `${point.date ?? 'trend'}-${index}`,
  day: formatDate(point.date),
  score: clampScore(point.average_score ?? point.score),
  attempts: Number(point.attempts ?? point.total_attempts ?? 0),
})))

const topicMastery = computed(() => rawTopicMastery.value.map((topic) => ({
  name: topic.topic ?? 'Untitled topic',
  score: clampScore(topic.accuracy ?? topic.score),
  status: statusFor(Number(topic.accuracy ?? topic.score ?? 0)),
  activity: `${topic.correct ?? 0}/${topic.total ?? 0} correct answers`,
})))

const weaknessMap = computed(() => rawWeakTopics.value.map((weakness) => ({
  topic: weakness.topic ?? 'Untitled topic',
  risk: clampScore(100 - Number(weakness.accuracy ?? 0)),
  reason: `Accuracy is ${clampScore(weakness.accuracy)}%.`,
  action: weakness.recommendation ?? 'Review this topic with AI Tutor and retry a focused quiz.',
})))

const recentQuizzes = computed(() => rawRecentQuizzes.value.map((quiz, index) => ({
  id: quiz.attempt_id ?? quiz.id ?? `${quiz.quiz_id ?? 'quiz'}-${index}`,
  topic: quiz.topic ?? quiz.quiz_title ?? 'Quiz attempt',
  score: clampScore(quiz.score),
  difficulty: quiz.difficulty ?? 'medium',
  date: formatDate(quiz.submitted_at ?? quiz.created_at),
})))

const chartViewBox = computed(() => `0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`)
const yAxisLines = computed(() => [0, 25, 50, 75, 100].map((value) => {
  const usableHeight = chartPlot.bottom - chartPlot.top
  const y = chartPlot.bottom - (value / 100) * usableHeight
  return { label: String(value), y }
}))
const chartPoints = computed(() => {
  const points = scoreTrend.value
  const usableWidth = chartPlot.right - chartPlot.left
  const usableHeight = chartPlot.bottom - chartPlot.top
  const lastIndex = Math.max(points.length - 1, 1)
  return points.map((point, index) => ({
    ...point,
    x: points.length === 1 ? chartPlot.left + usableWidth / 2 : chartPlot.left + (index / lastIndex) * usableWidth,
    y: chartPlot.bottom - (point.score / 100) * usableHeight,
  }))
})
const chartLinePath = computed(() => chartPoints.value.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' '))
const chartAreaPath = computed(() => {
  if (chartPoints.value.length < 2) return ''
  const line = chartPoints.value.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ')
  const first = chartPoints.value[0]
  const last = chartPoints.value[chartPoints.value.length - 1]
  return `${line} L ${last.x} ${chartPlot.bottom} L ${first.x} ${chartPlot.bottom} Z`
})

const topicTotalPages = computed(() => totalPagesFor(topicMastery.value, TOPIC_PAGE_SIZE))
const weakTotalPages = computed(() => totalPagesFor(weaknessMap.value, WEAK_PAGE_SIZE))
const recentQuizTotalPages = computed(() => totalPagesFor(recentQuizzes.value, RECENT_QUIZ_PAGE_SIZE))
const paginatedTopicMastery = computed(() => paginate(topicMastery.value, topicPage.value, TOPIC_PAGE_SIZE))
const paginatedWeakTopics = computed(() => paginate(weaknessMap.value, weakPage.value, WEAK_PAGE_SIZE))
const paginatedRecentQuizzes = computed(() => paginate(recentQuizzes.value, recentQuizPage.value, RECENT_QUIZ_PAGE_SIZE))
const visibleTopicPages = computed(() => pageNumbers(topicPage.value, topicTotalPages.value))
const visibleWeakPages = computed(() => pageNumbers(weakPage.value, weakTotalPages.value))
const visibleRecentQuizPages = computed(() => pageNumbers(recentQuizPage.value, recentQuizTotalPages.value))

const aiInsight = computed(() => {
  if ((summary.value?.total_attempts ?? 0) === 0) {
    return { summary: 'No quiz attempts yet. EduPath will generate stronger analytics after your first submitted quiz.', nextStep: 'Generate a short quiz from Quiz Arena.', tags: ['First quiz', 'Baseline'] }
  }
  if (weaknessMap.value.length > 0) {
    return { summary: `Your weakest topic is ${weaknessMap.value[0].topic}.`, nextStep: weaknessMap.value[0].action, tags: ['Weak topic', 'AI Tutor', 'Focused quiz'] }
  }
  return { summary: 'Your quiz performance is stable across available topics.', nextStep: 'Keep alternating study plan tasks and focused quizzes.', tags: ['Momentum', 'Review', 'Practice'] }
})

const getStatusClass = (status: MasteryStatus) => {
  const classes: Record<MasteryStatus, string> = {
    Strong: 'bg-emerald-300/10 text-emerald-100',
    Moderate: 'bg-cyan-300/10 text-cyan-100',
    Weak: 'bg-amber-300/10 text-amber-100',
  }
  return classes[status]
}

const goToTopicPage = (page: number) => {
  topicPage.value = clampPage(page, topicTotalPages.value)
}
const nextTopicPage = () => goToTopicPage(topicPage.value + 1)
const prevTopicPage = () => goToTopicPage(topicPage.value - 1)

const goToWeakPage = (page: number) => {
  weakPage.value = clampPage(page, weakTotalPages.value)
}
const nextWeakPage = () => goToWeakPage(weakPage.value + 1)
const prevWeakPage = () => goToWeakPage(weakPage.value - 1)

const goToRecentQuizPage = (page: number) => {
  recentQuizPage.value = clampPage(page, recentQuizTotalPages.value)
}
const nextRecentQuizPage = () => goToRecentQuizPage(recentQuizPage.value + 1)
const prevRecentQuizPage = () => goToRecentQuizPage(recentQuizPage.value - 1)

const resetPagination = () => {
  topicPage.value = 1
  weakPage.value = 1
  recentQuizPage.value = 1
}

const loadAnalytics = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const [summaryData, trendData, masteryData, weakData, recentData] = await Promise.all([
      getSummary(),
      getScoreTrend(),
      getTopicMastery(),
      getWeakTopics(),
      getRecentQuizzes(),
    ])
    summary.value = summaryData
    rawScoreTrend.value = Array.isArray(trendData) ? trendData : []
    rawTopicMastery.value = Array.isArray(masteryData) ? masteryData : []
    rawWeakTopics.value = Array.isArray(weakData) ? weakData : []
    rawRecentQuizzes.value = Array.isArray(recentData) ? recentData : []
    resetPagination()
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to load learning analytics.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadAnalytics)
</script>