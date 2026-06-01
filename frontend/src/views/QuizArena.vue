<template>
  <div class="flex w-full min-w-0 flex-col gap-4 overflow-x-hidden xl:h-[calc(100vh-96px)] xl:overflow-hidden">
    <div v-if="errorMessage" class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100">
      {{ errorMessage }}
    </div>

    <section class="grid min-w-0 flex-1 grid-cols-1 gap-5 overflow-visible xl:min-h-0 xl:grid-cols-[minmax(360px,0.78fr)_minmax(0,1.18fr)] xl:gap-6 xl:overflow-hidden">
      <div class="contents min-w-0 xl:flex xl:h-full xl:min-h-0 xl:flex-col xl:gap-6 xl:overflow-hidden">
        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="order-1 min-w-0 xl:flex xl:max-h-[62%] xl:flex-none xl:flex-col xl:overflow-hidden">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Quiz Arena</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Generate adaptive quiz</h2>
            <p class="mt-2 text-sm leading-6 text-slate-400">
              Build practice from a topic or a selected document, then review explanations and weak topics.
            </p>
          </div>

          <form class="thin-scrollbar mt-5 grid min-w-0 gap-4 xl:min-h-0 xl:flex-1 xl:overflow-y-auto xl:pr-1" @submit.prevent="generateQuiz">
            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Source</span>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="source in sources"
                  :key="source"
                  class="min-h-10 rounded-xl border px-3 text-sm font-semibold transition"
                  :class="form.source === source ? 'border-cyan-300/35 bg-cyan-300/10 text-cyan-100' : 'border-white/10 bg-white/[0.05] text-slate-300 hover:bg-white/[0.08]'"
                  type="button"
                  @click="setSource(source)"
                >
                  {{ source }}
                </button>
              </div>
            </label>

            <label v-if="form.source === 'Topic'" class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Topic input</span>
              <input
                v-model="form.topic"
                class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                placeholder="Matrix transformations"
                required
              />
            </label>

            <div v-else class="grid min-w-0 gap-4 rounded-3xl border border-white/8 bg-white/[0.035] p-4">
              <input
                ref="documentFileInputRef"
                class="hidden"
                type="file"
                accept=".txt,.pdf,.docx,.pptx"
                @change="handleDocumentFileChange"
              />

              <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div class="min-w-0">
                  <p class="text-sm font-semibold text-white">Document source</p>
                  <p class="mt-1 text-xs leading-5 text-slate-500">Upload a file or choose one of your recent Document Lab uploads.</p>
                </div>
                <button
                  class="inline-flex min-h-10 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-not-allowed disabled:opacity-50"
                  type="button"
                  :disabled="isUploadingDocument || isGenerating"
                  @click="openDocumentPicker"
                >
                  {{ isUploadingDocument ? 'Uploading...' : 'Upload file' }}
                </button>
              </div>

              <div v-if="uploadMessage" class="rounded-2xl border border-emerald-300/20 bg-emerald-300/10 px-4 py-3 text-sm text-emerald-100">
                {{ uploadMessage }}
              </div>
              <div v-if="uploadError" class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm text-rose-100">
                {{ uploadError }}
              </div>
              <div v-if="isUploadingDocument" class="rounded-2xl border border-white/8 bg-white/[0.04] p-3">
                <div class="flex items-center justify-between gap-3 text-xs text-slate-400">
                  <span>Uploading and processing document...</span>
                  <span>{{ uploadProgress }}%</span>
                </div>
                <div class="mt-2 h-1.5 rounded-full bg-slate-800">
                  <div class="h-1.5 rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500 transition-all duration-200" :style="{ width: `${uploadProgress}%` }" />
                </div>
              </div>

              <article v-if="selectedDocument" class="rounded-2xl border border-cyan-300/25 bg-cyan-300/[0.075] p-4">
                <div class="flex min-w-0 items-start gap-3">
                  <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-xs font-bold text-cyan-100">
                    {{ selectedDocument.type }}
                  </div>
                  <div class="min-w-0 flex-1">
                    <div class="flex min-w-0 items-start justify-between gap-3">
                      <div class="min-w-0">
                        <p class="truncate text-sm font-semibold text-white">{{ selectedDocument.title }}</p>
                        <p class="mt-1 truncate text-xs text-slate-400">{{ selectedDocument.originalFilename }}</p>
                      </div>
                      <button class="shrink-0 rounded-full border border-white/10 bg-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-200 transition hover:bg-white/10" type="button" @click="removeSelectedDocument">
                        X
                      </button>
                    </div>
                    <div class="mt-3 flex flex-wrap gap-2 text-xs text-slate-300">
                      <span class="rounded-full border border-white/10 bg-white/[0.05] px-2.5 py-1">{{ selectedDocument.size }}</span>
                      <span class="rounded-full border border-white/10 bg-white/[0.05] px-2.5 py-1">{{ selectedDocument.pages }} pages</span>
                      <span class="rounded-full border border-white/10 bg-white/[0.05] px-2.5 py-1">{{ selectedDocument.chunks }} chunks</span>
                      <span :class="['rounded-full px-2.5 py-1 font-semibold', selectedDocument.status === 'ready' ? 'bg-emerald-300/10 text-emerald-100' : 'bg-amber-300/10 text-amber-100']">{{ selectedDocument.status }}</span>
                    </div>
                  </div>
                </div>
              </article>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Focus topic (optional)</span>
                <input
                  v-model="form.focusTopic"
                  class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="Optional: focus quiz on a specific section, e.g. supervised learning"
                />
              </label>

              <div class="grid min-w-0 gap-2">
                <div class="flex items-center justify-between gap-3">
                  <span class="text-sm font-medium text-slate-300">Choose from uploaded documents</span>
                  <button class="text-xs font-semibold text-cyan-100 transition hover:text-cyan-50" type="button" :disabled="isLoadingDocuments" @click="loadDocuments">
                    {{ isLoadingDocuments ? 'Loading...' : 'Refresh' }}
                  </button>
                </div>
                <div v-if="isLoadingDocuments" class="rounded-2xl border border-white/8 bg-white/[0.04] px-4 py-3 text-sm text-slate-300">
                  Loading documents...
                </div>
                <div v-else-if="documents.length === 0" class="rounded-2xl border border-dashed border-white/14 bg-white/[0.04] px-4 py-3 text-sm text-slate-400">
                  No uploaded documents yet. Upload a file above to generate from a document.
                </div>
                <div v-else class="thin-scrollbar max-h-40 space-y-2 overflow-y-auto pr-1">
                  <button
                    v-for="document in documents"
                    :key="document.id"
                    class="w-full rounded-2xl border px-3 py-2.5 text-left transition"
                    :class="selectedDocument?.id === document.id ? 'border-cyan-300/35 bg-cyan-300/10' : 'border-white/8 bg-white/[0.04] hover:border-white/16 hover:bg-white/[0.07]'"
                    type="button"
                    @click="selectDocument(document)"
                  >
                    <div class="flex items-start justify-between gap-3">
                      <span class="min-w-0 truncate text-sm font-semibold text-white">{{ document.title }}</span>
                      <span :class="['shrink-0 rounded-full px-2 py-0.5 text-[11px] font-semibold', document.status === 'ready' ? 'bg-emerald-300/10 text-emerald-100' : 'bg-amber-300/10 text-amber-100']">{{ document.status }}</span>
                    </div>
                    <p class="mt-1 truncate text-xs text-slate-500">{{ document.type }} / {{ document.size }} / {{ document.chunks }} chunks</p>
                  </button>
                </div>
              </div>
            </div>

            <div class="grid min-w-0 gap-4 sm:grid-cols-2">
              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Difficulty</span>
                <select v-model="form.difficulty" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option>Easy</option>
                  <option>Medium</option>
                  <option>Hard</option>
                  <option>Adaptive</option>
                </select>
              </label>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Number of questions</span>
                <select v-model.number="form.questionCount" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option :value="3">3 questions</option>
                  <option :value="5">5 questions</option>
                  <option :value="10">10 questions</option>
                </select>
              </label>
            </div>

            <div class="grid min-w-0 gap-4 sm:grid-cols-2">
              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Question type</span>
                <select v-model="form.questionType" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option>Multiple Choice</option>
                  <option>True/False</option>
                  <option>Short Answer</option>
                </select>
              </label>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Language</span>
                <select v-model="form.language" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option value="id">Bahasa Indonesia</option>
                  <option value="en">English</option>
                </select>
              </label>
            </div>

            <div v-if="isGenerating" class="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm text-cyan-100">
              {{ generationLoadingLabel }}
            </div>

            <GradientButton type="submit" full-width :disabled="!canGenerateQuiz">
              {{ generateButtonLabel }}
            </GradientButton>
          </form>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5" extra-class="order-4 min-w-0 xl:flex xl:flex-1 xl:flex-col xl:min-h-0 xl:overflow-hidden">
          <div class="flex items-center justify-between gap-4">
            <div class="min-w-0">
              <p class="text-sm font-medium text-violet-200/80">Quiz history</p>
              <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Previous attempts</h2>
            </div>
            <span class="shrink-0 rounded-full border border-white/10 px-3 py-1 text-xs text-slate-400">{{ quizHistory.length }}</span>
          </div>

          <div v-if="isLoadingHistory" class="mt-5 rounded-2xl border border-white/8 bg-white/[0.045] p-4 text-sm text-slate-300">
            Loading attempts...
          </div>
          <div v-else-if="quizHistory.length === 0" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-4 text-sm text-slate-400">
            No quiz attempts yet.
          </div>
          <div v-else class="thin-scrollbar mt-5 min-h-0 space-y-3 xl:flex-1 xl:overflow-y-auto xl:pr-1">
            <article v-for="item in quizHistory" :key="item.id" class="rounded-2xl border border-white/8 bg-white/[0.045] p-4 break-words">
              <div class="flex items-start justify-between gap-3">
                <div class="min-w-0">
                  <p class="truncate text-sm font-semibold text-white">{{ item.topic }}</p>
                  <p class="mt-1 text-xs text-slate-500">{{ item.date }} / {{ item.difficulty }}</p>
                </div>
                <span class="shrink-0 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1 text-sm font-semibold text-cyan-100">{{ item.score }}%</span>
              </div>
            </article>
          </div>
        </GlassCard>
      </div>

      <div class="contents min-w-0 xl:flex xl:h-full xl:min-h-0 xl:flex-col xl:gap-6 xl:overflow-hidden">
        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="order-2 min-w-0 xl:flex xl:max-h-[56%] xl:flex-none xl:flex-col xl:overflow-hidden">
          <div v-if="!activeQuiz" class="rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center">
            <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
              <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 3 4 7v6c0 5 8 8 8 8s8-3 8-8V7l-8-4Zm-2 8h4M10 15h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </div>
            <p class="mt-4 font-semibold text-white">No active quiz</p>
            <p class="mt-2 text-sm leading-6 text-slate-400">Generate a quiz to start answering questions one by one.</p>
          </div>

          <div v-else-if="!quizSubmitted" class="thin-scrollbar min-w-0 xl:min-h-0 xl:overflow-y-auto xl:pr-1">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div class="min-w-0">
                <p class="text-sm font-medium text-cyan-200/80">{{ activeQuiz.sourceLabel }}</p>
                <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">{{ activeQuiz.title }}</h2>
                <p class="mt-2 text-sm leading-6 text-slate-400">{{ activeQuiz.difficulty }} / {{ activeQuiz.questionType }}</p>
              </div>
              <div class="flex w-fit items-center gap-2 rounded-2xl border border-white/10 bg-white/[0.06] px-3 py-2 text-sm font-semibold text-white">
                <svg class="h-4 w-4 text-cyan-200" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M12 7v5l3 2M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                {{ formattedTimer }}
              </div>
            </div>

            <div class="mt-5 rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <div class="flex items-center justify-between gap-4 text-sm">
                <span class="text-slate-400">Question {{ currentQuestionIndex + 1 }} of {{ activeQuiz.questions.length }}</span>
                <span class="font-semibold text-white">{{ answeredCount }} answered</span>
              </div>
              <div class="mt-3 h-2 rounded-full bg-slate-800">
                <div class="h-2 rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500 transition-all duration-300" :style="{ width: `${questionProgress}%` }" />
              </div>
            </div>

            <article class="mt-5 rounded-3xl border border-white/8 bg-white/[0.045] p-4 sm:p-5">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">{{ currentQuestion.topic }}</p>
                  <h3 class="mt-2 text-base font-semibold leading-7 text-white sm:text-lg">{{ currentQuestion.prompt }}</h3>
                </div>
                <span class="shrink-0 rounded-full bg-white/[0.06] px-3 py-1 text-xs font-semibold text-slate-300">{{ currentQuestion.points }} pt</span>
              </div>

              <div v-if="currentQuestion.type !== 'Short Answer'" class="mt-5 grid gap-3">
                <button
                  v-for="option in currentQuestion.options"
                  :key="option.id"
                  class="min-w-0 rounded-2xl border p-4 text-left text-sm transition"
                  :class="answers[currentQuestion.id] === option.value ? 'border-cyan-300/40 bg-cyan-300/10 text-cyan-100' : 'border-white/10 bg-white/[0.04] text-slate-300 hover:border-white/18 hover:bg-white/[0.07]'"
                  type="button"
                  @click="selectAnswer(currentQuestion.id, option.value)"
                >
                  <span class="font-semibold">{{ option.id }}.</span>
                  <span class="ml-2">{{ option.text }}</span>
                </button>
              </div>

              <textarea
                v-else
                :value="answers[currentQuestion.id] ?? ''"
                class="thin-scrollbar mt-5 min-h-32 w-full min-w-0 resize-none rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                placeholder="Write your short answer here"
                @input="selectAnswer(currentQuestion.id, ($event.target as HTMLTextAreaElement).value)"
              />
            </article>

            <div class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <button class="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50" type="button" :disabled="currentQuestionIndex === 0" @click="previousQuestion">
                Previous
              </button>

              <div class="flex flex-col gap-3 sm:flex-row">
                <button class="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50" type="button" :disabled="currentQuestionIndex === activeQuiz.questions.length - 1" @click="nextQuestion">
                  Next
                </button>
                <GradientButton type="button" @click="submitActiveQuiz">
                  {{ isSubmitting ? 'Submitting...' : 'Submit Quiz' }}
                </GradientButton>
              </div>
            </div>
          </div>

          <div v-else class="thin-scrollbar min-w-0 xl:min-h-0 xl:overflow-y-auto xl:pr-1">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div class="min-w-0">
                <p class="text-sm font-medium text-emerald-200/80">Quiz result</p>
                <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">{{ activeQuiz.title }}</h2>
                <p class="mt-2 text-sm leading-6 text-slate-400">{{ resultSummary.recommendation }}</p>
              </div>
              <span class="w-fit rounded-full border border-emerald-300/20 bg-emerald-300/10 px-4 py-2 text-lg font-semibold text-emerald-100">{{ resultSummary.score }}%</span>
            </div>

            <div class="mt-6 grid gap-3 sm:grid-cols-3">
              <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4 break-words">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Correct</p>
                <p class="mt-2 text-2xl font-semibold text-white">{{ resultSummary.correct }}</p>
              </div>
              <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4 break-words">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Wrong</p>
                <p class="mt-2 text-2xl font-semibold text-white">{{ resultSummary.wrong }}</p>
              </div>
              <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4 break-words">
                <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Answered</p>
                <p class="mt-2 text-2xl font-semibold text-white">{{ answeredCount }}/{{ activeQuiz.questions.length }}</p>
              </div>
            </div>

            <section class="mt-6 rounded-2xl border border-amber-300/18 bg-amber-300/10 p-4">
              <p class="text-sm font-semibold text-white">Weak topics detected</p>
              <div v-if="resultSummary.weakTopics.length" class="mt-3 flex flex-wrap gap-2">
                <span v-for="topic in resultSummary.weakTopics" :key="topic" class="rounded-full border border-amber-300/20 bg-amber-300/10 px-3 py-1 text-xs font-medium text-amber-100">{{ topic }}</span>
              </div>
              <p v-else class="mt-3 text-sm text-slate-400">No weak topics detected in this attempt.</p>
              <div v-if="resultSummary.reviews.length" class="mt-4 space-y-2">
                <p v-for="review in resultSummary.reviews" :key="review" class="text-sm leading-6 text-slate-300">{{ review }}</p>
              </div>
            </section>
          </div>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="order-3 min-w-0 xl:flex xl:flex-1 xl:flex-col xl:min-h-0 xl:overflow-hidden">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Review</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Explanation per question</h2>
          </div>

          <div v-if="activeQuiz && quizSubmitted" class="thin-scrollbar mt-5 min-h-0 space-y-4 xl:flex-1 xl:overflow-y-auto xl:pr-1">
            <article v-for="question in activeQuiz.questions" :key="question.id" class="rounded-2xl border border-white/8 bg-white/[0.045] p-4 break-words">
              <div class="flex items-start justify-between gap-4">
                <div class="min-w-0">
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">{{ question.topic }}</p>
                  <h3 class="mt-2 break-words text-sm font-semibold leading-6 text-white">{{ question.prompt }}</h3>
                </div>
                <span :class="['shrink-0 rounded-full px-3 py-1 text-xs font-semibold', isQuestionCorrect(question) ? 'bg-emerald-300/10 text-emerald-100' : 'bg-rose-300/10 text-rose-100']">
                  {{ isQuestionCorrect(question) ? 'Correct' : 'Review' }}
                </span>
              </div>
              <p class="mt-3 break-words text-sm leading-6 text-slate-400">{{ explanationFor(question) }}</p>
              <p class="mt-3 break-words text-xs text-slate-500">Your answer: {{ formatAnswer(question, answers[question.id]) }} / Correct: {{ correctAnswerFor(question) }}</p>
            </article>
          </div>
          <div v-else class="mt-5 flex min-h-28 items-center justify-center rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-4 text-center text-sm leading-6 text-slate-400 xl:flex-1">
            Submit a quiz to review explanations here.
          </div>
        </GlassCard>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'

import GlassCard from '../components/GlassCard.vue'
import GradientButton from '../components/GradientButton.vue'
import { REQUEST_TIMEOUT_MESSAGE } from '../services/api'
import { getDocuments, uploadDocument } from '../services/documentService'
import { generateQuiz as generateQuizApi, getRecentAttempts, submitQuiz as submitQuizApi } from '../services/quizService'

type QuizSource = 'Topic' | 'Document'
type QuestionType = 'Multiple Choice' | 'True/False' | 'Short Answer'
type QuizLanguage = 'id' | 'en'

interface QuizQuestion {
  id: string
  type: QuestionType
  prompt: string
  topic: string
  points: number
  options: Array<{ id: string; text: string; value: string }>
  correctAnswer: string
  explanation: string
}

interface ActiveQuiz {
  id: string
  title: string
  sourceLabel: string
  difficulty: string
  questionType: QuestionType
  questions: QuizQuestion[]
}

interface QuizDocument {
  id: string
  title: string
  originalFilename: string
  type: string
  size: string
  pages: number | string
  chunks: number
  status: string
}

const sources: QuizSource[] = ['Topic', 'Document']
const form = reactive({ source: 'Topic' as QuizSource, topic: 'Matrix transformations', focusTopic: '', difficulty: 'Adaptive', questionCount: 5, questionType: 'Multiple Choice' as QuestionType, language: 'id' as QuizLanguage })
const documentFileInputRef = ref<HTMLInputElement | null>(null)
const documents = ref<QuizDocument[]>([])
const selectedDocument = ref<QuizDocument | null>(null)
const isLoadingDocuments = ref(false)
const isUploadingDocument = ref(false)
const uploadProgress = ref(0)
const uploadError = ref('')
const uploadMessage = ref('')
const activeQuiz = ref<ActiveQuiz | null>(null)
const currentQuestionIndex = ref(0)
const answers = reactive<Record<string, string>>({})
const quizSubmitted = ref(false)
const elapsedSeconds = ref(0)
const quizHistory = ref<Array<{ id: string; topic: string; score: number; date: string; difficulty: string }>>([])
const attemptResult = ref<any | null>(null)
const isGenerating = ref(false)
const isSubmitting = ref(false)
const isLoadingHistory = ref(false)
const errorMessage = ref('')
let timer: number | undefined

const emptyQuestion: QuizQuestion = { id: 'empty', type: 'Multiple Choice', prompt: '', topic: '', points: 0, options: [], correctAnswer: '', explanation: '' }
const currentQuestion = computed(() => activeQuiz.value?.questions[currentQuestionIndex.value] ?? emptyQuestion)
const answeredCount = computed(() => activeQuiz.value?.questions.filter((question) => Boolean(answers[question.id]?.trim())).length ?? 0)
const questionProgress = computed(() => (activeQuiz.value ? Math.round(((currentQuestionIndex.value + 1) / activeQuiz.value.questions.length) * 100) : 0))
const formattedTimer = computed(() => `${String(Math.floor(elapsedSeconds.value / 60)).padStart(2, '0')}:${String(elapsedSeconds.value % 60).padStart(2, '0')}`)
const canGenerateQuiz = computed(() => {
  if (isGenerating.value || isUploadingDocument.value) return false
  if (form.source === 'Topic') return Boolean(form.topic.trim())
  return Boolean(selectedDocument.value)
})
const generationLoadingLabel = computed(() => (form.source === 'Document' ? 'Generating quiz from document...' : 'Generating quiz...'))
const generateButtonLabel = computed(() => {
  if (isUploadingDocument.value) return 'Uploading document...'
  if (isGenerating.value) return generationLoadingLabel.value
  if (form.source === 'Document') return activeQuiz.value ? 'Regenerate from Document' : 'Generate from Document'
  return activeQuiz.value ? 'Regenerate Quiz' : 'Generate Quiz'
})

const resultSummary = computed(() => {
  if (!attemptResult.value) return { score: 0, correct: 0, wrong: 0, weakTopics: [], reviews: [], recommendation: 'Generate a quiz to see recommendations.' }
  const reviews = attemptResult.value.recommended_review ?? []
  return {
    score: Math.round(Number(attemptResult.value.score ?? 0)),
    correct: Number(attemptResult.value.correct_count ?? 0),
    wrong: Number(attemptResult.value.wrong_count ?? 0),
    weakTopics: attemptResult.value.weak_topics ?? [],
    reviews,
    recommendation: reviews[0] ?? (Number(attemptResult.value.score ?? 0) >= 80 ? 'Great work. Try a harder quiz next.' : 'Review weak topics, then retry a focused quiz.'),
  }
})

const toSnakeQuestionType = (value: QuestionType) => value.toLowerCase().replace('/', '_').replace(/\s+/g, '_')
const toQuestionLabel = (value: string): QuestionType => {
  if (value === 'true_false') return 'True/False'
  if (value === 'short_answer') return 'Short Answer'
  return 'Multiple Choice'
}
const formatDate = (value?: string) => {
  if (!value) return 'Just now'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return 'Just now'
  return new Intl.DateTimeFormat('en', { month: 'short', day: 'numeric' }).format(parsed)
}
const optionLetter = (index: number) => String.fromCharCode(65 + index)
const requestErrorMessage = (error: any, fallback: string) => (error?.code === 'ECONNABORTED' ? REQUEST_TIMEOUT_MESSAGE : (error?.apiMessage ?? fallback))

const mapQuiz = (quiz: any): ActiveQuiz => ({
  id: String(quiz.id),
  title: quiz.title ?? 'Generated Quiz',
  sourceLabel: `${quiz.source_type ?? 'topic'}: ${quiz.topic ?? 'General Topic'}`,
  difficulty: quiz.difficulty ?? 'medium',
  questionType: toQuestionLabel(quiz.question_type ?? 'multiple_choice'),
  questions: (quiz.questions ?? []).map((question: any, index: number) => ({
    id: String(question.id),
    type: toQuestionLabel(question.question_type ?? quiz.question_type ?? 'multiple_choice'),
    prompt: question.question_text ?? '',
    topic: question.topic ?? quiz.topic ?? 'General',
    points: 1,
    options: (question.options ?? []).map((option: string, optionIndex: number) => ({ id: optionLetter(optionIndex), text: String(option), value: String(option) })),
    correctAnswer: question.correct_answer ?? '',
    explanation: question.explanation ?? 'Explanation will appear after submission.',
    order: question.order_index ?? index,
  })),
})

const mapAttempt = (attempt: any) => ({
  id: String(attempt.id),
  topic: attempt.quiz_title ?? 'Quiz attempt',
  score: Math.round(Number(attempt.score ?? 0)),
  date: formatDate(attempt.submitted_at ?? attempt.created_at),
  difficulty: attempt.difficulty ?? 'Recent',
})

const formatFileSize = (size: number) => {
  if (!size) return '-'
  if (size < 1024 * 1024) return `${Math.max(1, Math.round(size / 1024))} KB`
  return `${(size / 1024 / 1024).toFixed(1)} MB`
}

const getDocumentType = (document: any) => {
  const filename = document.original_filename ?? document.title ?? ''
  const extension = filename.split('.').pop()?.toUpperCase()
  if (extension && extension !== filename.toUpperCase()) return extension
  if (document.mime_type === 'application/pdf') return 'PDF'
  if (document.mime_type === 'text/plain') return 'TXT'
  if (document.mime_type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return 'DOCX'
  if (document.mime_type === 'application/vnd.openxmlformats-officedocument.presentationml.presentation') return 'PPTX'
  return document.mime_type ?? 'FILE'
}

const mapDocument = (document: any): QuizDocument => ({
  id: String(document.id),
  title: document.title ?? document.original_filename ?? 'Untitled document',
  originalFilename: document.original_filename ?? document.title ?? 'Untitled document',
  type: getDocumentType(document),
  size: formatFileSize(Number(document.file_size_bytes ?? 0)),
  pages: document.page_count ?? document.total_pages ?? document.total_sections ?? '-',
  chunks: Number(document.chunks_count ?? document.chunks ?? 0),
  status: String(document.status ?? 'processing').toLowerCase(),
})

const setSource = (source: QuizSource) => {
  form.source = source
  errorMessage.value = ''
  uploadError.value = ''
  uploadMessage.value = ''
  if (source === 'Document' && documents.value.length === 0) {
    loadDocuments()
  }
}

const openDocumentPicker = () => {
  uploadError.value = ''
  uploadMessage.value = ''
  documentFileInputRef.value?.click()
}

const handleDocumentFileChange = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  input.value = ''
  if (!file) return

  const extension = file.name.split('.').pop()?.toLowerCase() ?? ''
  if (!['txt', 'pdf', 'docx', 'pptx'].includes(extension)) {
    uploadError.value = 'Unsupported file type. Please upload TXT, PDF, DOCX, or PPTX.'
    return
  }

  isUploadingDocument.value = true
  uploadProgress.value = 0
  uploadError.value = ''
  uploadMessage.value = ''
  errorMessage.value = ''

  try {
    const uploaded = await uploadDocument({
      file,
      title: file.name.replace(/\.[^/.]+$/, ''),
      onUploadProgress: (progressEvent: any) => {
        uploadProgress.value = progressEvent.lengthComputable && progressEvent.total
          ? Math.min(99, Math.round((progressEvent.loaded / progressEvent.total) * 100))
          : Math.min(99, uploadProgress.value + 10)
      },
    })
    const mapped = mapDocument(uploaded)
    documents.value = [mapped, ...documents.value.filter((document) => document.id !== mapped.id)]
    selectedDocument.value = mapped
    uploadProgress.value = 100
    uploadMessage.value = 'Document ready for quiz.'
  } catch (error: any) {
    uploadError.value = requestErrorMessage(error, 'Unable to upload document for quiz.')
  } finally {
    isUploadingDocument.value = false
  }
}

const loadDocuments = async () => {
  isLoadingDocuments.value = true
  try {
    documents.value = (await getDocuments()).map(mapDocument)
    if (selectedDocument.value) {
      selectedDocument.value = documents.value.find((document) => document.id === selectedDocument.value?.id) ?? selectedDocument.value
    }
  } catch (error: any) {
    uploadError.value = requestErrorMessage(error, 'Unable to load uploaded documents.')
  } finally {
    isLoadingDocuments.value = false
  }
}

const selectDocument = (document: QuizDocument) => {
  selectedDocument.value = document
  uploadError.value = ''
  uploadMessage.value = 'Document selected for quiz.'
}

const removeSelectedDocument = () => {
  selectedDocument.value = null
  uploadMessage.value = ''
}

const loadRecentAttempts = async () => {
  isLoadingHistory.value = true
  try {
    quizHistory.value = (await getRecentAttempts()).map(mapAttempt)
  } catch (error: any) {
    errorMessage.value = requestErrorMessage(error, 'Unable to load quiz attempts.')
  } finally {
    isLoadingHistory.value = false
  }
}

const generateQuiz = async () => {
  if (form.source === 'Topic' && !form.topic.trim()) {
    errorMessage.value = 'Topic is required to generate a topic quiz.'
    return
  }

  if (form.source === 'Document' && !selectedDocument.value) {
    errorMessage.value = 'Upload or select a document first.'
    return
  }

  if (form.source === 'Document' && selectedDocument.value?.status !== 'ready') {
    errorMessage.value = `Selected document is not ready yet. Current status: ${selectedDocument.value?.status}.`
    return
  }

  stopTimer()
  Object.keys(answers).forEach((key) => delete answers[key])
  isGenerating.value = true
  errorMessage.value = ''
  attemptResult.value = null
  try {
    const focusTopic = form.focusTopic.trim()
    const payload = form.source === 'Document'
      ? {
          source_type: 'document',
          document_id: selectedDocument.value?.id,
          source_id: selectedDocument.value?.id,
          focus_topic: focusTopic || undefined,
          topic: focusTopic || undefined,
          difficulty: form.difficulty,
          question_type: toSnakeQuestionType(form.questionType),
          language: form.language,
          total_questions: form.questionCount,
        }
      : {
          source_type: 'topic',
          topic: form.topic.trim(),
          difficulty: form.difficulty,
          question_type: toSnakeQuestionType(form.questionType),
          language: form.language,
          total_questions: form.questionCount,
        }

    const quiz = await generateQuizApi(payload)
    activeQuiz.value = mapQuiz(quiz)
    currentQuestionIndex.value = 0
    quizSubmitted.value = false
    elapsedSeconds.value = 0
    startTimer()
  } catch (error: any) {
    errorMessage.value = requestErrorMessage(error, 'Unable to generate quiz.')
  } finally {
    isGenerating.value = false
  }
}

const submitActiveQuiz = async () => {
  if (!activeQuiz.value) return
  isSubmitting.value = true
  errorMessage.value = ''
  try {
    attemptResult.value = await submitQuizApi(activeQuiz.value.id, answers)
    quizSubmitted.value = true
    stopTimer()
    await loadRecentAttempts()
  } catch (error: any) {
    errorMessage.value = requestErrorMessage(error, 'Unable to submit quiz.')
  } finally {
    isSubmitting.value = false
  }
}

const selectAnswer = (questionId: string, answer: string) => {
  answers[questionId] = answer
}
const nextQuestion = () => {
  if (activeQuiz.value) currentQuestionIndex.value = Math.min(currentQuestionIndex.value + 1, activeQuiz.value.questions.length - 1)
}
const previousQuestion = () => {
  currentQuestionIndex.value = Math.max(currentQuestionIndex.value - 1, 0)
}
const answerResultFor = (question: QuizQuestion) => (attemptResult.value?.answers ?? []).find((answer: any) => String(answer.question_id) === question.id)
const isQuestionCorrect = (question: QuizQuestion) => Boolean(answerResultFor(question)?.is_correct)
const explanationFor = (question: QuizQuestion) => answerResultFor(question)?.explanation ?? question.explanation
const correctAnswerFor = (question: QuizQuestion) => answerResultFor(question)?.correct_answer ?? question.correctAnswer
const formatAnswer = (question: QuizQuestion, answer?: string) => {
  if (!answer) return 'Not answered'
  const option = question.options.find((item) => item.value === answer)
  return option ? `${option.id}. ${option.text}` : answer
}
const startTimer = () => {
  timer = window.setInterval(() => {
    elapsedSeconds.value += 1
  }, 1000)
}
const stopTimer = () => {
  if (timer) window.clearInterval(timer)
  timer = undefined
}

onMounted(() => {
  loadRecentAttempts()
  loadDocuments()
})
onBeforeUnmount(stopTimer)
</script>








