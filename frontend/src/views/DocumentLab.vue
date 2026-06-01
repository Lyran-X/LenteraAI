<template>
  <div class="w-full min-w-0 overflow-x-hidden xl:h-[calc(100vh-96px)] xl:overflow-hidden">
    <section class="grid min-w-0 grid-cols-1 gap-5 xl:h-full xl:min-h-0 xl:grid-cols-[minmax(0,1fr)_380px] xl:gap-6 2xl:grid-cols-[minmax(0,1fr)_420px]">
      <div class="flex min-w-0 flex-col gap-5 xl:h-full xl:min-h-0">
        <GlassCard padding="p-0" extra-class="flex h-[calc(100vh-120px)] min-h-[640px] w-full min-w-0 overflow-hidden xl:h-auto xl:min-h-0 xl:flex-[1.42]">
        <section class="flex h-full w-full min-h-0 min-w-0 flex-col overflow-hidden">
          <header class="w-full flex-none border-b border-white/8 p-4 sm:p-5">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div class="min-w-0">
                <p class="text-sm font-medium text-cyan-200/80">Document Lab</p>
                <h2 class="mt-1 truncate text-lg font-semibold text-white sm:text-xl">
                  {{ selectedDocument?.title ?? 'Attach or select a document' }}
                </h2>
                <p class="mt-1 truncate text-sm text-slate-400">
                  {{ selectedDocument ? `${selectedDocument.type} / ${selectedDocument.size}` : 'Upload from the chat input, then ask from the document.' }}
                </p>
              </div>
              <span
                v-if="selectedDocument"
                :class="['w-fit rounded-full px-3 py-1 text-xs font-semibold', getStatusClass(selectedDocument.status)]"
              >
                {{ selectedDocument.status }}
              </span>
            </div>
          </header>

          <div ref="messageListRef" class="thin-scrollbar min-h-0 w-full flex-1 overflow-y-auto overflow-x-hidden p-4 sm:p-5">
            <div v-if="!selectedDocument && !pendingAttachment" class="flex h-full min-h-full w-full items-start justify-center pt-6">
              <div class="w-full max-w-2xl rounded-2xl border border-white/10 bg-white/[0.035] p-6 text-center">
                <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
                  <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M7 3h7l5 5v13H7V3Zm7 0v5h5M10 13h6M10 17h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </div>
                <h3 class="mt-4 text-lg font-semibold text-white">Upload or select a document first</h3>
                <p class="mt-2 text-sm leading-6 text-slate-400">Use the + button beside the chat input to attach PDF, TXT, Word, or PowerPoint files.</p>
              </div>
            </div>

            <div v-else class="flex min-h-full w-full min-w-0 flex-col space-y-4">
              <div v-if="selectedDocument && chatMessages.length === 0" class="w-full rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-5 text-center">
                <p class="font-semibold text-white">Ask a question about this document.</p>
                <p class="mt-2 text-sm leading-6 text-slate-400">Answers and citations will come directly from the backend.</p>
              </div>

              <div v-else-if="pendingAttachment && !selectedDocument" class="w-full rounded-2xl border border-dashed border-cyan-300/20 bg-cyan-300/[0.055] p-5 text-center">
                <p class="font-semibold text-white">Attachment is ready</p>
                <p class="mt-2 text-sm leading-6 text-slate-400">Send it to upload the document. Add a question if you want EduPath AI to answer immediately after upload.</p>
              </div>

              <div v-if="askError" class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">
                {{ askError }}
              </div>

              <div
                v-for="message in chatMessages"
                :key="message.id"
                :class="['flex w-full min-w-0 overflow-x-hidden', message.role === 'user' ? 'justify-end' : 'justify-start']"
              >
                <div
                  :class="[
                    'max-w-[90%] min-w-0 break-words rounded-3xl px-4 py-3 text-sm leading-6 shadow-lg sm:max-w-[82%]',
                    message.role === 'user'
                      ? 'rounded-br-lg bg-gradient-to-r from-cyan-500 via-blue-500 to-violet-500 text-white shadow-blue-500/18'
                      : 'rounded-bl-lg border border-white/10 bg-white/[0.065] text-slate-200 shadow-black/18',
                  ]"
                >
                  <div
                    v-if="message.role === 'assistant'"
                    class="ai-markdown"
                    v-html="renderMarkdown(message.content)"
                  />
                  <p v-else class="whitespace-pre-wrap break-words">{{ message.content }}</p>

                  <div v-if="message.role === 'assistant' && message.modelName" class="mt-3 flex flex-wrap gap-2 text-[11px] text-slate-400">
                    <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">{{ message.modelProvider }}</span>
                    <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">{{ message.modelName }}</span>
                    <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">{{ message.usedChunks }} chunks</span>
                  </div>

                  <div v-if="message.role === 'assistant' && message.documentName && message.modelName" class="mt-3 flex min-w-0 flex-wrap items-center gap-2 border-t border-white/8 pt-3 text-xs text-slate-400">
                    <span>Answered from:</span>
                    <button
                      class="max-w-full truncate rounded-full border px-3 py-1 font-semibold transition disabled:cursor-not-allowed disabled:opacity-55"
                      :class="isDocumentAvailable(message.documentId) ? 'border-cyan-300/20 bg-cyan-300/10 text-cyan-100 hover:bg-cyan-300/15' : 'border-white/10 bg-white/[0.04] text-slate-500'"
                      type="button"
                      :disabled="!isDocumentAvailable(message.documentId)"
                      @click.stop="switchToMessageDocument(message)"
                    >
                      {{ message.documentName }}
                    </button>
                  </div>
                </div>
              </div>

              <div v-if="isAsking" class="flex justify-start">
                <div class="rounded-3xl rounded-bl-lg border border-white/10 bg-white/[0.065] px-4 py-3 shadow-lg shadow-black/18">
                  <div class="flex items-center gap-3 text-sm text-slate-300">
                    <div class="flex items-center gap-2">
                      <span class="h-2 w-2 animate-pulse rounded-full bg-cyan-200" />
                      <span class="h-2 w-2 animate-pulse rounded-full bg-blue-300 [animation-delay:120ms]" />
                      <span class="h-2 w-2 animate-pulse rounded-full bg-violet-300 [animation-delay:240ms]" />
                    </div>
                    <span>Searching document...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <form class="w-full flex-none border-t border-white/8 bg-slate-950/45 p-3 backdrop-blur-2xl sm:p-4" @submit.prevent="submitDocumentInteraction">
            <input
              ref="fileInputRef"
              class="hidden"
              type="file"
              :accept="fileInputAccept"
              @change="handleFileChange"
            />

            <div v-if="pendingAttachment" class="mb-3 rounded-2xl border border-white/10 bg-white/[0.055] p-3">
              <div class="flex min-w-0 items-center gap-3">
                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-xs font-bold text-cyan-100">
                  {{ pendingAttachment.type }}
                </div>
                <div class="min-w-0 flex-1">
                  <p class="truncate text-sm font-semibold text-white">{{ pendingAttachment.name }}</p>
                  <div class="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                    <span>{{ pendingAttachment.size }}</span>
                    <span :class="['rounded-full px-2 py-0.5 font-medium', getAttachmentStatusClass(pendingAttachment.status)]">
                      {{ getAttachmentStatusLabel(pendingAttachment) }}
                    </span>
                  </div>
                  <p v-if="pendingAttachment.error" class="mt-1 text-xs text-rose-200">{{ pendingAttachment.error }}</p>
                </div>
                <button
                  class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-white/10 bg-white/[0.05] text-slate-300 transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
                  type="button"
                  :disabled="pendingAttachment.status === 'uploading'"
                  @click="removeAttachment"
                >
                  <span class="sr-only">Remove attachment</span>
                  <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  </svg>
                </button>
              </div>
              <div v-if="pendingAttachment.status === 'uploading'" class="mt-3 h-1.5 rounded-full bg-slate-800">
                <div
                  class="h-1.5 rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500 transition-all duration-200"
                  :style="{ width: `${pendingAttachment.progress}%` }"
                />
              </div>
            </div>

            <div class="flex min-w-0 flex-col gap-2.5 rounded-3xl border border-white/10 bg-white/[0.055] p-2 transition focus-within:border-cyan-300/40 sm:flex-row sm:items-end">
              <div class="relative shrink-0" ref="uploadMenuRef">
                <button
                  ref="uploadButtonRef"
                  class="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.06] text-xl font-semibold text-cyan-100 transition hover:border-cyan-300/30 hover:bg-cyan-300/10 disabled:cursor-not-allowed disabled:opacity-50"
                  type="button"
                  :disabled="isBusy"
                  @click.stop="toggleUploadMenu"
                >
                  +
                </button>

                <div
                  v-if="uploadMenuOpen"
                  class="absolute bottom-full left-0 z-30 mb-3 w-64 rounded-2xl border border-white/10 bg-slate-950/95 p-2 shadow-2xl shadow-black/40 backdrop-blur-2xl"
                >
                  <button
                    v-for="option in uploadOptions"
                    :key="option.accept"
                    class="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-slate-200 transition hover:bg-white/[0.07]"
                    type="button"
                    @click="chooseUploadOption(option)"
                  >
                    <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 text-xs font-bold text-cyan-100">
                      {{ option.badge }}
                    </span>
                    <span class="min-w-0">
                      <span class="block font-semibold text-white">{{ option.label }}</span>
                      <span class="block text-xs text-slate-500">{{ option.description }}</span>
                    </span>
                  </button>
                </div>
              </div>

              <textarea
                v-model="questionDraft"
                class="thin-scrollbar max-h-32 min-h-12 min-w-0 flex-1 resize-none overflow-y-auto bg-transparent px-3 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:outline-none"
                :disabled="isBusy"
                rows="1"
                :placeholder="inputPlaceholder"
                @keydown.enter.exact.prevent="submitDocumentInteraction"
              />
              <button
                class="inline-flex min-h-11 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-4 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 sm:min-w-24"
                type="submit"
                :disabled="!canSubmit"
              >
                {{ submitLabel }}
              </button>
            </div>
          </form>
          </section>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5" extra-class="flex h-[420px] min-w-0 flex-col overflow-hidden xl:h-auto xl:min-h-0 xl:flex-[0.78]">
          <div class="flex flex-none items-start justify-between gap-4">
            <div class="min-w-0">
              <p class="text-sm font-medium text-cyan-200/80">Document Evidence Viewer</p>
              <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Evidence used by AI</h2>
            </div>
            <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
              {{ activeCitations.length }} chunks
            </span>
          </div>

          <div v-if="activeCitations.length === 0" class="mt-4 flex min-h-0 flex-1 items-center justify-center rounded-2xl border border-dashed border-white/12 bg-white/[0.035] p-6 text-center">
            <div class="max-w-md">
              <p class="font-semibold text-white">Ask a question to see evidence from the document.</p>
              <p class="mt-2 text-sm leading-6 text-slate-400">The viewer will show backend citations as evidence blocks, separate from the clean answer bubble.</p>
            </div>
          </div>

          <div v-else class="thin-scrollbar mt-4 min-h-0 flex-1 space-y-3 overflow-y-auto pr-1">
            <article
              v-for="(citation, index) in activeCitations"
              :id="getEvidenceDomId(index)"
              :key="`${citation.id}-evidence`"
              class="rounded-2xl border bg-white/[0.045] p-4 transition"
              :class="focusedEvidenceIndex === index ? 'border-cyan-300/50 shadow-lg shadow-cyan-500/10' : 'border-white/8'"
            >
              <div class="flex flex-wrap items-start justify-between gap-3">
                <div class="min-w-0">
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-cyan-200">Evidence {{ index + 1 }}</p>
                  <h3 class="mt-1 truncate text-sm font-semibold text-white">{{ citation.source }}</h3>
                </div>
                <span class="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-xs font-semibold text-cyan-100">
                  Used as evidence
                </span>
              </div>

              <div class="mt-3 flex flex-wrap gap-2 text-xs text-slate-400">
                <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">Page {{ citation.page }}</span>
                <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">Chunk {{ citation.chunk }}</span>
                <span class="rounded-full border border-white/10 bg-white/[0.04] px-2.5 py-1">Score {{ citation.score }}</span>
              </div>

              <div class="mt-4 rounded-2xl border-l border-cyan-300/40 bg-cyan-400/10 px-4 py-3 text-sm leading-7 text-cyan-50">
                <p class="whitespace-pre-wrap break-words" v-html="renderHighlightedEvidence(citation.evidenceText || citation.excerpt, activeEvidenceQuestion)" />
              </div>
            </article>
          </div>
        </GlassCard>
      </div>

      <aside class="flex min-w-0 flex-col gap-5 xl:h-full xl:min-h-0">
        <GlassCard padding="p-4 sm:p-5" extra-class="min-w-0 xl:flex-[1.16] xl:min-h-0 xl:overflow-hidden">
          <div class="flex h-full min-h-0 flex-col">
            <div class="flex flex-none items-start justify-between gap-4">
              <div class="min-w-0">
                <p class="text-sm font-medium text-violet-200/80">Document context</p>
                <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Sources and metadata</h2>
              </div>
              <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
                {{ documents.length }} files
              </span>
            </div>

            <div v-if="loadError" class="mt-5 flex-none rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">
              {{ loadError }}
            </div>
            <div v-if="documentActionError" class="mt-5 flex-none rounded-2xl border border-amber-300/20 bg-amber-300/10 px-4 py-3 text-sm text-amber-100">
              {{ documentActionError }}
            </div>
            <div v-if="documentActionMessage" class="mt-5 flex-none rounded-2xl border border-emerald-300/20 bg-emerald-300/10 px-4 py-3 text-sm text-emerald-100">
              {{ documentActionMessage }}
            </div>

            <div class="thin-scrollbar mt-5 min-h-0 flex-1 overflow-y-auto pr-1">
              <div v-if="isLoadingDocuments" class="rounded-2xl border border-white/8 bg-white/[0.04] p-5 text-center">
                <p class="font-semibold text-white">Loading documents</p>
                <p class="mt-2 text-sm leading-6 text-slate-400">Fetching your protected document list.</p>
              </div>

              <div v-else-if="documents.length === 0" class="rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-5 text-center">
                <p class="font-semibold text-white">No uploaded documents</p>
                <p class="mt-2 text-sm leading-6 text-slate-400">Attach a file from the chat input to create your first document context.</p>
              </div>

              <div v-else class="space-y-2">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Recent documents</p>
                <article
                  v-for="doc in documents"
                  :key="doc.id"
                  class="w-full min-w-0 rounded-2xl border p-3 transition"
                  :class="
                    doc.id === selectedDocumentId
                      ? 'border-cyan-300/35 bg-cyan-300/10 shadow-lg shadow-cyan-500/10'
                      : 'border-white/8 bg-white/[0.04] hover:border-white/16 hover:bg-white/[0.07]'
                  "
                >
                  <div class="flex min-w-0 items-start gap-2">
                    <button class="min-w-0 flex-1 text-left" type="button" @click="selectDocument(doc.id)">
                      <div class="flex min-w-0 items-start justify-between gap-2">
                        <span class="min-w-0 truncate text-sm font-semibold text-white">{{ doc.title }}</span>
                        <span :class="['shrink-0 rounded-full px-2 py-0.5 text-[11px] font-semibold', getStatusClass(doc.status)]">
                          {{ doc.status }}
                        </span>
                      </div>
                      <p class="mt-1 truncate text-xs text-slate-500">{{ doc.type }} / {{ doc.size }} / {{ doc.uploadedAt }}</p>
                    </button>

                    <button
                      class="shrink-0 rounded-full border border-rose-300/15 bg-rose-300/10 px-2.5 py-1 text-[11px] font-semibold text-rose-100 transition hover:bg-rose-300/15 disabled:cursor-not-allowed disabled:opacity-50"
                      type="button"
                      :disabled="isDeletingDocument && deletingDocumentId === doc.id"
                      @click.stop="deleteDocument(doc)"
                    >
                      {{ isDeletingDocument && deletingDocumentId === doc.id ? 'Deleting' : 'Delete' }}
                    </button>
                  </div>
                </article>
              </div>

              <div v-if="selectedDocument" class="mt-6 space-y-5">
                <section>
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Summary</p>
                  <div class="thin-scrollbar mt-3 max-h-36 overflow-y-auto pr-1 text-sm leading-6 text-slate-300">{{ selectedDocument.summary || 'Summary is being generated or not available yet.' }}</div>
                </section>

                <section>
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Metadata</p>
                  <div class="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-300">
                    <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-3">
                      <span class="block text-xs text-slate-500">Words</span>
                      <span class="mt-1 block font-semibold text-white">{{ selectedDocument.wordCount }}</span>
                    </div>
                    <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-3">
                      <span class="block text-xs text-slate-500">Chunks</span>
                      <span class="mt-1 block font-semibold text-white">{{ selectedDocument.chunks }}</span>
                    </div>
                  </div>
                </section>

                <section v-if="activeAnswerMeta">
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Last answer</p>
                  <div class="mt-3 space-y-2 text-sm text-slate-300">
                    <div class="rounded-2xl border border-white/8 bg-white/[0.045] px-3 py-2.5">
                      Provider: <span class="font-semibold text-cyan-100">{{ activeAnswerMeta.modelProvider }}</span>
                    </div>
                    <div class="rounded-2xl border border-white/8 bg-white/[0.045] px-3 py-2.5">
                      Model: <span class="font-semibold text-cyan-100">{{ activeAnswerMeta.modelName }}</span>
                    </div>
                    <div class="rounded-2xl border border-white/8 bg-white/[0.045] px-3 py-2.5">
                      Used chunks: <span class="font-semibold text-cyan-100">{{ activeAnswerMeta.usedChunks }}</span>
                    </div>
                  </div>
                </section>
              </div>
            </div>
          </div>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5" extra-class="flex min-h-[320px] min-w-0 flex-col overflow-hidden xl:min-h-0 xl:flex-[0.84]">
          <div class="flex flex-none items-start justify-between gap-4">
            <div class="min-w-0">
              <p class="text-sm font-medium text-cyan-200/80">Sources from Backend</p>
              <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Citation cards</h2>
            </div>
            <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
              {{ activeCitations.length }} sources
            </span>
          </div>

          <div v-if="activeCitations.length === 0" class="mt-4 flex min-h-0 flex-1 items-center justify-center rounded-2xl border border-dashed border-white/12 bg-white/[0.035] p-5 text-center">
            <div>
              <p class="font-semibold text-white">Sources will appear after you ask a question.</p>
              <p class="mt-2 text-sm leading-6 text-slate-400">Backend citations stay separate from the answer so the response remains readable.</p>
            </div>
          </div>

          <div v-else class="thin-scrollbar mt-4 min-h-0 flex-1 space-y-3 overflow-y-auto pr-1">
            <button
              v-for="(citation, index) in activeCitations"
              :key="`${citation.id}-source`"
              class="w-full rounded-2xl border bg-white/[0.045] p-3 text-left transition hover:border-cyan-300/35 hover:bg-cyan-300/[0.08]"
              :class="focusedEvidenceIndex === index ? 'border-cyan-300/45' : 'border-white/8'"
              type="button"
              @click="focusEvidence(index)"
            >
              <div class="flex items-start justify-between gap-3">
                <p class="min-w-0 truncate text-sm font-semibold text-white">{{ citation.source }}</p>
                <span class="shrink-0 text-xs text-cyan-100">p. {{ citation.page }}</span>
              </div>
              <p class="mt-2 line-clamp-4 text-xs leading-5 text-slate-400">{{ citation.excerpt }}</p>
              <p class="mt-2 text-xs text-slate-500">Chunk {{ citation.chunk }} / score {{ citation.score }}</p>
            </button>
          </div>
        </GlassCard>
      </aside>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import MarkdownIt from 'markdown-it'
import Swal from 'sweetalert2'

import GlassCard from '../components/GlassCard.vue'
import {
  askDocumentQuestion,
  deleteDocument as deleteDocumentRequest,
  getDocuments,
  uploadDocument as uploadDocumentRequest,
} from '../services/documentService'

type DocumentStatus = 'Uploaded' | 'Processing' | 'Ready' | 'Failed' | 'Archived'
type BackendDocumentStatus = 'uploaded' | 'processing' | 'ready' | 'failed' | 'archived' | string
type MessageRole = 'user' | 'assistant'
type AttachmentStatus = 'ready_to_upload' | 'uploading' | 'ready' | 'failed'

interface Citation {
  id: string
  source: string
  page: string
  pageStart?: number | string | null
  pageEnd?: number | string | null
  chunk: string
  score: string
  excerpt: string
  evidenceText: string
  vectorId?: string
}

interface DocumentMessage {
  id: string
  role: MessageRole
  content: string
  citations?: Citation[]
  usedChunks?: number
  modelProvider?: string
  modelName?: string
  documentId?: string
  documentName?: string
  question?: string
  createdAt?: string
}

interface LearningDocument {
  id: string
  title: string
  originalFilename: string
  type: string
  size: string
  pages: number | string
  chunks: number
  wordCount: number | string
  uploadedAt: string
  status: DocumentStatus
  backendStatus: BackendDocumentStatus
  summary: string
  messages: DocumentMessage[]
}

interface UploadOption {
  label: string
  description: string
  accept: string
  badge: string
}

interface PendingAttachment {
  file: File
  name: string
  type: string
  size: string
  status: AttachmentStatus
  progress: number
  error: string
  uploadedDocumentId?: string
}

const md = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

const defaultLinkOpen = md.renderer.rules.link_open
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  const targetIndex = tokens[idx].attrIndex('target')
  if (targetIndex < 0) tokens[idx].attrPush(['target', '_blank'])
  else tokens[idx].attrs![targetIndex][1] = '_blank'

  const relIndex = tokens[idx].attrIndex('rel')
  if (relIndex < 0) tokens[idx].attrPush(['rel', 'noopener noreferrer'])
  else tokens[idx].attrs![relIndex][1] = 'noopener noreferrer'

  return defaultLinkOpen ? defaultLinkOpen(tokens, idx, options, env, self) : self.renderToken(tokens, idx, options)
}

md.renderer.rules.table_open = () => '<div class="ai-markdown-table-wrap thin-scrollbar"><table>\n'
md.renderer.rules.table_close = () => '</table></div>\n'

const uploadOptions: UploadOption[] = [
  { label: 'Upload PDF', description: '.pdf document', accept: '.pdf', badge: 'PDF' },
  { label: 'Upload TXT', description: '.txt notes', accept: '.txt', badge: 'TXT' },
  { label: 'Upload Word', description: '.docx document', accept: '.docx', badge: 'DOCX' },
  { label: 'Upload PowerPoint', description: '.pptx slides', accept: '.pptx', badge: 'PPTX' },
]

const fileInputRef = ref<HTMLInputElement | null>(null)
const messageListRef = ref<HTMLElement | null>(null)
const uploadMenuRef = ref<HTMLElement | null>(null)
const uploadButtonRef = ref<HTMLElement | null>(null)
const fileInputAccept = ref('.pdf,.txt,.docx,.pptx')
const uploadMenuOpen = ref(false)
const pendingAttachment = ref<PendingAttachment | null>(null)
const loadError = ref('')
const askError = ref('')
const documentActionError = ref('')
const documentActionMessage = ref('')
const selectedDocumentId = ref('')
const questionDraft = ref('')
const isAsking = ref(false)
const isLoadingDocuments = ref(false)
const isDeletingDocument = ref(false)
const deletingDocumentId = ref('')
const focusedEvidenceIndex = ref<number | null>(null)
const documents = ref<LearningDocument[]>([])
const chatMessages = ref<DocumentMessage[]>([])

const selectedDocument = computed(() =>
  documents.value.find((document) => document.id === selectedDocumentId.value),
)

const isUploadingAttachment = computed(() => pendingAttachment.value?.status === 'uploading')
const inputPlaceholder = computed(() => selectedDocument.value ? `Ask a question about ${selectedDocument.value.title}` : 'Ask a question or attach a document')
const isBusy = computed(() => isAsking.value || isUploadingAttachment.value)
const canSubmit = computed(() => !isBusy.value && Boolean(questionDraft.value.trim() || pendingAttachment.value))
const submitLabel = computed(() => {
  if (isUploadingAttachment.value) return 'Uploading'
  if (isAsking.value) return 'Searching'
  if (pendingAttachment.value && !questionDraft.value.trim()) return 'Upload'
  return 'Ask'
})

const activeEvidenceMessage = computed(() => {
  const document = selectedDocument.value

  if (!document) {
    return null
  }

  return [...document.messages]
    .reverse()
    .find((message) => message.role === 'assistant' && message.citations?.length) ?? null
})

const activeCitations = computed(() => activeEvidenceMessage.value?.citations ?? [])
const activeEvidenceQuestion = computed(() => activeEvidenceMessage.value?.question ?? '')

const activeAnswerMeta = computed(() => {
  const document = selectedDocument.value

  if (!document) {
    return null
  }

  return [...document.messages]
    .reverse()
    .find((message) => message.role === 'assistant' && message.modelName)
})

const debugLog = (...args: unknown[]) => {
  if (import.meta.env.DEV) {
    console.log(...args)
  }
}

const debugError = (...args: unknown[]) => {
  if (import.meta.env.DEV) {
    console.error(...args)
  }
}

const createId = (prefix: string) => `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2)}`
const renderMarkdown = (content: string) => md.render(content || '')

const scrollMessagesToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const loadDocuments = async () => {
  isLoadingDocuments.value = true
  loadError.value = ''

  try {
    const response = await getDocuments()
    documents.value = response.map((document: any) => mapDocument(document))
  } catch (error: any) {
    loadError.value = error.apiMessage ?? 'Unable to load documents from backend.'
  } finally {
    isLoadingDocuments.value = false
  }
}

const toggleUploadMenu = () => {
  uploadMenuOpen.value = !uploadMenuOpen.value
}

const chooseUploadOption = (option: UploadOption) => {
  fileInputAccept.value = option.accept
  uploadMenuOpen.value = false
  fileInputRef.value?.click()
}

const handleFileChange = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  if (file) {
    stageAttachment(file)
  }

  input.value = ''
}

const stageAttachment = (file: File) => {
  const extension = file.name.split('.').pop()?.toLowerCase() ?? ''
  const supportedExtensions = ['pdf', 'txt', 'docx', 'pptx']

  askError.value = ''
  documentActionError.value = ''
  documentActionMessage.value = ''

  if (!supportedExtensions.includes(extension)) {
    askError.value = 'Unsupported file type. Please upload PDF, TXT, DOCX, or PPTX.'
    return
  }

  pendingAttachment.value = {
    file,
    name: file.name,
    type: extension.toUpperCase(),
    size: formatFileSize(file.size),
    status: 'ready_to_upload',
    progress: 0,
    error: '',
  }
}

const removeAttachment = () => {
  if (pendingAttachment.value?.status === 'uploading') return
  pendingAttachment.value = null
  askError.value = ''
}

const selectDocument = (documentId: string) => {
  selectedDocumentId.value = documentId
  askError.value = ''
  documentActionError.value = ''
  documentActionMessage.value = ''
  focusedEvidenceIndex.value = null
  debugLog('[DocumentLab] selected document id', documentId)
}

const submitDocumentInteraction = async () => {
  const question = questionDraft.value.trim()

  if (isBusy.value) return

  askError.value = ''
  documentActionError.value = ''
  documentActionMessage.value = ''

  if (!pendingAttachment.value && !selectedDocument.value) {
    askError.value = 'Upload or select a document first.'
    return
  }

  if (!pendingAttachment.value && !question) {
    return
  }

  try {
    const document = pendingAttachment.value
      ? await uploadPendingAttachment()
      : selectedDocument.value

    if (!document) {
      askError.value = 'Upload or select a document first.'
      return
    }

    if (document.backendStatus !== 'ready') {
      askError.value = `Document is not ready yet. Current status: ${document.status}.`
      return
    }

    if (!question) {
      appendMessage(document.id, {
        id: createId('system'),
        role: 'assistant',
        content: 'Document uploaded. Ask a question about this document.',
        documentId: document.id,
        documentName: document.title,
        createdAt: new Date().toISOString(),
      })
      pendingAttachment.value = null
      await scrollMessagesToBottom()
      return
    }

    await askSelectedDocument(document, question)
  } catch (error: any) {
    debugError('[DocumentLab] submit error', error)
    askError.value = error.apiMessage ?? 'Unable to process this document request.'
  }
}

const uploadPendingAttachment = async (): Promise<LearningDocument | null> => {
  const attachment = pendingAttachment.value
  if (!attachment) return selectedDocument.value ?? null

  if (attachment.status === 'ready' && attachment.uploadedDocumentId) {
    return documents.value.find((document) => document.id === attachment.uploadedDocumentId) ?? selectedDocument.value ?? null
  }

  pendingAttachment.value = {
    ...attachment,
    status: 'uploading',
    progress: 0,
    error: '',
  }

  try {
    const response = await uploadDocumentRequest({
      file: attachment.file,
      title: attachment.name.replace(/\.[^/.]+$/, ''),
      onUploadProgress: (event: any) => {
        if (!pendingAttachment.value) return

        const progress = event.lengthComputable && event.total
          ? Math.min(99, Math.round((event.loaded / event.total) * 100))
          : Math.min(99, pendingAttachment.value.progress + 10)

        pendingAttachment.value = {
          ...pendingAttachment.value,
          progress,
        }
      },
    })

    const mapped = mapDocument(response)
    documents.value = [mapped, ...documents.value.filter((document) => document.id !== mapped.id)]
    selectedDocumentId.value = mapped.id
    pendingAttachment.value = {
      ...pendingAttachment.value,
      status: 'ready',
      progress: 100,
      error: '',
      uploadedDocumentId: mapped.id,
    }

    return mapped
  } catch (error: any) {
    pendingAttachment.value = {
      ...attachment,
      status: 'failed',
      progress: 0,
      error: error.apiMessage ?? 'Upload failed. Remove this attachment and try again.',
    }
    throw error
  }
}

const askSelectedDocument = async (document: LearningDocument, question: string) => {
  const payload = { question }

  debugLog('[DocumentLab] selected document id', document.id)
  debugLog('[DocumentLab] ask payload', payload)

  appendMessage(document.id, {
    id: createId('user'),
    role: 'user',
    content: question,
    documentId: document.id,
    documentName: document.title,
    createdAt: new Date().toISOString(),
  })

  questionDraft.value = ''
  pendingAttachment.value = null
  isAsking.value = true
  await scrollMessagesToBottom()

  try {
    const response = await askDocumentQuestion(document.id, payload)
    debugLog('[DocumentLab] ask response', response)

    appendMessage(document.id, {
      id: createId('assistant'),
      role: 'assistant',
      content: response.answer ?? '',
      documentId: String(response.document_id ?? document.id),
      documentName: document.title,
      question,
      citations: mapCitations(response.citations ?? [], document),
      usedChunks: response.used_chunks ?? 0,
      modelProvider: response.model_provider ?? 'unknown',
      modelName: response.model_name ?? 'unknown',
      createdAt: new Date().toISOString(),
    })
    focusedEvidenceIndex.value = 0
    await scrollMessagesToBottom()
  } catch (error: any) {
    debugError('[DocumentLab] ask error', error)
    askError.value = error.apiMessage ?? 'Unable to ask this document.'
  } finally {
    isAsking.value = false
  }
}

const appendMessage = (documentId: string, message: DocumentMessage) => {
  const relatedDocument = documents.value.find((document) => document.id === documentId)
  const enrichedMessage: DocumentMessage = {
    ...message,
    documentId: message.documentId ?? documentId,
    documentName: message.documentName ?? relatedDocument?.title,
    createdAt: message.createdAt ?? new Date().toISOString(),
  }

  chatMessages.value = [...chatMessages.value, enrichedMessage]
  documents.value = documents.value.map((document) =>
    document.id === documentId
      ? {
          ...document,
          messages: [...document.messages, enrichedMessage],
        }
      : document,
  )
}

const sweetAlertClasses = {
  popup: 'rounded-3xl border border-white/10 bg-slate-950 text-slate-100 shadow-2xl shadow-black/40',
  title: 'text-white',
  htmlContainer: 'text-slate-300',
  actions: 'gap-3',
  confirmButton: 'rounded-2xl bg-rose-500 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-rose-400 focus:outline-none focus:ring-2 focus:ring-rose-300/40',
  cancelButton: 'rounded-2xl bg-white/10 px-5 py-2.5 text-sm font-semibold text-slate-200 transition hover:bg-white/15 focus:outline-none focus:ring-2 focus:ring-white/20',
}

const confirmDeleteDocument = async (document: LearningDocument) => {
  const result = await Swal.fire({
    title: 'Delete document?',
    text: `This will permanently remove ${document.title} and its chunks.`,
    icon: 'warning',
    background: '#111827',
    color: '#E5E7EB',
    showCancelButton: true,
    confirmButtonText: 'Delete',
    cancelButtonText: 'Cancel',
    reverseButtons: true,
    buttonsStyling: false,
    customClass: sweetAlertClasses,
  })

  return result.isConfirmed
}

const showDeleteSuccess = async () => {
  await Swal.fire({
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: 'Document deleted',
    background: '#111827',
    color: '#E5E7EB',
    showConfirmButton: false,
    timer: 2200,
    timerProgressBar: true,
    customClass: {
      popup: 'rounded-2xl border border-emerald-300/20 bg-slate-950 text-slate-100 shadow-2xl shadow-black/40',
      title: 'text-sm font-semibold text-white',
    },
  })
}

const showDeleteError = async (message: string) => {
  await Swal.fire({
    title: 'Failed to delete document',
    text: message,
    icon: 'error',
    background: '#111827',
    color: '#E5E7EB',
    confirmButtonText: 'Close',
    buttonsStyling: false,
    customClass: {
      ...sweetAlertClasses,
      confirmButton: 'rounded-2xl bg-cyan-500 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-cyan-400 focus:outline-none focus:ring-2 focus:ring-cyan-300/40',
    },
  })
}

const removeDeletedDocumentFromState = (document: LearningDocument) => {
  documents.value = documents.value.filter((item) => item.id !== document.id)
  chatMessages.value = chatMessages.value.filter((message) => message.documentId !== document.id)

  if (selectedDocumentId.value === document.id) {
    selectedDocumentId.value = ''
    focusedEvidenceIndex.value = null
  }

  if (pendingAttachment.value?.uploadedDocumentId === document.id) {
    pendingAttachment.value = null
  }
}

const deleteDocument = async (document: LearningDocument) => {
  const confirmed = await confirmDeleteDocument(document)
  if (!confirmed) return

  documentActionError.value = ''
  documentActionMessage.value = ''
  askError.value = ''
  isDeletingDocument.value = true
  deletingDocumentId.value = document.id

  try {
    await deleteDocumentRequest(document.id)
    removeDeletedDocumentFromState(document)
    documentActionMessage.value = 'Document deleted.'
    await loadDocuments()
    await showDeleteSuccess()
  } catch (error: any) {
    const status = error.response?.status
    const message = status === 404 || status === 405
      ? 'Delete endpoint is not available yet.'
      : error.apiMessage ?? 'Unable to delete this document.'

    documentActionError.value = message
    await showDeleteError(message)
  } finally {
    isDeletingDocument.value = false
    deletingDocumentId.value = ''
  }
}

const isDocumentAvailable = (documentId?: string) => {
  if (!documentId) return false
  return documents.value.some((document) => document.id === documentId)
}

const switchToMessageDocument = (message: DocumentMessage) => {
  if (!message.documentId || !isDocumentAvailable(message.documentId)) return

  selectedDocumentId.value = message.documentId
  askError.value = ''
  documentActionError.value = ''
  documentActionMessage.value = ''
  focusedEvidenceIndex.value = null
  debugLog('[DocumentLab] switched to message document id', message.documentId)
}

const focusEvidence = async (index: number) => {
  focusedEvidenceIndex.value = index
  await nextTick()
  document.getElementById(getEvidenceDomId(index))?.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
}

const getEvidenceDomId = (index: number) => `document-evidence-${index}`

const handleOutsideClick = (event: MouseEvent) => {
  if (!uploadMenuOpen.value) return

  const target = event.target as Node
  if (uploadMenuRef.value?.contains(target) || uploadButtonRef.value?.contains(target)) {
    return
  }

  uploadMenuOpen.value = false
}

const mapDocument = (document: any): LearningDocument => ({
  id: String(document.id),
  title: document.title ?? document.original_filename ?? 'Untitled document',
  originalFilename: document.original_filename ?? document.title ?? 'Untitled document',
  type: getDocumentType(document),
  size: formatFileSize(Number(document.file_size_bytes ?? 0)),
  pages: document.page_count ?? document.total_pages ?? document.total_sections ?? '-',
  chunks: Number(document.chunks_count ?? document.chunks ?? 0),
  wordCount: document.word_count ?? '-',
  uploadedAt: formatDate(document.created_at),
  status: mapStatus(document.status),
  backendStatus: String(document.status ?? '').toLowerCase(),
  summary: document.summary ?? '',
  messages: [],
})

const mapCitations = (citations: any[], document: LearningDocument): Citation[] =>
  citations.map((citation, index) => {
    const rawChunkId = String(citation.chunk_id ?? citation.id ?? citation.vector_id ?? index + 1)
    const excerpt = citation.excerpt ?? citation.text ?? citation.content ?? citation.chunk_text ?? ''
    const evidenceText = citation.chunk_text ?? citation.full_text ?? citation.text ?? citation.content ?? excerpt

    return {
      id: `${rawChunkId}-${index}`,
      source: citation.filename ?? citation.document_name ?? document.title,
      page: formatPageRange(citation.page_start, citation.page_end),
      pageStart: citation.page_start ?? null,
      pageEnd: citation.page_end ?? null,
      chunk: rawChunkId.slice(0, 8),
      score: Number(citation.score ?? 0).toFixed(4),
      excerpt,
      evidenceText,
      vectorId: citation.vector_id ? String(citation.vector_id) : undefined,
    }
  })

const getDocumentType = (document: any) => {
  const filename = document.original_filename ?? document.title ?? ''
  const extension = filename.split('.').pop()?.toUpperCase()

  if (extension && extension !== filename.toUpperCase()) {
    return extension
  }

  if (document.mime_type === 'application/pdf') return 'PDF'
  if (document.mime_type === 'text/plain') return 'TXT'
  if (document.mime_type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return 'DOCX'
  if (document.mime_type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation') return 'PPTX'
  return document.mime_type ?? 'FILE'
}

const formatFileSize = (size: number) => {
  if (!size) return '-'

  if (size < 1024 * 1024) {
    return `${Math.max(1, Math.round(size / 1024))} KB`
  }

  return `${(size / 1024 / 1024).toFixed(1)} MB`
}

const formatDate = (value?: string) => {
  if (!value) return '-'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return '-'

  return new Intl.DateTimeFormat('en', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(parsed)
}

const formatPageRange = (start?: number | string | null, end?: number | string | null) => {
  if (!start && !end) return '-'
  if (!end || start === end) return String(start ?? end)
  return `${start}-${end}`
}

const mapStatus = (status?: string): DocumentStatus => {
  const normalized = String(status ?? '').toLowerCase()
  const statuses: Record<string, DocumentStatus> = {
    uploaded: 'Uploaded',
    processing: 'Processing',
    ready: 'Ready',
    failed: 'Failed',
    archived: 'Archived',
  }

  return statuses[normalized] ?? 'Processing'
}

const getStatusClass = (status: DocumentStatus) => {
  const classes: Record<DocumentStatus, string> = {
    Uploaded: 'bg-cyan-300/10 text-cyan-100',
    Processing: 'bg-cyan-300/10 text-cyan-100',
    Ready: 'bg-emerald-300/10 text-emerald-100',
    Failed: 'bg-rose-300/10 text-rose-100',
    Archived: 'bg-slate-300/10 text-slate-100',
  }

  return classes[status]
}

const getAttachmentStatusClass = (status: AttachmentStatus) => {
  const classes: Record<AttachmentStatus, string> = {
    ready_to_upload: 'bg-cyan-300/10 text-cyan-100',
    uploading: 'bg-blue-300/10 text-blue-100',
    ready: 'bg-emerald-300/10 text-emerald-100',
    failed: 'bg-rose-300/10 text-rose-100',
  }

  return classes[status]
}

const getAttachmentStatusLabel = (attachment: PendingAttachment) => {
  const labels: Record<AttachmentStatus, string> = {
    ready_to_upload: 'ready to upload',
    uploading: `uploading ${attachment.progress}%`,
    ready: 'ready',
    failed: 'failed',
  }

  return labels[attachment.status]
}

const renderHighlightedEvidence = (text: string, question: string) => {
  const safeText = escapeHtml(text || 'No evidence text returned by backend.')
  const keywords = getQuestionKeywords(question)

  if (!keywords.length) {
    return safeText
  }

  const pattern = new RegExp(`(${keywords.map(escapeRegex).join('|')})`, 'gi')
  return safeText.replace(pattern, '<mark class="rounded bg-cyan-300/20 px-1 py-0.5 text-cyan-50">$1</mark>')
}

const getQuestionKeywords = (question: string) => {
  const stopWords = new Set([
    'apa', 'itu', 'yang', 'dan', 'atau', 'dari', 'dalam', 'untuk', 'dengan', 'pada', 'adalah', 'sebutkan',
    'the', 'and', 'or', 'from', 'with', 'what', 'why', 'how', 'is', 'are', 'about', 'this', 'that',
  ])

  return question
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .map((word) => word.trim())
    .filter((word) => word.length > 3 && !stopWords.has(word))
    .slice(0, 10)
}

const escapeHtml = (value: string) => value
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#039;')

const escapeRegex = (value: string) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
watch(selectedDocumentId, () => {
  scrollMessagesToBottom()
})

onMounted(() => {
  loadDocuments()
  document.addEventListener('click', handleOutsideClick)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleOutsideClick)
})
</script>





















