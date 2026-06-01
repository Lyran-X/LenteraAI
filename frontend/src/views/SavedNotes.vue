<template>
  <div class="w-full min-w-0 space-y-5 overflow-x-hidden xl:space-y-6">
    <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0 xl:flex-none">
      <div class="flex min-w-0 flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
        <div class="min-w-0">
          <p class="text-sm font-medium text-cyan-200/80">Saved Notes</p>
          <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Knowledge vault</h2>
          <p class="mt-2 text-sm leading-6 text-slate-400">
            Collect AI Tutor answers, document insights, quiz reviews, and your own manual notes in one place.
          </p>
        </div>
        <button
          class="inline-flex min-h-11 w-fit items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-4 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15"
          type="button"
          @click="openEditor()"
        >
          New Note
        </button>
      </div>

      <div class="mt-5 grid min-w-0 gap-3 xl:grid-cols-[minmax(0,1fr)_auto]">
        <label class="flex min-w-0 items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-slate-400">
          <svg class="h-4 w-4 shrink-0 text-slate-500" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="m21 21-4.3-4.3M11 18a7 7 0 1 1 0-14 7 7 0 0 1 0 14Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
          </svg>
          <input
            v-model="searchQuery"
            class="min-w-0 flex-1 bg-transparent text-white placeholder:text-slate-500 focus:outline-none"
            placeholder="Search title, content, or tags"
            type="search"
          />
        </label>

        <div class="thin-scrollbar flex gap-2 overflow-x-auto pb-1">
          <button
            v-for="source in sourceFilters"
            :key="source.value"
            class="shrink-0 rounded-xl border px-4 py-3 text-sm font-semibold transition"
            :class="activeSource === source.value ? 'border-cyan-300/35 bg-cyan-300/10 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/[0.08]'"
            type="button"
            @click="activeSource = source.value"
          >
            {{ source.label }}
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="mt-5 rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100">
        {{ errorMessage }}
      </div>
      <div v-if="actionNotice" class="mt-5 rounded-2xl border border-emerald-300/20 bg-emerald-300/10 px-4 py-3 text-sm font-medium text-emerald-100">
        {{ actionNotice }}
      </div>
    </GlassCard>

    <section class="grid min-w-0 grid-cols-1 gap-5 xl:grid-cols-[minmax(0,1fr)_420px] xl:gap-6">
      <div class="min-w-0">
        <div v-if="isLoading" class="rounded-2xl border border-white/10 bg-white/[0.04] p-6 text-sm text-slate-300">
          Loading saved notes...
        </div>

        <div v-else-if="notes.length === 0" class="rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center">
          <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
            <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <path d="M6 3h12v18l-6-3-6 3V3Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
          </div>
          <p class="mt-4 font-semibold text-white">No saved notes yet</p>
          <p class="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
            Save an AI Tutor answer or create your first note.
          </p>
          <button
            class="mt-5 inline-flex min-h-10 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-4 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15"
            type="button"
            @click="openEditor()"
          >
            Create Note
          </button>
        </div>

        <div v-else class="min-w-0 space-y-5">
          <div class="grid min-w-0 gap-4 md:grid-cols-2 2xl:grid-cols-3">
          <article
            v-for="note in paginatedNotes"
            :key="note.id"
            class="group flex min-h-[22rem] min-w-0 flex-col rounded-2xl border border-white/10 bg-white/[0.045] p-4 transition hover:border-cyan-300/25 hover:bg-white/[0.065]"
          >
            <div class="flex min-w-0 items-start justify-between gap-3">
              <div class="min-w-0">
                <div class="flex min-w-0 flex-wrap items-center gap-2">
                  <span :class="['rounded-full px-2.5 py-1 text-[11px] font-semibold', sourceBadgeClass(note.source_type)]">
                    {{ sourceLabel(note.source_type) }}
                  </span>
                  <span v-if="note.is_pinned" class="rounded-full border border-amber-300/20 bg-amber-300/10 px-2.5 py-1 text-[11px] font-semibold text-amber-100">
                    Pinned
                  </span>
                </div>
                <h3 class="mt-3 line-clamp-2 break-words text-base font-semibold text-white">{{ note.title }}</h3>
              </div>
              <button
                class="shrink-0 rounded-xl border border-white/10 bg-white/[0.05] px-3 py-2 text-xs font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
                type="button"
                :disabled="activeActionId === note.id"
                @click="togglePin(note)"
              >
                {{ note.is_pinned ? 'Unpin' : 'Pin' }}
              </button>
            </div>

            <p class="mt-3 line-clamp-4 min-h-[5.5rem] break-words text-sm leading-6 text-slate-300">
              {{ notePreview(note.content) }}
            </p>

            <div v-if="note.tags.length" class="mt-4 flex min-w-0 flex-wrap gap-2">
              <span v-for="tag in note.tags" :key="`${note.id}-${tag}`" class="rounded-full border border-white/10 bg-white/[0.045] px-2.5 py-1 text-[11px] text-slate-300">
                #{{ tag }}
              </span>
            </div>

            <div class="mt-auto pt-4">
              <p class="text-xs text-slate-500">Updated {{ formatDate(note.updated_at || note.created_at) }}</p>
              <div class="mt-3 grid grid-cols-2 gap-2">
                <button
                  class="rounded-xl border border-white/10 bg-white/[0.055] px-3 py-2 text-sm font-semibold text-slate-200 transition hover:bg-white/10"
                  type="button"
                  @click="openEditor(note)"
                >
                  View/Edit
                </button>
                <button
                  class="rounded-xl border border-rose-300/20 bg-rose-300/10 px-3 py-2 text-sm font-semibold text-rose-100 transition hover:bg-rose-300/15 disabled:cursor-not-allowed disabled:opacity-50"
                  type="button"
                  :disabled="activeActionId === note.id"
                  @click="confirmDeleteNote(note)"
                >
                  Delete
                </button>
              </div>
            </div>
          </article>
          </div>

          <nav v-if="totalPages > 1" class="flex flex-wrap items-center justify-center gap-2" aria-label="Saved notes pagination">
            <button
              class="min-h-10 rounded-xl border border-white/10 bg-white/[0.05] px-3 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
              type="button"
              :disabled="currentPage === 1"
              @click="prevPage"
            >
              Previous
            </button>
            <button
              v-for="page in visiblePageNumbers"
              :key="page"
              class="h-10 min-w-10 rounded-xl border px-3 text-sm font-semibold transition"
              :class="currentPage === page ? 'border-cyan-300/35 bg-cyan-300/10 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/10'"
              type="button"
              @click="goToPage(page)"
            >
              {{ page }}
            </button>
            <button
              class="min-h-10 rounded-xl border border-white/10 bg-white/[0.05] px-3 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
              type="button"
              :disabled="currentPage === totalPages"
              @click="nextPage"
            >
              Next
            </button>
          </nav>
        </div>
      </div>

      <GlassCard padding="p-4 sm:p-5" extra-class="min-w-0 self-start xl:min-h-[560px]">
        <div class="rounded-2xl border border-cyan-300/14 bg-cyan-300/[0.06] p-5">
          <p class="font-semibold text-white">Available now</p>
          <p class="mt-2 text-sm leading-6 text-slate-300">
            Notes from AI Tutor, manual notes, quiz review notes, and document QA notes all use your authenticated account.
          </p>
        </div>

        <div class="mt-5 grid grid-cols-2 gap-3">
          <div class="rounded-2xl border border-white/10 bg-white/[0.045] p-4">
            <p class="text-xs text-slate-500">Total notes</p>
            <p class="mt-1 text-2xl font-semibold text-white">{{ notes.length }}</p>
          </div>
          <div class="rounded-2xl border border-white/10 bg-white/[0.045] p-4">
            <p class="text-xs text-slate-500">Pinned</p>
            <p class="mt-1 text-2xl font-semibold text-white">{{ pinnedCount }}</p>
          </div>
        </div>

        <div class="mt-5 rounded-2xl border border-white/10 bg-white/[0.04] p-4">
          <div class="flex items-center justify-between gap-3">
            <p class="font-semibold text-white">Recent source distribution</p>
            <button class="text-xs font-semibold text-cyan-100 transition hover:text-cyan-50" type="button" @click="loadNotes">
              Refresh
            </button>
          </div>
          <div class="thin-scrollbar mt-4 max-h-56 space-y-3 overflow-y-auto pr-1">
            <div v-for="item in sourceDistribution" :key="item.value" class="rounded-2xl border border-white/8 bg-white/[0.04] p-3">
              <div class="flex items-center justify-between gap-3 text-sm">
                <span class="font-medium text-slate-200">{{ item.label }}</span>
                <span class="font-semibold text-white">{{ item.count }}</span>
              </div>
              <div class="mt-2 h-1.5 rounded-full bg-slate-800">
                <div class="h-1.5 rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500" :style="{ width: `${item.percent}%` }" />
              </div>
            </div>
          </div>
        </div>

        <div class="mt-5 grid gap-3">
          <RouterLink
            class="inline-flex min-h-10 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-3 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15"
            to="/dashboard/ai-tutor"
          >
            Open AI Tutor
          </RouterLink>
          <RouterLink
            class="inline-flex min-h-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-3 text-sm font-semibold text-slate-200 transition hover:bg-white/10"
            to="/dashboard/quiz-arena"
          >
            Review Quizzes
          </RouterLink>
        </div>
      </GlassCard>
    </section>

    <Teleport to="body">
      <div v-if="isEditorOpen" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-sm">
        <form class="flex max-h-[92vh] w-full max-w-4xl min-w-0 flex-col overflow-hidden rounded-3xl border border-white/10 bg-slate-950 shadow-2xl" @submit.prevent="submitEditor">
          <div class="flex flex-none items-start justify-between gap-4 border-b border-white/10 p-5">
            <div class="min-w-0">
              <p class="text-sm font-medium text-cyan-200/80">{{ editingNote ? 'Edit note' : 'New note' }}</p>
              <h2 class="mt-1 text-xl font-semibold text-white">{{ editorForm.title || 'Untitled note' }}</h2>
            </div>
            <button class="rounded-xl border border-white/10 bg-white/[0.06] px-3 py-2 text-sm font-semibold text-slate-200 transition hover:bg-white/10" type="button" @click="closeEditor">
              Close
            </button>
          </div>

          <div class="thin-scrollbar grid min-h-0 flex-1 gap-4 overflow-y-auto p-5 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
            <div class="grid min-w-0 content-start gap-4">
              <label class="grid gap-2">
                <span class="text-sm font-medium text-slate-300">Title</span>
                <input
                  v-model="editorForm.title"
                  class="rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="Note title"
                  required
                />
              </label>

              <label class="grid gap-2">
                <span class="text-sm font-medium text-slate-300">Content</span>
                <textarea
                  v-model="editorForm.content"
                  class="min-h-64 resize-none rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="Write your note... Markdown is supported for preview."
                  required
                />
              </label>

              <label class="grid gap-2">
                <span class="text-sm font-medium text-slate-300">Tags</span>
                <input
                  v-model="editorForm.tagsInput"
                  class="rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="ai, machine-learning"
                />
              </label>

              <div class="grid gap-4 sm:grid-cols-2">
                <label class="grid gap-2">
                  <span class="text-sm font-medium text-slate-300">Source type</span>
                  <select
                    v-model="editorForm.source_type"
                    class="rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-60"
                    :disabled="Boolean(editingNote)"
                  >
                    <option value="manual">Manual</option>
                    <option value="ai_tutor">AI Tutor</option>
                    <option value="document_qa">Document QA</option>
                    <option value="quiz">Quiz</option>
                  </select>
                </label>

                <label class="flex items-center gap-3 self-end rounded-2xl border border-white/10 bg-white/[0.045] px-4 py-3 text-sm font-semibold text-slate-200">
                  <input v-model="editorForm.is_pinned" class="h-4 w-4 accent-cyan-300" type="checkbox" />
                  Pin note
                </label>
              </div>
            </div>

            <div class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.04] p-4">
              <div class="mb-3 flex items-center justify-between gap-3">
                <p class="font-semibold text-white">Markdown preview</p>
                <span :class="['rounded-full px-2.5 py-1 text-[11px] font-semibold', sourceBadgeClass(editorForm.source_type)]">
                  {{ sourceLabel(editorForm.source_type) }}
                </span>
              </div>
              <div class="notes-markdown thin-scrollbar max-h-[30rem] overflow-y-auto rounded-2xl border border-white/8 bg-slate-950/40 p-4 text-sm leading-6 text-slate-200" v-html="renderMarkdown(editorForm.content || 'Preview will appear here.')" />
            </div>
          </div>

          <div class="flex flex-none flex-col-reverse gap-3 border-t border-white/10 p-5 sm:flex-row sm:justify-end">
            <button class="min-h-11 rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10" type="button" @click="closeEditor">
              Cancel
            </button>
            <button
              class="min-h-11 rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-4 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50"
              type="submit"
              :disabled="isSavingNote || !editorForm.title.trim() || !editorForm.content.trim()"
            >
              {{ isSavingNote ? 'Saving...' : editingNote ? 'Save Changes' : 'Create Note' }}
            </button>
          </div>
        </form>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import Swal from 'sweetalert2'
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import GlassCard from '../components/GlassCard.vue'
import { createNote, deleteNote, getNotes, pinNote, unpinNote, updateNote } from '../services/notesService'

type PublicSourceType = 'ai_tutor' | 'document_qa' | 'quiz' | 'manual'
type SourceFilter = 'all' | PublicSourceType

interface SavedNote {
  id: string
  title: string
  content: string
  source_type: PublicSourceType
  source_id?: string | null
  tags: string[]
  is_pinned: boolean
  metadata?: Record<string, unknown>
  created_at: string
  updated_at: string
}

interface EditorForm {
  title: string
  content: string
  tagsInput: string
  source_type: PublicSourceType
  is_pinned: boolean
}

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

const sourceFilters: Array<{ label: string; value: SourceFilter }> = [
  { label: 'All', value: 'all' },
  { label: 'AI Tutor', value: 'ai_tutor' },
  { label: 'Document QA', value: 'document_qa' },
  { label: 'Quiz', value: 'quiz' },
  { label: 'Manual', value: 'manual' },
]

const sourceLabels: Record<PublicSourceType, string> = {
  ai_tutor: 'AI Tutor',
  document_qa: 'Document QA',
  quiz: 'Quiz',
  manual: 'Manual',
}

const notes = ref<SavedNote[]>([])
const searchQuery = ref('')
const activeSource = ref<SourceFilter>('all')
const errorMessage = ref('')
const actionNotice = ref('')
const isLoading = ref(false)
const isEditorOpen = ref(false)
const isSavingNote = ref(false)
const editingNote = ref<SavedNote | null>(null)
const activeActionId = ref<string | null>(null)
const editorForm = reactive<EditorForm>({
  title: '',
  content: '',
  tagsInput: '',
  source_type: 'manual',
  is_pinned: false,
})

const NOTES_PER_PAGE = 6

let searchTimer: number | undefined
let noticeTimer: number | undefined

const currentPage = ref(1)
const filteredNotes = computed(() => notes.value)
const totalPages = computed(() => Math.max(1, Math.ceil(filteredNotes.value.length / NOTES_PER_PAGE)))
const paginatedNotes = computed(() => {
  const start = (currentPage.value - 1) * NOTES_PER_PAGE
  return filteredNotes.value.slice(start, start + NOTES_PER_PAGE)
})
const visiblePageNumbers = computed(() => Array.from({ length: totalPages.value }, (_, index) => index + 1))

const pinnedCount = computed(() => notes.value.filter((note) => note.is_pinned).length)

const sourceDistribution = computed(() => {
  const total = Math.max(notes.value.length, 1)
  return sourceFilters
    .filter((source): source is { label: string; value: PublicSourceType } => source.value !== 'all')
    .map((source) => {
      const count = notes.value.filter((note) => note.source_type === source.value).length
      return {
        ...source,
        count,
        percent: Math.round((count / total) * 100),
      }
    })
})

const normalizeNote = (raw: any): SavedNote => ({
  id: String(raw.id),
  title: raw.title ?? 'Untitled note',
  content: raw.content ?? '',
  source_type: normalizeSourceType(raw.source_type),
  source_id: raw.source_id ?? null,
  tags: Array.isArray(raw.tags) ? raw.tags.map((tag: unknown) => String(tag)).filter(Boolean) : [],
  is_pinned: Boolean(raw.is_pinned),
  metadata: raw.metadata ?? {},
  created_at: raw.created_at ?? new Date().toISOString(),
  updated_at: raw.updated_at ?? raw.created_at ?? new Date().toISOString(),
})

const normalizeSourceType = (value: unknown): PublicSourceType => {
  const normalized = String(value ?? 'manual')
  if (normalized === 'ai_tutor' || normalized === 'document_qa' || normalized === 'quiz' || normalized === 'manual') return normalized
  return 'manual'
}

const sortNotes = () => {
  notes.value = [...notes.value].sort((a, b) => {
    if (a.is_pinned !== b.is_pinned) return Number(b.is_pinned) - Number(a.is_pinned)
    return new Date(b.updated_at || b.created_at).getTime() - new Date(a.updated_at || a.created_at).getTime()
  })
}

const loadNotes = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const params = {
      search: searchQuery.value.trim() || undefined,
      source_type: activeSource.value === 'all' ? undefined : activeSource.value,
      limit: 100,
    }
    const data = await getNotes(params)
    notes.value = Array.isArray(data) ? data.map(normalizeNote) : []
    sortNotes()
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
  } catch (error: any) {
    errorMessage.value = error?.apiMessage ?? 'Failed to load saved notes.'
  } finally {
    isLoading.value = false
  }
}

const showNotice = (message: string) => {
  actionNotice.value = message
  if (noticeTimer) window.clearTimeout(noticeTimer)
  noticeTimer = window.setTimeout(() => {
    actionNotice.value = ''
  }, 2200)
}

const sourceLabel = (sourceType: string) => sourceLabels[normalizeSourceType(sourceType)]

const sourceBadgeClass = (sourceType: string) => {
  const normalized = normalizeSourceType(sourceType)
  if (normalized === 'ai_tutor') return 'border border-cyan-300/20 bg-cyan-300/10 text-cyan-100'
  if (normalized === 'document_qa') return 'border border-blue-300/20 bg-blue-300/10 text-blue-100'
  if (normalized === 'quiz') return 'border border-violet-300/20 bg-violet-300/10 text-violet-100'
  return 'border border-slate-300/15 bg-slate-300/10 text-slate-200'
}

const notePreview = (content: string) => String(content || '')
  .replace(/```[\s\S]*?```/g, ' ')
  .replace(/[#>*_`|\[\]()]/g, '')
  .replace(/\s+/g, ' ')
  .trim() || 'No content yet.'

const formatDate = (value: string) => {
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'recently'
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric', year: 'numeric' }).format(date)
}

const parseTagsInput = (value: string) => value
  .split(',')
  .map((tag) => tag.trim())
  .filter(Boolean)
  .slice(0, 12)

const formatTagsInput = (tags: string[]) => tags.join(', ')

const renderMarkdown = (content: string) => md.render(content || '')

const openEditor = (note?: SavedNote) => {
  editingNote.value = note ?? null
  editorForm.title = note?.title ?? ''
  editorForm.content = note?.content ?? ''
  editorForm.tagsInput = note ? formatTagsInput(note.tags) : ''
  editorForm.source_type = note?.source_type ?? 'manual'
  editorForm.is_pinned = note?.is_pinned ?? false
  isEditorOpen.value = true
}

const closeEditor = () => {
  if (isSavingNote.value) return
  isEditorOpen.value = false
  editingNote.value = null
}

const submitEditor = async () => {
  if (!editorForm.title.trim() || !editorForm.content.trim()) return

  isSavingNote.value = true
  errorMessage.value = ''
  try {
    if (editingNote.value) {
      await updateNote(editingNote.value.id, {
        title: editorForm.title.trim(),
        content: editorForm.content.trim(),
        tags: parseTagsInput(editorForm.tagsInput),
        is_pinned: editorForm.is_pinned,
      })
      showNotice('Note updated.')
    } else {
      await createNote({
        title: editorForm.title.trim(),
        content: editorForm.content.trim(),
        source_type: editorForm.source_type,
        tags: parseTagsInput(editorForm.tagsInput),
        is_pinned: editorForm.is_pinned,
      })
      showNotice('Note created.')
    }

    isEditorOpen.value = false
    editingNote.value = null
    await loadNotes()
  } catch (error: any) {
    errorMessage.value = error?.apiMessage ?? 'Failed to save note.'
  } finally {
    isSavingNote.value = false
  }
}

const togglePin = async (note: SavedNote) => {
  activeActionId.value = note.id
  errorMessage.value = ''
  try {
    const updated = note.is_pinned ? await unpinNote(note.id) : await pinNote(note.id)
    const normalized = normalizeNote(updated)
    notes.value = notes.value.map((item) => (item.id === note.id ? normalized : item))
    sortNotes()
    showNotice(normalized.is_pinned ? 'Note pinned.' : 'Note unpinned.')
  } catch (error: any) {
    errorMessage.value = error?.apiMessage ?? 'Failed to update pinned state.'
  } finally {
    activeActionId.value = null
  }
}

const goToPage = (page: number) => {
  currentPage.value = Math.min(Math.max(page, 1), totalPages.value)
}

const nextPage = () => {
  goToPage(currentPage.value + 1)
}

const prevPage = () => {
  goToPage(currentPage.value - 1)
}

const confirmDeleteNote = async (note: SavedNote) => {
  const result = await Swal.fire({
    title: 'Delete note?',
    text: 'This note will be permanently removed.',
    icon: 'warning',
    showCancelButton: true,
    reverseButtons: true,
    confirmButtonText: 'Delete',
    cancelButtonText: 'Cancel',
    background: '#0f172a',
    color: '#e5e7eb',
    confirmButtonColor: '#ef4444',
    cancelButtonColor: '#334155',
  })

  if (!result.isConfirmed) return

  activeActionId.value = note.id
  errorMessage.value = ''
  try {
    await deleteNote(note.id)
    notes.value = notes.value.filter((item) => item.id !== note.id)
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    await Swal.fire({
      title: 'Note deleted',
      icon: 'success',
      toast: true,
      position: 'top-end',
      timer: 1800,
      showConfirmButton: false,
      background: '#0f172a',
      color: '#e5e7eb',
    })
  } catch (error: any) {
    await Swal.fire({
      title: 'Failed to delete note',
      text: error?.apiMessage ?? 'Please try again.',
      icon: 'error',
      background: '#0f172a',
      color: '#e5e7eb',
      confirmButtonColor: '#38bdf8',
    })
  } finally {
    activeActionId.value = null
  }
}

watch([searchQuery, activeSource], () => {
  currentPage.value = 1
  if (searchTimer) window.clearTimeout(searchTimer)
  searchTimer = window.setTimeout(() => {
    void loadNotes()
  }, 350)
})

onMounted(() => {
  void loadNotes()
})

onBeforeUnmount(() => {
  if (searchTimer) window.clearTimeout(searchTimer)
  if (noticeTimer) window.clearTimeout(noticeTimer)
})
</script>

<style scoped>
.notes-markdown :deep(p) {
  margin: 0 0 0.75rem;
}

.notes-markdown :deep(p:last-child) {
  margin-bottom: 0;
}

.notes-markdown :deep(strong) {
  color: #f8fafc;
  font-weight: 700;
}

.notes-markdown :deep(ul),
.notes-markdown :deep(ol) {
  margin: 0.75rem 0;
  padding-left: 1.25rem;
}

.notes-markdown :deep(ul) {
  list-style: disc;
}

.notes-markdown :deep(ol) {
  list-style: decimal;
}

.notes-markdown :deep(li) {
  margin: 0.25rem 0;
}

.notes-markdown :deep(a) {
  color: #67e8f9;
  text-decoration: underline;
}

.notes-markdown :deep(code) {
  border: 1px solid rgb(255 255 255 / 0.1);
  border-radius: 0.5rem;
  background: rgb(15 23 42 / 0.8);
  padding: 0.1rem 0.35rem;
  color: #bae6fd;
  font-size: 0.85em;
}

.notes-markdown :deep(pre) {
  margin: 0.85rem 0;
  overflow-x: auto;
  border: 1px solid rgb(255 255 255 / 0.1);
  border-radius: 1rem;
  background: rgb(15 23 42 / 0.85);
  padding: 1rem;
}

.notes-markdown :deep(pre code) {
  border: 0;
  background: transparent;
  padding: 0;
}

.notes-markdown :deep(blockquote) {
  margin: 0.85rem 0;
  border-left: 2px solid rgb(34 211 238 / 0.45);
  background: rgb(34 211 238 / 0.08);
  padding: 0.75rem 1rem;
  color: #cffafe;
}

.notes-markdown :deep(table) {
  display: block;
  max-width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.notes-markdown :deep(th),
.notes-markdown :deep(td) {
  border: 1px solid rgb(255 255 255 / 0.12);
  padding: 0.5rem 0.65rem;
  text-align: left;
}

.notes-markdown :deep(th) {
  background: rgb(255 255 255 / 0.06);
  color: #f8fafc;
}
</style>