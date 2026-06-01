<template>
  <header class="sticky top-0 z-30 w-full min-w-0 border-b border-white/7 bg-slate-950/55 px-4 py-3 backdrop-blur-2xl sm:px-6 xl:px-8">
    <div class="mx-auto flex w-full max-w-[1440px] min-w-0 flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div class="min-w-0">
        <p class="text-xs font-medium text-cyan-200/80">{{ route.meta.eyebrow }}</p>
        <h1 class="mt-1 truncate text-xl font-semibold tracking-normal text-white sm:text-2xl">
          {{ route.meta.title }}
        </h1>
      </div>

      <div class="flex min-w-0 flex-wrap items-center gap-2 sm:gap-3 lg:flex-nowrap">
        <div ref="searchContainer" class="relative min-w-[13rem] flex-1 sm:min-w-[18rem] lg:w-[24rem] lg:flex-none xl:w-[28rem]">
          <label class="flex min-w-0 items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] px-3 py-2.5 text-sm text-slate-400 transition focus-within:border-cyan-300/35 focus-within:bg-white/[0.08]">
            <svg class="h-4 w-4 shrink-0 text-slate-500" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="m21 21-4.3-4.3M11 18a7 7 0 1 1 0-14 7 7 0 0 1 0 14Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
            </svg>
            <input
              v-model="searchQuery"
              class="min-w-0 flex-1 bg-transparent text-slate-200 placeholder:text-slate-500 focus:outline-none"
              placeholder="Search lessons, notes, quizzes"
              type="search"
              @focus="openSearchDropdown"
              @keydown.enter.prevent="navigateFirstSearchResult"
              @keydown.escape.prevent="closeSearchDropdown"
            />
          </label>

          <div
            v-if="showSearchDropdown"
            class="absolute left-0 right-0 top-full z-50 mt-2 max-h-[22rem] overflow-hidden rounded-2xl border border-white/10 bg-slate-950/95 p-2 shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl"
          >
            <div v-if="searchResults.length > 0" class="thin-scrollbar max-h-[20rem] space-y-1 overflow-y-auto">
              <button
                v-for="item in searchResults"
                :key="item.title"
                class="flex w-full min-w-0 items-start gap-3 rounded-xl px-3 py-3 text-left transition hover:bg-cyan-300/10"
                type="button"
                @click="navigateToSearchResult(item)"
              >
                <span :class="['flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border', item.iconClass]">
                  <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path :d="item.icon" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </span>
                <span class="min-w-0">
                  <span class="block truncate text-sm font-semibold text-white">{{ item.title }}</span>
                  <span class="mt-0.5 block line-clamp-2 text-xs leading-5 text-slate-400">{{ item.description }}</span>
                </span>
              </button>
            </div>

            <div v-else class="rounded-xl border border-dashed border-white/12 bg-white/[0.035] px-4 py-5 text-center">
              <p class="text-sm font-semibold text-white">No results found</p>
              <p class="mt-1 text-xs leading-5 text-slate-500">Try searching AI Tutor, Quiz, Notes, or Document.</p>
            </div>
          </div>
        </div>

        <div ref="notificationContainer" class="relative shrink-0">
          <button
            class="relative flex h-10 w-10 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.06] text-slate-300 transition hover:bg-white/10"
            type="button"
            aria-label="Notifications"
            @click="toggleNotifications"
            @keydown.escape.prevent="closeNotifications"
          >
            <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <span v-if="unreadCount > 0" class="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full border border-slate-950 bg-rose-500 px-1 text-[10px] font-bold text-white">
              {{ unreadCount }}
            </span>
          </button>

          <Transition
            enter-active-class="transition duration-150 ease-out"
            enter-from-class="translate-y-1 scale-[0.98] opacity-0"
            enter-to-class="translate-y-0 scale-100 opacity-100"
            leave-active-class="transition duration-150 ease-in"
            leave-from-class="translate-y-0 scale-100 opacity-100"
            leave-to-class="translate-y-1 scale-[0.98] opacity-0"
          >
            <div
              v-if="showNotifications"
              class="absolute right-0 top-full z-50 mt-3 w-[min(24rem,calc(100vw-2rem))] overflow-hidden rounded-[24px] border border-white/10 bg-slate-950/95 p-4 shadow-2xl shadow-cyan-950/30 backdrop-blur-xl"
            >
              <div class="flex items-start justify-between gap-4 pb-4">
                <div class="min-w-0">
                  <p class="text-base font-semibold text-white">Notifications</p>
                  <p class="mt-1 text-xs text-slate-400">{{ unreadCount }} unread</p>
                </div>
                <button
                  v-if="unreadCount > 0"
                  class="shrink-0 rounded-full border border-white/10 bg-white/[0.05] px-3 py-1.5 text-xs font-semibold text-slate-200 transition hover:bg-white/10"
                  type="button"
                  @click="markAllNotificationsRead"
                >
                  Mark all read
                </button>
              </div>

              <div v-if="notifications.length === 0" class="rounded-2xl border border-dashed border-white/12 bg-white/[0.035] px-4 py-6 text-center">
                <div class="mx-auto flex h-11 w-11 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
                  <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9ZM10 21h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </div>
                <p class="mt-3 text-sm font-semibold text-white">No notifications</p>
                <p class="mt-1 text-xs text-slate-500">You're all caught up.</p>
              </div>
              <div v-else class="thin-scrollbar max-h-80 space-y-2 overflow-y-auto pr-1">
                <button
                  v-for="notification in notifications"
                  :key="notification.id"
                  class="w-full rounded-2xl border p-4 text-left transition duration-150 hover:border-cyan-300/25 hover:bg-white/[0.08]"
                  :class="notification.is_read ? 'border-white/8 bg-white/[0.03]' : 'border-cyan-300/20 bg-cyan-400/[0.08]'"
                  type="button"
                  @click="openNotification(notification)"
                >
                  <div class="flex items-start gap-3">
                    <span
                      class="mt-1.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-xl border"
                      :class="notification.is_read ? 'border-white/10 bg-white/[0.04] text-slate-500' : 'border-cyan-300/25 bg-cyan-300/10 text-cyan-100'"
                    >
                      <span class="h-2 w-2 rounded-full" :class="notification.is_read ? 'bg-slate-600' : 'bg-rose-400'" />
                    </span>
                    <span class="min-w-0 flex-1">
                      <span class="flex items-start justify-between gap-3">
                        <span class="block text-sm font-semibold text-white">{{ notification.title }}</span>
                        <span v-if="!notification.is_read" class="mt-1 h-2 w-2 shrink-0 rounded-full bg-rose-400 shadow-[0_0_10px_rgba(251,113,133,0.6)]" />
                      </span>
                      <span class="mt-1.5 block text-sm leading-relaxed text-slate-300/80">{{ notification.message }}</span>
                      <span class="mt-3 block text-xs text-slate-500">{{ formatNotificationTime(notification.created_at) }}</span>
                    </span>
                  </div>
                </button>
              </div>
            </div>
          </Transition>
        </div>

        <div class="hidden shrink-0 items-center gap-2 rounded-2xl border border-white/10 bg-white/[0.06] px-2.5 py-2 sm:flex">
          <div class="flex h-8 w-8 items-center justify-center overflow-hidden rounded-xl bg-gradient-to-br from-cyan-300 to-violet-400 text-xs font-bold text-white">
            <img v-if="showAvatarImage" :src="avatarImageUrl" alt="Profile avatar" class="h-full w-full object-cover" @error="handleAvatarError" />
            <span v-else>{{ userInitial }}</span>
          </div>
          <div class="hidden min-w-0 text-left lg:block">
            <p class="max-w-32 truncate text-sm font-semibold text-white">{{ displayName }}</p>
            <p class="text-xs text-slate-400">{{ displayRole }}</p>
          </div>
        </div>

        <button
          class="shrink-0 rounded-2xl border border-white/10 bg-white/[0.06] px-3 py-2.5 text-xs font-semibold text-slate-200 transition hover:bg-white/10 hover:text-white sm:px-4"
          type="button"
          @click="emit('logout')"
        >
          Logout
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/authStore'
import { getAssetUrl, getProfile } from '@/services/profileService'

type SearchItem = {
  title: string
  description: string
  route: string
  keywords: string[]
  icon: string
  iconClass: string
}

type AppNotification = {
  id: string
  title: string
  message: string
  type: string
  is_read: boolean
  created_at: string
  route?: string
}

const emit = defineEmits<{ logout: [] }>()
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const NOTIFICATION_STORAGE_KEY = 'edupath_notifications'

const searchContainer = ref<HTMLElement | null>(null)
const notificationContainer = ref<HTMLElement | null>(null)
const searchQuery = ref('')
const isSearchFocused = ref(false)
const showNotifications = ref(false)
const notifications = ref<AppNotification[]>([])
const profileUser = ref<Record<string, any> | null>(authStore.user)
const avatarLoadFailed = ref(false)

const searchableItems: SearchItem[] = [
  { title: 'Dashboard Overview', description: 'View learning analytics and next actions', route: '/dashboard', keywords: ['dashboard', 'overview', 'home', 'analytics'], iconClass: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-100', icon: 'M4 13h6V4H4v9Zm10 7h6V4h-6v16ZM4 20h6v-5H4v5Z' },
  { title: 'AI Tutor', description: 'Ask questions and get guided explanations', route: '/dashboard/ai-tutor', keywords: ['chat', 'tutor', 'ask', 'explain', 'learning'], iconClass: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-100', icon: 'M12 4a7 7 0 0 0-7 7v2a4 4 0 0 0 4 4h1l2 3 2-3h1a4 4 0 0 0 4-4v-2a7 7 0 0 0-7-7Z' },
  { title: 'Document Lab', description: 'Upload documents and ask questions with sources', route: '/dashboard/document-lab', keywords: ['document', 'upload', 'rag', 'pdf', 'docx', 'ask'], iconClass: 'border-blue-300/25 bg-blue-300/10 text-blue-100', icon: 'M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9l-6-6Zm0 0v6h6' },
  { title: 'Smart Plan', description: 'Generate and complete study quests', route: '/dashboard/smart-plan', keywords: ['study', 'plan', 'roadmap', 'quest', 'schedule'], iconClass: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-100', icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01' },
  { title: 'Quiz Arena', description: 'Generate quizzes and review answers', route: '/dashboard/quiz-arena', keywords: ['quiz', 'practice', 'test', 'question', 'exam'], iconClass: 'border-violet-300/25 bg-violet-300/10 text-violet-100', icon: 'M12 3 4 7v6c0 5 8 8 8 8s8-3 8-8V7l-8-4Zm-2 8h4M10 15h4' },
  { title: 'Progress Insight', description: 'Track score trends and weak topics', route: '/dashboard/progress', keywords: ['progress', 'analytics', 'trend', 'weak', 'mastery'], iconClass: 'border-amber-300/25 bg-amber-300/10 text-amber-100', icon: 'M4 19V5m0 14h16M8 16v-4m4 4V8m4 8v-6' },
  { title: 'Saved Notes', description: 'Open your saved knowledge vault', route: '/dashboard/notes', keywords: ['notes', 'saved', 'vault', 'bookmark'], iconClass: 'border-violet-300/25 bg-violet-300/10 text-violet-100', icon: 'M6 4h9l3 3v13H6V4Zm8 0v4h4M9 12h6M9 16h6' },
  { title: 'Profile Settings', description: 'Manage profile, avatar, and tutor preferences', route: '/dashboard/settings', keywords: ['profile', 'settings', 'account', 'avatar', 'password'], iconClass: 'border-slate-300/25 bg-slate-300/10 text-slate-100', icon: 'M20 21a8 8 0 0 0-16 0M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z' },
  { title: 'Upload Document', description: 'Go to Document Lab and upload learning files', route: '/dashboard/document-lab', keywords: ['upload', 'file', 'pdf', 'document', 'pptx'], iconClass: 'border-blue-300/25 bg-blue-300/10 text-blue-100', icon: 'M12 16V4m0 0 5 5m-5-5-5 5M4 16v3h16v-3' },
  { title: 'Generate Quiz', description: 'Create a quiz from topic or document', route: '/dashboard/quiz-arena', keywords: ['generate', 'quiz', 'practice', 'question'], iconClass: 'border-violet-300/25 bg-violet-300/10 text-violet-100', icon: 'M12 3 4 7v6c0 5 8 8 8 8s8-3 8-8V7l-8-4Zm-2 8h4M10 15h4' },
  { title: 'Create Study Plan', description: 'Build a personalized learning roadmap', route: '/dashboard/smart-plan', keywords: ['create', 'study', 'plan', 'roadmap'], iconClass: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-100', icon: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01' },
  { title: 'Review Weak Topics', description: 'Open analytics and review topics that need attention', route: '/dashboard/progress', keywords: ['review', 'weak', 'topics', 'progress', 'analytics'], iconClass: 'border-amber-300/25 bg-amber-300/10 text-amber-100', icon: 'M12 9v4m0 4h.01M10.3 4.3 2 19h20L13.7 4.3a2 2 0 0 0-3.4 0Z' },
]

const normalizedSearchQuery = computed(() => searchQuery.value.trim().toLowerCase())
const searchResults = computed(() => {
  const query = normalizedSearchQuery.value
  if (!query) return []

  return searchableItems
    .filter((item) => {
      const haystack = [item.title, item.description, ...item.keywords].join(' ').toLowerCase()
      return haystack.includes(query)
    })
    .slice(0, 5)
})
const showSearchDropdown = computed(() => isSearchFocused.value && normalizedSearchQuery.value.length > 0)

const displayName = computed<string>(() => {
  const name = String(profileUser.value?.name ?? authStore.user?.name ?? '').trim()
  const email = String(profileUser.value?.email ?? authStore.user?.email ?? '').trim()
  return name || email || 'User'
})
const displayRole = computed<string>(() => {
  const role = String(profileUser.value?.role ?? authStore.user?.role ?? 'student')
  return `${role.charAt(0).toUpperCase()}${role.slice(1)}`
})
const avatarImageUrl = computed(() => getAssetUrl(profileUser.value?.avatar_url ?? authStore.user?.avatar_url))
const showAvatarImage = computed(() => Boolean(avatarImageUrl.value && !avatarLoadFailed.value))
const userInitial = computed(() => {
  const name = String(profileUser.value?.name ?? authStore.user?.name ?? '').trim()
  const email = String(profileUser.value?.email ?? authStore.user?.email ?? '').trim()
  return (name || email || 'User').charAt(0).toUpperCase() || 'U'
})
const unreadCount = computed(() => notifications.value.filter((notification) => !notification.is_read).length)

watch(avatarImageUrl, () => {
  avatarLoadFailed.value = false
})

const canUseStorage = () => typeof window !== 'undefined' && Boolean(window.localStorage)

const seedNotification = (): AppNotification => ({
  id: 'welcome-dashboard',
  title: 'Welcome to LenteraAI',
  message: 'Your learning dashboard is ready. Start with AI Tutor, Document Lab, or Quiz Arena.',
  type: 'welcome',
  is_read: false,
  created_at: new Date().toISOString(),
  route: '/dashboard/ai-tutor',
})

const saveNotifications = () => {
  if (!canUseStorage()) return
  window.localStorage.setItem(NOTIFICATION_STORAGE_KEY, JSON.stringify(notifications.value))
}

const loadNotifications = () => {
  if (!canUseStorage()) {
    notifications.value = [seedNotification()]
    return
  }

  try {
    const raw = window.localStorage.getItem(NOTIFICATION_STORAGE_KEY)
    if (!raw) {
      notifications.value = [seedNotification()]
      saveNotifications()
      return
    }

    const parsed = JSON.parse(raw)
    notifications.value = Array.isArray(parsed) ? parsed : [seedNotification()]
  } catch {
    notifications.value = [seedNotification()]
    saveNotifications()
  }
}

const fetchProfile = async () => {
  try {
    const profile = await getProfile()
    profileUser.value = profile
    authStore.updateUserProfile?.({
      id: profile.id,
      name: profile.name,
      email: profile.email,
      role: profile.role,
      avatar_url: profile.avatar_url,
    })
  } catch {
    profileUser.value = authStore.user
  }
}

const openSearchDropdown = () => {
  isSearchFocused.value = true
  showNotifications.value = false
}

const closeSearchDropdown = () => {
  isSearchFocused.value = false
}

const navigateToSearchResult = async (item: SearchItem) => {
  await router.push(item.route)
  searchQuery.value = ''
  closeSearchDropdown()
}

const navigateFirstSearchResult = async () => {
  const [firstResult] = searchResults.value
  if (firstResult) {
    await navigateToSearchResult(firstResult)
  }
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  closeSearchDropdown()
}

const closeNotifications = () => {
  showNotifications.value = false
}

const markAllNotificationsRead = () => {
  notifications.value = notifications.value.map((notification) => ({ ...notification, is_read: true }))
  saveNotifications()
}

const openNotification = async (notification: AppNotification) => {
  notifications.value = notifications.value.map((item) => (item.id === notification.id ? { ...item, is_read: true } : item))
  saveNotifications()

  if (notification.route) {
    await router.push(notification.route)
    closeNotifications()
  }
}

const formatNotificationTime = (value: string) => {
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return 'Recently'
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(parsed)
}

const handleAvatarError = () => {
  avatarLoadFailed.value = true
}

const handleDocumentClick = (event: MouseEvent) => {
  const target = event.target as Node
  if (searchContainer.value && !searchContainer.value.contains(target)) {
    closeSearchDropdown()
  }
  if (notificationContainer.value && !notificationContainer.value.contains(target)) {
    closeNotifications()
  }
}

const handleDocumentKeydown = (event: KeyboardEvent) => {
  if (event.key === 'Escape') {
    closeSearchDropdown()
    closeNotifications()
  }
}

onMounted(() => {
  loadNotifications()
  void fetchProfile()
  document.addEventListener('click', handleDocumentClick)
  document.addEventListener('keydown', handleDocumentKeydown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDocumentClick)
  document.removeEventListener('keydown', handleDocumentKeydown)
})
</script>