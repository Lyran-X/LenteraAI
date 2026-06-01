<template>
  <div class="mx-auto w-full max-w-[1440px] min-w-0 overflow-x-hidden">
    <div v-if="pageError" class="mb-4 rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100">
      {{ pageError }}
    </div>

    <div class="grid min-w-0 grid-cols-1 gap-5 xl:h-[calc(100vh-96px)] xl:min-h-[640px] xl:grid-cols-[320px_minmax(0,1fr)] xl:gap-6 xl:overflow-hidden">
      <aside class="order-2 flex min-w-0 flex-col gap-5 xl:order-none xl:h-full xl:min-h-0 xl:overflow-hidden">
        <div class="h-[340px] min-w-0 sm:h-[400px] xl:h-auto xl:flex-[0.95] xl:min-h-0 xl:overflow-hidden">
          <ChatSessionList
            class="h-full min-w-0"
            :active-session-id="activeSessionId"
            :sessions="sessionSummaries"
            @select="selectSession"
          />
        </div>

        <GlassCard padding="p-4 sm:p-5" extra-class="min-w-0 xl:flex-[1.05] xl:min-h-0 xl:overflow-hidden">
          <div class="flex h-full min-h-0 flex-col">
            <div class="flex flex-none items-center justify-between gap-3">
              <div>
                <p class="text-sm font-medium text-violet-200/80">Tutor mode</p>
                <h3 class="mt-1 text-lg font-semibold text-white">Response style</h3>
              </div>
              <span class="rounded-full border border-white/10 px-2.5 py-1 text-xs font-medium text-slate-400">
                5 modes
              </span>
            </div>

            <TutorModeSelector
              class="thin-scrollbar mt-4 min-h-0 xl:flex-1 xl:overflow-y-auto xl:pr-1"
              :modes="tutorModes"
              :selected-mode="selectedMode"
              @select="selectTutorMode"
            />
          </div>
        </GlassCard>
      </aside>

      <div class="order-1 min-w-0 xl:order-none xl:h-full xl:min-h-0 xl:overflow-hidden">
        <GlassCard padding="p-0" extra-class="flex h-[calc(100vh-120px)] min-h-[620px] min-w-0 overflow-hidden xl:h-full xl:min-h-0">
          <section class="flex min-h-0 min-w-0 w-full flex-col">
            <header class="flex-none border-b border-white/8 p-4 sm:p-5">
              <div class="flex min-w-0 flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-2">
                    <span class="h-2.5 w-2.5 shrink-0 rounded-full bg-emerald-300 shadow-lg shadow-emerald-300/50" />
                    <p class="text-sm font-medium text-cyan-200/80">AI Tutor online</p>
                  </div>
                  <h2 class="mt-2 truncate text-xl font-semibold text-white sm:text-2xl">
                    {{ activeSessionTitle }}
                  </h2>
                  <p class="mt-1 truncate text-sm text-slate-400">
                    Current mode: <span class="font-medium text-cyan-100">{{ currentMode.label }}</span>
                  </p>
                </div>

                <div class="flex shrink-0 flex-wrap gap-2">
                  <button
                    class="inline-flex min-h-9 items-center justify-center rounded-xl border border-rose-300/20 bg-rose-300/10 px-3 text-xs font-semibold text-rose-100 transition hover:bg-rose-300/15 disabled:cursor-not-allowed disabled:opacity-50 sm:text-sm"
                    type="button"
                    :disabled="!activeSessionId || isLoading"
                    @click="deleteActiveSession"
                  >
                    Delete Session
                  </button>
                  <button
                    class="inline-flex min-h-9 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-3 text-xs font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50 sm:text-sm"
                    type="button"
                    :disabled="isLoading"
                    @click="startFreshSession"
                  >
                    New Session
                  </button>
                </div>
              </div>
            </header>

            <div ref="messageListRef" class="thin-scrollbar min-h-0 flex-1 overflow-y-auto p-4 sm:p-5 lg:p-6">
              <EmptyState
                v-if="isBooting"
                title="Loading AI Tutor"
                description="Fetching your protected chat sessions from EduPath AI."
              />

              <EmptyState
                v-else-if="activeMessages.length === 0 && loadingSessionId !== activeSessionId"
                title="Start a new learning conversation"
                description="Ask a question to create a protected AI Tutor session for your account."
              />

              <div v-else class="space-y-5">
                <ChatMessage
                  v-for="message in activeMessages"
                  :key="message.id"
                  :message="message"
                  :saved="savedMessageIds.has(message.id)"
                  @save="saveAnswerToNotes"
                />

                <article v-if="loadingSessionId === activeSessionId" class="flex min-w-0 justify-start gap-3">
                  <div class="mt-1 hidden h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-xs font-bold text-cyan-100 sm:flex">
                    AI
                  </div>
                  <div class="max-w-[90%] rounded-3xl rounded-bl-lg border border-white/10 bg-white/[0.065] px-4 py-3 shadow-lg shadow-black/18 sm:max-w-[82%]">
                    <div class="flex items-center gap-2">
                      <span class="h-2 w-2 animate-pulse rounded-full bg-cyan-200" />
                      <span class="h-2 w-2 animate-pulse rounded-full bg-blue-300 [animation-delay:120ms]" />
                      <span class="h-2 w-2 animate-pulse rounded-full bg-violet-300 [animation-delay:240ms]" />
                    </div>
                  </div>
                </article>
              </div>
            </div>

            <div v-if="savedNotice" class="mx-4 mb-3 flex-none rounded-2xl border border-emerald-300/20 bg-emerald-300/10 px-4 py-3 text-sm font-medium text-emerald-100 sm:mx-5">
              {{ savedNotice }}
            </div>

            <ChatInput
              v-model="draftMessage"
              class="flex-none"
              :disabled="isLoading || isBooting"
              :selected-mode-label="currentMode.label"
              placeholder="Ask EduPath AI about your lesson"
              @submit="submitMessage"
            />
          </section>
        </GlassCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import EmptyState from '../components/EmptyState.vue'
import GlassCard from '../components/GlassCard.vue'
import ChatInput from '../components/tutor/ChatInput.vue'
import ChatMessage from '../components/tutor/ChatMessage.vue'
import ChatSessionList from '../components/tutor/ChatSessionList.vue'
import TutorModeSelector from '../components/tutor/TutorModeSelector.vue'
import {
  createSession,
  deleteSession,
  getSession,
  getSessions,
  saveMessageToNote,
  sendMessage,
} from '../services/aiTutorService'

type TutorModeId = 'explain_simply' | 'step_by_step' | 'socratic' | 'give_example' | 'practice_question'
type ChatRole = 'user' | 'assistant'

interface ChatMessageItem {
  id: string
  role: ChatRole
  content: string
  createdAt: string
  modeId?: TutorModeId
  modeLabel?: string
}

interface ChatSession {
  id: string
  title: string
  topic: string
  preview: string
  updatedAt: string
  messagesCount: number
  messages: ChatMessageItem[]
}

const tutorModes = [
  { id: 'explain_simply', label: 'Explain Simply', description: 'Use plain language and short analogies.', dotClass: 'bg-cyan-300' },
  { id: 'step_by_step', label: 'Step-by-Step', description: 'Break the solution into clear ordered steps.', dotClass: 'bg-blue-300' },
  { id: 'socratic', label: 'Socratic Mode', description: 'Guide learning with questions instead of direct answers.', dotClass: 'bg-violet-300' },
  { id: 'give_example', label: 'Give Example', description: 'Answer using a concrete worked example.', dotClass: 'bg-emerald-300' },
  { id: 'practice_question', label: 'Practice Question', description: 'Turn the topic into a quick exercise.', dotClass: 'bg-amber-300' },
] satisfies Array<{ id: TutorModeId; label: string; description: string; dotClass: string }>

const chatSessions = ref<ChatSession[]>([])
const activeSessionId = ref('')
const selectedMode = ref<TutorModeId>('explain_simply')
const draftMessage = ref('')
const loadingSessionId = ref<string | null>(null)
const savedMessageIds = ref(new Set<string>())
const savedNotice = ref('')
const messageListRef = ref<HTMLElement | null>(null)
const isBooting = ref(false)
const pageError = ref('')

let savedNoticeTimer: number | undefined

const activeSession = computed(() => chatSessions.value.find((session) => session.id === activeSessionId.value))
const activeSessionTitle = computed(() => activeSession.value?.title ?? 'AI Tutor')
const activeMessages = computed(() => activeSession.value?.messages ?? [])
const isLoading = computed(() => loadingSessionId.value !== null)
const currentMode = computed(() => tutorModes.find((mode) => mode.id === selectedMode.value) ?? tutorModes[0])
const sessionSummaries = computed(() => chatSessions.value.map(({ messages, ...session }) => session))

const modeLabel = (modeId?: string) => tutorModes.find((mode) => mode.id === modeId)?.label ?? 'AI Tutor'
const formatDateTime = (value?: string) => {
  if (!value) return 'Now'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return 'Now'
  return new Intl.DateTimeFormat('en', { hour: '2-digit', minute: '2-digit', hour12: false }).format(parsed)
}

const lastMessagePreview = (messages: ChatMessageItem[]) => messages[messages.length - 1]?.content ?? 'No messages yet'

const mapMessage = (message: any, fallbackMode?: TutorModeId): ChatMessageItem => ({
  id: String(message.id),
  role: message.role === 'assistant' ? 'assistant' : 'user',
  content: message.content ?? '',
  createdAt: formatDateTime(message.created_at),
  modeId: fallbackMode,
  modeLabel: message.role === 'assistant' ? modeLabel(fallbackMode) : undefined,
})

const mapSession = (session: any, messages: ChatMessageItem[] = []): ChatSession => {
  const tutorMode = (session.tutor_mode ?? selectedMode.value) as TutorModeId
  return {
    id: String(session.id),
    title: session.title ?? 'New Chat',
    topic: modeLabel(tutorMode),
    preview: lastMessagePreview(messages),
    updatedAt: formatDateTime(session.last_message_at ?? session.updated_at ?? session.created_at),
    messagesCount: Number(session.messages_count ?? messages.length ?? 0),
    messages,
  }
}

const upsertSession = (session: ChatSession) => {
  const index = chatSessions.value.findIndex((item) => item.id === session.id)
  if (index === -1) {
    chatSessions.value = [session, ...chatSessions.value]
    return
  }
  chatSessions.value = chatSessions.value.map((item) => (item.id === session.id ? { ...item, ...session } : item))
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) messageListRef.value.scrollTop = messageListRef.value.scrollHeight
}

const loadSessions = async () => {
  isBooting.value = true
  pageError.value = ''
  try {
    const sessions = await getSessions()
    chatSessions.value = sessions.map((session: any) => mapSession(session))
    if (chatSessions.value.length > 0) {
      await selectSession(activeSessionId.value || chatSessions.value[0].id)
    }
  } catch (error: any) {
    pageError.value = error.apiMessage ?? 'Unable to load AI Tutor sessions.'
  } finally {
    isBooting.value = false
  }
}

const selectSession = async (sessionId: string) => {
  if (!sessionId) return
  activeSessionId.value = sessionId
  pageError.value = ''
  try {
    const detail = await getSession(sessionId)
    const tutorMode = (detail.tutor_mode ?? selectedMode.value) as TutorModeId
    const messages = (detail.messages ?? []).map((message: any) => mapMessage(message, tutorMode))
    upsertSession(mapSession(detail, messages))
    await scrollToBottom()
  } catch (error: any) {
    pageError.value = error.apiMessage ?? 'Unable to load this chat session.'
  }
}

const ensureActiveSession = async () => {
  if (activeSessionId.value) return activeSessionId.value
  const session = await createSession({ title: 'New Chat', tutor_mode: selectedMode.value })
  const mapped = mapSession(session)
  upsertSession(mapped)
  activeSessionId.value = mapped.id
  return mapped.id
}

const submitMessage = async () => {
  const question = draftMessage.value.trim()
  if (!question || loadingSessionId.value) return

  pageError.value = ''
  const selectedModeSnapshot = currentMode.value
  try {
    const sessionId = await ensureActiveSession()
    draftMessage.value = ''
    loadingSessionId.value = sessionId
    await scrollToBottom()

    const exchange = await sendMessage(sessionId, { content: question, tutor_mode: selectedModeSnapshot.id })
    const existingMessages = chatSessions.value.find((session) => session.id === sessionId)?.messages ?? []
    const nextMessages = [
      ...existingMessages,
      mapMessage(exchange.user_message, selectedModeSnapshot.id),
      mapMessage(exchange.assistant_message, selectedModeSnapshot.id),
    ]
    upsertSession(mapSession(exchange.session, nextMessages))
    await scrollToBottom()
  } catch (error: any) {
    pageError.value = error.apiMessage ?? 'Unable to send your message.'
  } finally {
    loadingSessionId.value = null
  }
}

const saveAnswerToNotes = async (messageId: string) => {
  try {
    await saveMessageToNote(messageId)
    savedMessageIds.value = new Set(savedMessageIds.value).add(messageId)
    showSavedNotice('Answer saved to notes.')
  } catch (error: any) {
    showSavedNotice(error.apiMessage ?? 'Unable to save this answer.')
  }
}

const deleteActiveSession = async () => {
  if (!activeSessionId.value) return
  const sessionId = activeSessionId.value
  try {
    await deleteSession(sessionId)
    chatSessions.value = chatSessions.value.filter((session) => session.id !== sessionId)
    activeSessionId.value = chatSessions.value[0]?.id ?? ''
    if (activeSessionId.value) await selectSession(activeSessionId.value)
    showSavedNotice('Session deleted.')
  } catch (error: any) {
    pageError.value = error.apiMessage ?? 'Unable to delete this session.'
  }
}

const startFreshSession = async () => {
  pageError.value = ''
  try {
    const session = await createSession({ title: 'New Chat', tutor_mode: selectedMode.value })
    const mapped = mapSession(session)
    upsertSession(mapped)
    activeSessionId.value = mapped.id
    draftMessage.value = ''
    await scrollToBottom()
  } catch (error: any) {
    pageError.value = error.apiMessage ?? 'Unable to create a new session.'
  }
}

const showSavedNotice = (message: string) => {
  savedNotice.value = message
  if (savedNoticeTimer) window.clearTimeout(savedNoticeTimer)
  savedNoticeTimer = window.setTimeout(() => {
    savedNotice.value = ''
  }, 1800)
}

const selectTutorMode = (modeId: string) => {
  selectedMode.value = modeId as TutorModeId
}

watch(activeSessionId, () => {
  scrollToBottom()
})

onMounted(loadSessions)

onBeforeUnmount(() => {
  if (savedNoticeTimer) window.clearTimeout(savedNoticeTimer)
})
</script>
