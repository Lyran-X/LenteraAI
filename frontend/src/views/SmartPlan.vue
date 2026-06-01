<template>
  <div class="w-full min-w-0 space-y-6 overflow-x-hidden">
    <div v-if="errorMessage" class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="rounded-2xl border border-emerald-300/20 bg-emerald-300/10 px-4 py-3 text-sm font-medium text-emerald-100">
      {{ successMessage }}
    </div>

    <section class="grid min-w-0 grid-cols-1 gap-6 xl:grid-cols-[minmax(360px,0.86fr)_minmax(0,1.14fr)]">
      <div class="min-w-0 space-y-6">
        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Smart Plan Generator</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Personalize your learning path</h2>
            <p class="mt-2 text-sm leading-6 text-slate-400">
              Set your goal, pace, and weak topics to generate an adaptive quest plan from the backend.
            </p>
          </div>

          <form class="mt-5 grid min-w-0 gap-4" @submit.prevent="generatePlan">
            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Learning Goal</span>
              <input
                v-model="form.learningGoal"
                class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                placeholder="Master machine learning fundamentals"
                required
              />
            </label>

            <div class="grid min-w-0 gap-4 sm:grid-cols-2">
              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Subject</span>
                <input
                  v-model="form.subject"
                  class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="Artificial Intelligence"
                  required
                />
              </label>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Topic</span>
                <input
                  v-model="form.topic"
                  class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                  placeholder="Supervised learning"
                  required
                />
              </label>
            </div>

            <div class="grid min-w-0 gap-4 sm:grid-cols-2">
              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Current Understanding Level</span>
                <select v-model="form.level" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </label>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Deadline Date</span>
                <input v-model="form.deadline" class="min-w-0 rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none" type="date" />
              </label>
            </div>

            <div class="grid min-w-0 gap-4 sm:grid-cols-2">
              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Study Duration per Day</span>
                <select v-model.number="form.duration" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option :value="25">25 minutes</option>
                  <option :value="45">45 minutes</option>
                  <option :value="60">60 minutes</option>
                  <option :value="90">90 minutes</option>
                </select>
              </label>

              <label class="grid min-w-0 gap-2">
                <span class="text-sm font-medium text-slate-300">Preferred Learning Style</span>
                <select v-model="form.learningStyle" class="min-w-0 rounded-2xl border border-white/10 bg-slate-950 px-4 py-3 text-sm text-white focus:border-cyan-300/50 focus:outline-none">
                  <option value="step_by_step">Step-by-step</option>
                  <option value="visual_examples">Visual examples</option>
                  <option value="practice_first">Practice first</option>
                  <option value="socratic_questioning">Socratic questioning</option>
                </select>
              </label>
            </div>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Weak Topics</span>
              <textarea
                v-model="form.weakTopics"
                class="thin-scrollbar min-h-24 min-w-0 resize-none rounded-2xl border border-white/10 bg-white/[0.06] px-4 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:border-cyan-300/50 focus:outline-none"
                placeholder="Gradient descent, overfitting, model evaluation"
              />
            </label>

            <div v-if="isGenerating" class="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm font-medium text-cyan-100">
              Generating quest plan with AI. This may take a moment...
            </div>

            <div class="flex flex-col gap-3 sm:flex-row">
              <GradientButton type="submit" full-width :disabled="isGenerating || !canGenerate">
                {{ isGenerating ? 'Generating...' : activePlan ? 'Regenerate Plan' : 'Generate Plan' }}
              </GradientButton>
              <button class="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10" type="button" @click="resetForm">
                Reset
              </button>
            </div>
          </form>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5" extra-class="min-w-0">
          <div class="flex items-center justify-between gap-4">
            <div class="min-w-0">
              <p class="text-sm font-medium text-violet-200/80">Saved plans</p>
              <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Plan history</h2>
            </div>
            <button class="shrink-0 rounded-xl border border-white/10 bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-200 transition hover:bg-white/10" type="button" @click="loadPlans">
              Refresh
            </button>
          </div>

          <div v-if="isLoadingPlan" class="mt-4 rounded-2xl border border-white/8 bg-white/[0.045] p-4 text-sm text-slate-300">
            Loading plans...
          </div>
          <div v-else-if="plans.length === 0" class="mt-4 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-4 text-sm text-slate-400">
            No saved study plans yet.
          </div>
          <div v-else class="thin-scrollbar mt-4 max-h-72 space-y-3 overflow-y-auto pr-1">
            <article
              v-for="plan in plans"
              :key="plan.id"
              class="flex w-full items-start gap-3 rounded-2xl border px-4 py-3 transition"
              :class="activePlan?.id === plan.id ? 'border-cyan-300/35 bg-cyan-300/10' : 'border-white/8 bg-white/[0.045] hover:border-white/16 hover:bg-white/[0.07]'"
            >
              <button class="min-w-0 flex-1 text-left disabled:cursor-wait disabled:opacity-70" type="button" :disabled="deletingPlanId === plan.id" @click="selectPlan(plan.id)">
                <div class="min-w-0">
                  <div class="flex min-w-0 flex-wrap items-center gap-2">
                    <p class="min-w-0 flex-1 truncate text-sm font-semibold text-white">{{ plan.title }}</p>
                    <span v-if="plan.status === 'active'" class="shrink-0 rounded-full border border-cyan-300/20 bg-cyan-300/10 px-2 py-0.5 text-[11px] font-semibold text-cyan-100">Active</span>
                  </div>
                  <p class="mt-1 truncate text-xs text-slate-500">{{ plan.subject }} / {{ plan.topic }}</p>
                </div>
              </button>

              <div class="flex shrink-0 items-start gap-2">
                <span class="rounded-full border border-white/10 px-2.5 py-1 text-xs font-semibold text-slate-300">{{ plan.progressPercentage }}%</span>
                <button
                  class="inline-flex h-8 w-8 items-center justify-center rounded-xl border border-rose-300/15 bg-rose-300/10 text-rose-100 transition hover:border-rose-300/30 hover:bg-rose-300/15 disabled:cursor-wait disabled:opacity-60"
                  type="button"
                  :aria-label="`Delete ${plan.title}`"
                  :disabled="deletingPlanId === plan.id"
                  @click.stop="confirmDeletePlan(plan)"
                >
                  <svg v-if="deletingPlanId !== plan.id" class="h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M4 7h16" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    <path d="M10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    <path d="M6 7l1 13h10l1-13M9 7V4h6v3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                  <span v-else class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-rose-100/30 border-t-rose-100" />
                </button>
              </div>
            </article>
          </div>
        </GlassCard>
      </div>

      <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0 overflow-hidden">
        <div class="text-center">
          <p class="bg-gradient-to-r from-cyan-200 via-blue-200 to-violet-200 bg-clip-text text-2xl font-semibold text-transparent sm:text-3xl">
            Learning Growth
          </p>
          <h2 class="mx-auto mt-2 max-w-3xl truncate text-base font-semibold text-white sm:text-lg">
            {{ activePlan?.title ?? 'Generate your first quest plan' }}
          </h2>
          <p class="mx-auto mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            {{ activePlan?.learningGoal || activePlan?.description || planStatusText }}
          </p>
        </div>

        <div v-if="isLoadingPlan && !activePlan" class="mt-6 rounded-2xl border border-white/10 bg-white/[0.045] p-6 text-center text-sm font-medium text-slate-300">
          Loading active quest plan...
        </div>

        <div v-else-if="!activePlan" class="mt-6 rounded-3xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center">
          <div class="tree-lottie-empty mx-auto">
            <div class="plant-icon sprout" aria-hidden="true">
              <span class="plant-leaf plant-leaf-left"></span>
              <span class="plant-leaf plant-leaf-right"></span>
              <span class="plant-stem"></span>
              <span class="plant-pot"></span>
            </div>
          </div>
          <p class="mt-4 font-semibold text-white">Growth dashboard is waiting</p>
          <p class="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">
            Generate a plan to see daily energy, streak, focus time, and quest progress here.
          </p>
        </div>

        <div v-else class="mt-6 space-y-5">
          <section class="grid min-w-0 gap-3 sm:grid-cols-2 xl:grid-cols-4">
            <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Streak</p>
              <div class="mt-2 flex items-center justify-center gap-3 sm:justify-start">
                <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-cyan-100">
                  <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M12 21c3.5 0 6-2.4 6-5.8 0-2.2-1.1-4.1-3.1-5.9-.6-.6-1.1-1.4-1.3-2.3-.2-.9-.9-1.5-1.7-.8-1.7 1.5-2.8 3.1-3.2 4.9-.8-.5-1.4-1.3-1.8-2.2-.2-.5-.8-.6-1.1-.1C4.7 10.5 4 12.7 4 15.1 4 18.6 6.5 21 12 21Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" />
                    <path d="M12 18.6c1.5 0 2.5-1 2.5-2.3 0-1-.5-1.8-1.4-2.6-.5-.4-.8-.9-.9-1.4-.8.7-1.4 1.5-1.6 2.4-.4-.2-.8-.6-1.1-1.1-.3.7-.5 1.5-.5 2.5 0 1.5 1.1 2.5 3 2.5Z" fill="currentColor" opacity="0.45" />
                  </svg>
                </span>
                <p class="text-lg font-semibold text-white">{{ streakCount }} day streak</p>
              </div>
            </div>
            <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Focus time</p>
              <p class="mt-2 text-lg font-semibold text-white">{{ totalMinutes }} min</p>
            </div>
            <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Quests</p>
              <p class="mt-2 text-lg font-semibold text-white">{{ totalDays }} total</p>
            </div>
            <div class="rounded-2xl border border-white/8 bg-white/[0.045] p-4">
              <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Completed</p>
              <p class="mt-2 text-lg font-semibold text-white">{{ completedDays }} quests</p>
            </div>
          </section>

          <section class="tree-growth-scene">
            <div class="tree-energy-overlay">
              <div class="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p class="text-xs font-semibold uppercase tracking-[0.14em] text-slate-500">Daily Energy</p>
                  <p class="mt-1 text-sm font-medium text-slate-200">{{ completedDays }}/{{ totalDays }} completed</p>
                </div>
                <div class="flex flex-wrap items-center gap-2 text-xs font-semibold text-cyan-100">
                  <span class="rounded-full border border-cyan-300/20 bg-cyan-300/10 px-3 py-1">{{ treeProgressPercentage }}%</span>
                </div>
              </div>
              <div class="mt-3 h-3 rounded-full bg-slate-900/80 p-0.5">
                <div class="h-full rounded-full bg-gradient-to-r from-cyan-300 via-blue-500 to-violet-500 transition-all duration-500 ease-out" :style="{ width: `${treeProgressPercentage}%` }" />
              </div>
              <p class="mt-2 text-xs text-slate-400">
                {{ treeProgressPercentage >= 100 ? 'Energy full for today!' : 'Complete quests to grow your learning tree.' }}
              </p>
            </div>

            <div class="tree-lottie-stage mt-5">
              <div v-show="!lottieLoadFailed" class="tree-lottie-scale" aria-hidden="true">
                <div ref="treeLottieContainer" class="tree-lottie-canvas"></div>
              </div>
              <div v-if="lottieLoadFailed" class="tree-lottie-fallback">
                <div :class="['plant-icon', plantVisual.stage]" aria-hidden="true">
                  <span class="plant-canopy plant-canopy-left"></span>
                  <span class="plant-canopy plant-canopy-right"></span>
                  <span class="plant-leaf plant-leaf-left"></span>
                  <span class="plant-leaf plant-leaf-right"></span>
                  <span class="plant-stem"></span>
                  <span class="plant-pot"></span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </GlassCard>
    </section>

    <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0 overflow-hidden">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div class="min-w-0">
          <p class="text-sm font-medium text-cyan-200/80">Today's Quests</p>
          <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Learning Quests Kanban</h2>
          <p class="mt-2 text-sm leading-6 text-slate-400">
            Move quests from AI recommendations into active learning, then mark them as mastered when complete.
          </p>
        </div>
        <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
          {{ plans.length }} saved plans
        </span>
      </div>

      <div v-if="isLoadingPlan && !activePlan" class="mt-5 rounded-2xl border border-white/10 bg-white/[0.045] p-5 text-sm text-slate-300">
        Loading quests...
      </div>
      <div v-else-if="!activePlan" class="mt-5 rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-6 text-center">
        <p class="font-semibold text-white">No active quests yet</p>
        <p class="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">Generate or select a study plan to show today's learning quests.</p>
      </div>
      <div v-else class="mt-5 space-y-4">
        <div class="grid min-w-0 gap-4 xl:grid-cols-3">
          <section
            v-for="column in kanbanColumns"
            :key="column.id"
            class="kanban-column rounded-3xl border border-white/10 bg-white/[0.035] p-4 transition"
            :class="dragOverColumn === column.id ? 'border-cyan-300/35 bg-cyan-300/[0.07]' : ''"
            @dragover.prevent="dragOverColumn = column.id"
            @dragleave="dragOverColumn = ''"
            @drop="handleKanbanDrop(column.id, $event)"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <p class="text-sm font-semibold text-white">{{ column.title }}</p>
                <p class="mt-1 text-xs leading-5 text-slate-500">{{ column.description }}</p>
              </div>
              <span class="shrink-0 rounded-full border border-white/10 bg-white/[0.06] px-2.5 py-1 text-xs font-semibold text-slate-300">
                {{ column.tasks.length }}
              </span>
            </div>

            <div class="thin-scrollbar mt-4 min-h-72 max-h-[34rem] space-y-3 overflow-y-auto pr-1">
              <div v-if="column.tasks.length === 0" class="rounded-2xl border border-dashed border-white/12 bg-white/[0.025] p-4 text-sm leading-6 text-slate-500">
                {{ column.emptyText }}
              </div>

              <article
                v-for="task in column.tasks"
                :key="task.id"
                class="kanban-quest-card relative rounded-2xl border p-4 transition-all duration-300"
                :class="[
                  task.completed ? 'border-emerald-300/25 bg-emerald-300/[0.08]' : 'border-white/8 bg-white/[0.045] hover:border-cyan-300/25 hover:bg-white/[0.07]',
                  celebrationTaskId === task.id ? 'quest-complete-pulse' : '',
                ]"
                draggable="true"
                @dragstart="handleKanbanDragStart(task, $event)"
                @dragend="handleKanbanDragEnd"
              >
                <div
                  v-if="energyFeedback?.taskId === task.id"
                  class="quest-energy-pop pointer-events-none absolute right-4 top-4 z-20 rounded-full border border-cyan-300/25 bg-cyan-300/15 px-3 py-1 text-xs font-semibold text-cyan-100 shadow-lg shadow-cyan-500/10"
                >
                  +{{ energyFeedback.points }} energy
                </div>
                <div v-if="celebrationTaskId === task.id" class="pointer-events-none absolute inset-0 z-10 overflow-hidden">
                  <span
                    v-for="piece in confettiPieces"
                    :key="piece.id"
                    class="quest-confetti-piece"
                    :style="{ left: piece.left, top: piece.top, backgroundColor: piece.color, animationDelay: piece.delay }"
                  />
                </div>

                <div class="relative z-0 min-w-0">
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <div class="flex flex-wrap items-center gap-2">
                        <span class="rounded-full border border-white/10 bg-white/[0.055] px-2.5 py-1 text-xs text-slate-300">{{ task.day }}</span>
                        <span :class="['rounded-full px-2.5 py-1 text-xs font-semibold', task.priorityClass]">{{ task.priority }}</span>
                        <span v-if="task.completed" class="rounded-full border border-emerald-300/20 bg-emerald-300/10 px-2.5 py-1 text-xs font-semibold text-emerald-100">Mastered</span>
                      </div>
                      <h3 class="mt-3 break-words text-sm font-semibold text-white" :class="task.completed ? 'text-slate-300' : ''">{{ task.title }}</h3>
                    </div>
                    <div class="shrink-0 rounded-2xl border border-cyan-300/15 bg-cyan-300/[0.08] px-3 py-2 text-center">
                      <p class="text-base font-semibold text-cyan-100">+{{ task.energyPoints }}</p>
                      <p class="text-[11px] text-slate-400">energy</p>
                    </div>
                  </div>

                  <p class="kanban-description mt-2 text-sm leading-6 text-slate-400">{{ task.description }}</p>

                  <div class="mt-3 flex flex-wrap gap-2 text-xs text-slate-400">
                    <span class="rounded-full bg-white/[0.06] px-3 py-1">{{ task.duration }} min</span>
                    <span class="rounded-full bg-white/[0.06] px-3 py-1">{{ task.resource }}</span>
                  </div>

                  <div class="mt-4 flex flex-wrap gap-2">
                    <button
                      v-if="column.id === 'recommended'"
                      class="inline-flex min-h-9 items-center justify-center rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-3 text-xs font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-wait disabled:opacity-60"
                      type="button"
                      :disabled="isQuestBusy(task.id)"
                      @click="startLearning(task.id)"
                    >
                      Start Learning
                    </button>
                    <template v-else-if="column.id === 'in_progress'">
                      <button
                        class="inline-flex min-h-9 items-center justify-center rounded-xl border border-emerald-300/20 bg-emerald-300/10 px-3 text-xs font-semibold text-emerald-100 transition hover:bg-emerald-300/15 disabled:cursor-wait disabled:opacity-60"
                        type="button"
                        :disabled="isQuestBusy(task.id)"
                        @click="markTaskAsMastered(task.id)"
                      >
                        {{ updatingItemId === task.id ? 'Updating...' : 'Mark as Mastered' }}
                      </button>
                      <button
                        class="inline-flex min-h-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.05] px-3 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-wait disabled:opacity-60"
                        type="button"
                        :disabled="isQuestBusy(task.id)"
                        @click="moveTaskBack(task.id)"
                      >
                        Move Back
                      </button>
                    </template>
                    <button
                      v-else
                      class="inline-flex min-h-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.05] px-3 text-xs font-semibold text-slate-300 transition hover:bg-white/10 disabled:cursor-wait disabled:opacity-60"
                      type="button"
                      :disabled="isQuestBusy(task.id)"
                      @click="undoTaskMastery(task.id)"
                    >
                      {{ updatingItemId === task.id ? 'Updating...' : 'Undo Mastery' }}
                    </button>

                    <button
                      class="inline-flex min-h-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.05] px-3 text-xs font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-wait disabled:opacity-60"
                      type="button"
                      :disabled="isQuestBusy(task.id)"
                      @click="openEditQuestModal(task)"
                    >
                      {{ editingItemId === task.id ? 'Editing...' : 'Edit' }}
                    </button>
                    <button
                      class="inline-flex min-h-9 items-center justify-center rounded-xl border border-rose-300/20 bg-rose-300/10 px-3 text-xs font-semibold text-rose-100 transition hover:bg-rose-300/15 disabled:cursor-wait disabled:opacity-60"
                      type="button"
                      :disabled="isQuestBusy(task.id)"
                      @click="confirmDeleteQuest(task)"
                    >
                      <span v-if="deletingItemId === task.id" class="mr-2 h-3.5 w-3.5 animate-spin rounded-full border-2 border-rose-100/30 border-t-rose-100" />
                      {{ deletingItemId === task.id ? 'Deleting...' : 'Delete' }}
                    </button>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>

        <section class="rounded-2xl border border-violet-300/18 bg-violet-300/10 p-4">
          <p class="text-sm font-semibold text-white">Adaptive suggestion</p>
          <p class="mt-2 text-sm leading-6 text-slate-300">{{ activePlan.adaptiveSuggestion }}</p>
        </section>
      </div>
    </GlassCard>
    <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0 overflow-hidden">
      <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div class="min-w-0">
          <p class="text-sm font-medium text-cyan-200/80">Quest Roadmap</p>
          <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">Skill tree timeline</h2>
          <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Follow the learning path node by node. Select a node to inspect details, review branches, or update completion.
          </p>
        </div>
        <span class="w-fit rounded-full border border-white/10 px-3 py-1 text-xs font-medium text-slate-400">
          {{ activePlan ? `${completedTasks}/${totalTasks} mastered` : 'Waiting for plan' }}
        </span>
      </div>

      <div v-if="!activePlan" class="mt-6 rounded-3xl border border-dashed border-white/14 bg-white/[0.035] p-6 text-center">
        <p class="font-semibold text-white">No roadmap yet</p>
        <p class="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">Generate or select a study plan to see the interactive skill tree.</p>
      </div>

      <div v-else-if="roadmapNodes.length === 0" class="mt-6 rounded-3xl border border-dashed border-white/14 bg-white/[0.035] p-6 text-center">
        <p class="font-semibold text-white">Roadmap is empty</p>
        <p class="mx-auto mt-2 max-w-xl text-sm leading-6 text-slate-400">Add or regenerate quests to rebuild this skill tree.</p>
      </div>

      <div v-else class="mt-6 grid min-w-0 gap-5 xl:grid-cols-[minmax(0,1fr)_360px]">
        <div class="roadmap-scroll thin-scrollbar min-w-0 overflow-x-auto overflow-y-hidden rounded-3xl border border-white/10 bg-white/[0.025] p-4 sm:p-5">
          <div class="roadmap-track" :style="roadmapTrackStyle">
            <div
              v-for="(node, index) in roadmapNodes"
              :key="node.id"
              class="roadmap-step"
              :class="node.positionClass"
            >
              <span
                v-if="index < roadmapNodes.length - 1"
                class="roadmap-connector"
                :class="node.connectorClass"
                aria-hidden="true"
              />

              <button
                class="roadmap-node-button"
                :class="[node.nodeClass, selectedRoadmapNode?.id === node.id && selectedRoadmapDetailMode === 'quest' ? 'roadmap-node-selected' : '']"
                type="button"
                :aria-label="`Open ${node.label}: ${node.task.title}`"
                @click="selectRoadmapNode(node, 'quest')"
              >
                <svg v-if="node.status === 'completed'" class="h-6 w-6" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                  <path d="M5 12.5l4.2 4.1L19 7" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span v-else class="text-sm font-bold">{{ node.index + 1 }}</span>
              </button>

              <div class="mt-3 min-w-0 text-center">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-cyan-100/80">{{ node.label }}</p>
                <p class="mx-auto mt-1 max-w-32 truncate text-xs font-medium text-slate-300">{{ node.task.title }}</p>
                <span :class="['mt-2 inline-flex rounded-full px-2.5 py-1 text-[11px] font-semibold', node.badgeClass]">{{ node.statusLabel }}</span>
              </div>

              <button
                v-if="node.hasReviewBranch"
                class="roadmap-branch-node"
                :class="selectedRoadmapNode?.id === node.id && selectedRoadmapDetailMode === 'review' ? 'roadmap-branch-selected' : ''"
                type="button"
                :aria-label="`Open review branch for ${node.task.title}`"
                @click="selectRoadmapNode(node, 'review')"
              >
                <span class="roadmap-branch-line" aria-hidden="true" />
                <span class="roadmap-branch-dot" aria-hidden="true" />
                <span class="text-[11px] font-semibold text-amber-100">Review</span>
              </button>
            </div>
          </div>
        </div>

        <aside class="roadmap-detail-panel min-w-0 rounded-3xl border border-white/10 bg-slate-950/35 p-4 sm:p-5">
          <template v-if="selectedRoadmapNode">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-cyan-100/70">{{ selectedRoadmapNode.label }}</p>
                <h3 class="mt-2 break-words text-lg font-semibold text-white">{{ selectedRoadmapNode.task.title }}</h3>
              </div>
              <span :class="['shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold', selectedRoadmapNode.badgeClass]">
                {{ selectedRoadmapNode.statusLabel }}
              </span>
            </div>

            <div v-if="selectedRoadmapDetailMode === 'review'" class="mt-4 rounded-2xl border border-amber-300/20 bg-amber-300/10 p-4">
              <p class="text-sm font-semibold text-amber-100">Review branch</p>
              <p class="mt-2 text-sm leading-6 text-slate-300">Review this concept before moving forward. This branch is suggested because the quest is high priority or likely needs extra reinforcement.</p>
            </div>

            <p class="mt-4 text-sm leading-6 text-slate-300">{{ selectedRoadmapNode.task.description }}</p>

            <div class="mt-4 flex flex-wrap gap-2 text-xs text-slate-300">
              <span class="rounded-full border border-white/10 bg-white/[0.06] px-3 py-1">{{ selectedRoadmapNode.task.duration }} min</span>
              <span :class="['rounded-full px-3 py-1 font-semibold', selectedRoadmapNode.task.priorityClass]">{{ selectedRoadmapNode.task.priority }}</span>
              <span class="rounded-full border border-white/10 bg-white/[0.06] px-3 py-1">{{ selectedRoadmapNode.task.resource }}</span>
            </div>

            <div class="mt-5 flex flex-col gap-2 sm:flex-row">
              <button
                v-if="!selectedRoadmapNode.task.completed"
                class="inline-flex min-h-10 items-center justify-center rounded-xl border border-emerald-300/20 bg-emerald-300/10 px-4 text-sm font-semibold text-emerald-100 transition hover:bg-emerald-300/15 disabled:cursor-wait disabled:opacity-60"
                type="button"
                :disabled="isQuestBusy(selectedRoadmapNode.task.id)"
                @click="completeRoadmapNode(selectedRoadmapNode)"
              >
                {{ updatingItemId === selectedRoadmapNode.task.id ? 'Updating...' : 'Mark Complete' }}
              </button>
              <button
                v-else
                class="inline-flex min-h-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-wait disabled:opacity-60"
                type="button"
                :disabled="isQuestBusy(selectedRoadmapNode.task.id)"
                @click="undoRoadmapNode(selectedRoadmapNode)"
              >
                {{ updatingItemId === selectedRoadmapNode.task.id ? 'Updating...' : 'Undo Complete' }}
              </button>
              <button
                v-if="selectedRoadmapNode.hasReviewBranch"
                class="inline-flex min-h-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] px-4 text-sm font-semibold text-slate-300 transition hover:bg-white/[0.08]"
                type="button"
                @click="selectRoadmapNode(selectedRoadmapNode, selectedRoadmapDetailMode === 'review' ? 'quest' : 'review')"
              >
                {{ selectedRoadmapDetailMode === 'review' ? 'View quest' : 'View review branch' }}
              </button>
            </div>
          </template>
        </aside>
      </div>
    </GlassCard>
  </div>
</template>
<script setup lang="ts">
import lottie from 'lottie-web'
import Swal from 'sweetalert2'
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

import GlassCard from '../components/GlassCard.vue'
import GradientButton from '../components/GradientButton.vue'
import treeGrowthAnimation from '../assets/lottie/tree-growth.json'
import { completeItem, deleteStudyPlan, deleteStudyPlanItem, generateStudyPlan, getActiveStudyPlan, getStudyPlan, getStudyPlans, uncompleteItem, updateStudyPlanItem } from '../services/studyPlanService'

interface PlanTask {
  id: string
  dayNumber: number
  day: string
  title: string
  description: string
  duration: number
  priority: 'High' | 'Medium' | 'Low'
  priorityClass: string
  resource: string
  completed: boolean
  completedAt: string | null
  energyPoints: number
}

type KanbanStatus = 'recommended' | 'in_progress'
type KanbanColumnId = KanbanStatus | 'mastered'

type QuestPriorityPayload = 'low' | 'medium' | 'high'

interface QuestUpdatePayload {
  title: string
  description: string | null
  estimated_minutes: number
  priority: QuestPriorityPayload
  recommended_resource: string | null
}

type RoadmapNodeStatus = 'completed' | 'current' | 'available' | 'future'
type RoadmapDetailMode = 'quest' | 'review'

interface RoadmapNode {
  id: string
  task: PlanTask
  index: number
  label: string
  status: RoadmapNodeStatus
  statusLabel: string
  nodeClass: string
  badgeClass: string
  connectorClass: string
  positionClass: string
  hasReviewBranch: boolean
}

interface GeneratedPlan {
  id: string
  title: string
  description: string
  learningGoal: string
  subject: string
  topic: string
  deadlineDate: string | null
  estimatedDuration: string
  recommendedResources: string[]
  adaptiveSuggestion: string
  status: string
  progressPercentage: number
  tasks: PlanTask[]
  createdAt: string
  updatedAt: string
}

const form = reactive({
  learningGoal: '',
  subject: '',
  topic: '',
  level: 'beginner',
  deadline: '',
  duration: 45,
  learningStyle: 'step_by_step',
  weakTopics: '',
})

const activePlan = ref<GeneratedPlan | null>(null)
const plans = ref<GeneratedPlan[]>([])
const isLoadingPlan = ref(false)
const isGenerating = ref(false)
const updatingItemId = ref('')
const editingItemId = ref('')
const deletingItemId = ref('')
const deletingPlanId = ref('')
const kanbanStatuses = ref<Record<string, KanbanStatus>>({})
const draggingTaskId = ref('')
const dragOverColumn = ref<KanbanColumnId | ''>('')
const selectedRoadmapItemId = ref('')
const selectedRoadmapDetailMode = ref<RoadmapDetailMode>('quest')
const errorMessage = ref('')
const successMessage = ref('')
const energyFeedback = ref<{ taskId: string; points: number } | null>(null)
const celebrationTaskId = ref('')
const confettiPieces = [
  { id: 1, left: '12%', top: '14%', delay: '0ms', color: '#67e8f9' },
  { id: 2, left: '28%', top: '8%', delay: '90ms', color: '#a78bfa' },
  { id: 3, left: '48%', top: '12%', delay: '160ms', color: '#34d399' },
  { id: 4, left: '68%', top: '10%', delay: '40ms', color: '#60a5fa' },
  { id: 5, left: '84%', top: '18%', delay: '130ms', color: '#f0abfc' },
]
let noticeTimer: number | undefined
let feedbackTimer: number | undefined
let celebrationTimer: number | undefined

const TREE_TOTAL_FRAMES = 187
const treeLottieContainer = ref<HTMLElement | null>(null)
const lottieLoadFailed = ref(false)
const lottieReady = ref(false)
let treeAnimation: any = null
let currentTreeFrame = 1
let treePlaybackMode: 'idle' | 'transition' | 'stopped' = 'stopped'
let currentIdleRange: [number, number] = [1, 15]

const canGenerate = computed(() => Boolean(form.learningGoal.trim() && form.subject.trim() && form.topic.trim()))

const priorityClass = (priority: string) => {
  const normalized = String(priority || 'medium').toLowerCase()
  if (normalized === 'high') return 'bg-rose-300/10 text-rose-100'
  if (normalized === 'low') return 'bg-emerald-300/10 text-emerald-100'
  return 'bg-cyan-300/10 text-cyan-100'
}

const priorityLabel = (priority: string): 'High' | 'Medium' | 'Low' => {
  const normalized = String(priority || 'medium').toLowerCase()
  if (normalized === 'high') return 'High'
  if (normalized === 'low') return 'Low'
  return 'Medium'
}

const toNumber = (value: unknown, fallback = 0) => {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

const energyPoints = (minutes: number) => Math.max(1, Math.round((minutes || 15) / 15))

const mapPlan = (plan: any): GeneratedPlan => {
  const tasks = (Array.isArray(plan?.items) ? plan.items : []).map((item: any) => {
    const duration = toNumber(item.estimated_minutes, 15)
    return {
      id: String(item.id),
      dayNumber: toNumber(item.day_number, 1),
      day: `Day ${toNumber(item.day_number, 1)}`,
      title: item.title ?? 'Study quest',
      description: item.description ?? 'Complete this study activity.',
      duration,
      priority: priorityLabel(item.priority),
      priorityClass: priorityClass(item.priority),
      resource: item.recommended_resource ?? 'EduPath AI',
      completed: Boolean(item.is_completed),
      completedAt: item.completed_at ?? null,
      energyPoints: energyPoints(duration),
    }
  })

  const progressFromBackend = plan?.progress_percentage
  const manualProgress = tasks.length ? Math.round((tasks.filter((task: PlanTask) => task.completed).length / tasks.length) * 100) : 0

  return {
    id: String(plan.id),
    title: plan.title ?? 'Study Plan',
    description: plan.description ?? plan.learning_goal ?? 'Personalized learning roadmap.',
    learningGoal: plan.learning_goal ?? '',
    subject: plan.subject ?? 'General Study',
    topic: plan.topic ?? 'Core Topic',
    deadlineDate: plan.deadline_date ?? null,
    estimatedDuration: `${tasks.length || 0} quests / ${plan.study_duration_per_day ?? form.duration} min per day`,
    recommendedResources: Array.from(new Set<string>(tasks.map((task: PlanTask) => task.resource).filter(Boolean))),
    adaptiveSuggestion: plan.generation_message ?? `Focus on ${plan.topic ?? 'your selected topic'} and complete quests in order.`,
    status: plan.status ?? 'active',
    progressPercentage: progressFromBackend === null || progressFromBackend === undefined ? manualProgress : toNumber(progressFromBackend, manualProgress),
    tasks,
    createdAt: plan.created_at ?? new Date().toISOString(),
    updatedAt: plan.updated_at ?? plan.created_at ?? new Date().toISOString(),
  }
}

const showSuccess = (message: string) => {
  successMessage.value = message
  if (noticeTimer) window.clearTimeout(noticeTimer)
  noticeTimer = window.setTimeout(() => {
    successMessage.value = ''
  }, 2200)
}

const triggerQuestCelebration = (task: PlanTask, updatedPlan: GeneratedPlan) => {
  energyFeedback.value = { taskId: task.id, points: task.energyPoints }
  celebrationTaskId.value = task.id

  if (feedbackTimer) window.clearTimeout(feedbackTimer)
  if (celebrationTimer) window.clearTimeout(celebrationTimer)

  feedbackTimer = window.setTimeout(() => {
    energyFeedback.value = null
  }, 1100)

  celebrationTimer = window.setTimeout(() => {
    celebrationTaskId.value = ''
  }, 1100)

  if (updatedPlan.progressPercentage >= 100) {
    showSuccess('Plan completed! Great job!')
  }
}

const fetchActivePlan = async () => {
  const active = await getActiveStudyPlan()
  activePlan.value = active ? mapPlan(active) : null
}

const fetchStudyPlans = async () => {
  const list = await getStudyPlans()
  plans.value = Array.isArray(list) ? list.map(mapPlan) : []
}

const loadPlans = async () => {
  isLoadingPlan.value = true
  errorMessage.value = ''
  try {
    await Promise.all([fetchActivePlan(), fetchStudyPlans()])
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to load study plans.'
  } finally {
    isLoadingPlan.value = false
  }
}

const refreshPlanList = async () => {
  try {
    await fetchStudyPlans()
  } catch {
    plans.value = activePlan.value ? [activePlan.value] : []
  }
}

const generatePlan = async () => {
  if (!canGenerate.value) return
  isGenerating.value = true
  errorMessage.value = ''
  try {
    const plan = await generateStudyPlan({
      learning_goal: form.learningGoal.trim(),
      subject: form.subject.trim(),
      topic: form.topic.trim(),
      deadline_date: form.deadline || null,
      study_duration_per_day: form.duration,
      understanding_level: form.level,
      preferred_learning_style: form.learningStyle,
      weak_topics: form.weakTopics,
    })
    activePlan.value = mapPlan(plan)
    await refreshPlanList()
    showSuccess('Quest plan generated.')
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to generate study plan.'
  } finally {
    isGenerating.value = false
  }
}

const selectPlan = async (planId: string) => {
  isLoadingPlan.value = true
  errorMessage.value = ''
  try {
    const plan = await getStudyPlan(planId)
    activePlan.value = mapPlan(plan)
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to open study plan.'
  } finally {
    isLoadingPlan.value = false
  }
}

const confirmDeletePlan = async (plan: GeneratedPlan) => {
  const result = await Swal.fire({
    title: 'Delete study plan?',
    text: 'This will permanently remove this plan and its tasks.',
    icon: 'warning',
    showCancelButton: true,
    reverseButtons: true,
    confirmButtonText: 'Delete',
    cancelButtonText: 'Cancel',
    background: '#111827',
    color: '#e5e7eb',
    confirmButtonColor: '#e11d48',
    cancelButtonColor: '#334155',
    customClass: {
      popup: 'rounded-3xl border border-white/10 shadow-2xl',
      title: 'text-white',
      htmlContainer: 'text-slate-300',
      confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      cancelButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
    },
  })

  if (!result.isConfirmed) return
  await deleteSelectedPlan(plan)
}

const deleteSelectedPlan = async (plan: GeneratedPlan) => {
  deletingPlanId.value = plan.id
  errorMessage.value = ''
  const deletedCurrentPlan = activePlan.value?.id === plan.id

  try {
    await deleteStudyPlan(plan.id)
    clearKanbanStorage(plan.id)
    plans.value = plans.value.filter((item) => item.id !== plan.id)

    if (deletedCurrentPlan) {
      activePlan.value = null
      kanbanStatuses.value = {}
    }

    try {
      await fetchStudyPlans()
      if (deletedCurrentPlan) await fetchActivePlan()
    } catch {
      if (deletedCurrentPlan) activePlan.value = null
    }

    showSuccess('Study plan deleted.')
  } catch (error: any) {
    await Swal.fire({
      title: 'Failed to delete study plan',
      text: error.apiMessage ?? 'Please try again in a moment.',
      icon: 'error',
      background: '#111827',
      color: '#e5e7eb',
      confirmButtonColor: '#06b6d4',
      customClass: {
        popup: 'rounded-3xl border border-white/10 shadow-2xl',
        title: 'text-white',
        htmlContainer: 'text-slate-300',
        confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      },
    })
  } finally {
    deletingPlanId.value = ''
  }
}

const resetForm = () => {
  form.learningGoal = ''
  form.subject = ''
  form.topic = ''
  form.level = 'beginner'
  form.deadline = ''
  form.duration = 45
  form.learningStyle = 'step_by_step'
  form.weakTopics = ''
}
const getKanbanStorageKey = (planId: string) => `smartplan_kanban_status_${planId}`

const loadKanbanStatuses = (planId: string | null | undefined) => {
  if (!planId || typeof window === 'undefined') {
    kanbanStatuses.value = {}
    return
  }

  try {
    const raw = window.localStorage.getItem(getKanbanStorageKey(planId))
    const parsed = raw ? JSON.parse(raw) : {}

    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
      kanbanStatuses.value = {}
      return
    }

    const activeTasks = activePlan.value?.tasks ?? []
    const validTaskIds = new Set(activeTasks.map((task) => task.id))
    const completedTaskIds = new Set(activeTasks.filter((task) => task.completed).map((task) => task.id))
    const nextStatuses: Record<string, KanbanStatus> = {}

    for (const [taskId, status] of Object.entries(parsed)) {
      if (!validTaskIds.has(taskId) || completedTaskIds.has(taskId)) continue
      if (status === 'recommended' || status === 'in_progress') {
        nextStatuses[taskId] = status
      }
    }

    kanbanStatuses.value = nextStatuses
    window.localStorage.setItem(getKanbanStorageKey(planId), JSON.stringify(nextStatuses))
  } catch (error) {
    console.error('Unable to load Smart Plan Kanban status.', error)
    kanbanStatuses.value = {}
  }
}

const saveKanbanStatuses = () => {
  if (!activePlan.value || typeof window === 'undefined') return

  const nextStatuses: Record<string, KanbanStatus> = {}
  for (const task of activePlan.value.tasks) {
    if (task.completed) continue
    if (kanbanStatuses.value[task.id] === 'in_progress') {
      nextStatuses[task.id] = 'in_progress'
    }
  }

  kanbanStatuses.value = nextStatuses
  window.localStorage.setItem(getKanbanStorageKey(activePlan.value.id), JSON.stringify(nextStatuses))
}

const clearKanbanStorage = (planId: string) => {
  if (typeof window === 'undefined') return
  window.localStorage.removeItem(getKanbanStorageKey(planId))
}

const setKanbanStatus = (taskId: string, status: KanbanStatus) => {
  const nextStatuses = { ...kanbanStatuses.value }

  if (status === 'in_progress') {
    nextStatuses[taskId] = 'in_progress'
  } else {
    delete nextStatuses[taskId]
  }

  kanbanStatuses.value = nextStatuses
  saveKanbanStatuses()
}

const toggleTask = async (taskId: string) => {
  if (!activePlan.value) return
  const task = activePlan.value.tasks.find((item) => item.id === taskId)
  if (!task) return

  const wasCompleted = task.completed
  updatingItemId.value = taskId
  errorMessage.value = ''
  try {
    const updated = wasCompleted ? await uncompleteItem(taskId) : await completeItem(taskId)
    const mappedPlan = mapPlan(updated)
    activePlan.value = mappedPlan

    if (wasCompleted) {
      setKanbanStatus(taskId, 'recommended')
    } else {
      setKanbanStatus(taskId, 'recommended')
      triggerQuestCelebration(task, mappedPlan)
    }

    await refreshPlanList()
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to update this study quest.'
  } finally {
    updatingItemId.value = ''
  }
}

const startLearning = (taskId: string) => {
  setKanbanStatus(taskId, 'in_progress')
}

const moveTaskBack = (taskId: string) => {
  setKanbanStatus(taskId, 'recommended')
}

const markTaskAsMastered = async (taskId: string) => {
  if (!activePlan.value) return
  const task = activePlan.value.tasks.find((item) => item.id === taskId)
  if (!task || task.completed) return

  updatingItemId.value = taskId
  errorMessage.value = ''
  try {
    const updated = await completeItem(taskId)
    const mappedPlan = mapPlan(updated)
    activePlan.value = mappedPlan
    setKanbanStatus(taskId, 'recommended')
    triggerQuestCelebration(task, mappedPlan)
    await refreshPlanList()
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to mark this quest as mastered.'
  } finally {
    updatingItemId.value = ''
  }
}

const undoTaskMastery = async (taskId: string, nextStatus: KanbanStatus = 'recommended') => {
  if (!activePlan.value) return
  const task = activePlan.value.tasks.find((item) => item.id === taskId)
  if (!task || !task.completed) {
    setKanbanStatus(taskId, nextStatus)
    return
  }

  updatingItemId.value = taskId
  errorMessage.value = ''
  try {
    const updated = await uncompleteItem(taskId)
    activePlan.value = mapPlan(updated)
    setKanbanStatus(taskId, nextStatus)
    await refreshPlanList()
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to undo mastery for this quest.'
  } finally {
    updatingItemId.value = ''
  }
}

const handleKanbanDragStart = (task: PlanTask, event: DragEvent) => {
  draggingTaskId.value = task.id
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', task.id)
  }
}

const handleKanbanDragEnd = () => {
  draggingTaskId.value = ''
  dragOverColumn.value = ''
}

const handleKanbanDrop = async (columnId: KanbanColumnId, event: DragEvent) => {
  event.preventDefault()
  const taskId = event.dataTransfer?.getData('text/plain') || draggingTaskId.value
  draggingTaskId.value = ''
  dragOverColumn.value = ''

  if (!taskId || !activePlan.value) return
  const task = activePlan.value.tasks.find((item) => item.id === taskId)
  if (!task) return

  if (columnId === 'mastered') {
    if (!task.completed) await markTaskAsMastered(taskId)
    return
  }

  const nextStatus: KanbanStatus = columnId === 'in_progress' ? 'in_progress' : 'recommended'
  if (task.completed) {
    await undoTaskMastery(taskId, nextStatus)
    return
  }

  setKanbanStatus(taskId, nextStatus)
}

const priorityPayloadValue = (priority: PlanTask['priority']): QuestPriorityPayload => priority.toLowerCase() as QuestPriorityPayload

const escapeHtml = (value: string) =>
  value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;')

const isQuestBusy = (taskId: string) => updatingItemId.value === taskId || editingItemId.value === taskId || deletingItemId.value === taskId

const removeKanbanStatusForItem = (itemId: string) => {
  const nextStatuses = { ...kanbanStatuses.value }
  delete nextStatuses[itemId]
  kanbanStatuses.value = nextStatuses
  saveKanbanStatuses()
}

const openEditQuestModal = async (task: PlanTask) => {
  editingItemId.value = task.id
  const selectedPriority = priorityPayloadValue(task.priority)
  const result = await Swal.fire({
    title: 'Edit quest',
    html: `
      <div style="display:grid;gap:12px;text-align:left">
        <label style="display:grid;gap:6px;color:#cbd5e1;font-size:13px;font-weight:600">
          Title
          <input id="quest-edit-title" class="swal2-input" style="margin:0;width:100%;height:44px;border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.92);color:#fff;padding:0 14px;font-size:14px" value="${escapeHtml(task.title)}" />
        </label>
        <label style="display:grid;gap:6px;color:#cbd5e1;font-size:13px;font-weight:600">
          Description
          <textarea id="quest-edit-description" style="width:100%;min-height:110px;resize:vertical;border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.92);color:#fff;padding:12px 14px;font-size:14px;line-height:1.5">${escapeHtml(task.description)}</textarea>
        </label>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
          <label style="display:grid;gap:6px;color:#cbd5e1;font-size:13px;font-weight:600">
            Estimated minutes
            <input id="quest-edit-minutes" type="number" min="5" max="300" class="swal2-input" style="margin:0;width:100%;height:44px;border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.92);color:#fff;padding:0 14px;font-size:14px" value="${task.duration}" />
          </label>
          <label style="display:grid;gap:6px;color:#cbd5e1;font-size:13px;font-weight:600">
            Priority
            <select id="quest-edit-priority" style="height:44px;border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.92);color:#fff;padding:0 14px;font-size:14px">
              <option value="low" ${selectedPriority === 'low' ? 'selected' : ''}>Low</option>
              <option value="medium" ${selectedPriority === 'medium' ? 'selected' : ''}>Medium</option>
              <option value="high" ${selectedPriority === 'high' ? 'selected' : ''}>High</option>
            </select>
          </label>
        </div>
        <label style="display:grid;gap:6px;color:#cbd5e1;font-size:13px;font-weight:600">
          Recommended resource
          <input id="quest-edit-resource" class="swal2-input" style="margin:0;width:100%;height:44px;border-radius:14px;border:1px solid rgba(255,255,255,.12);background:rgba(15,23,42,.92);color:#fff;padding:0 14px;font-size:14px" value="${escapeHtml(task.resource)}" />
        </label>
      </div>
    `,
    showCancelButton: true,
    reverseButtons: true,
    confirmButtonText: 'Save changes',
    cancelButtonText: 'Cancel',
    background: '#111827',
    color: '#e5e7eb',
    confirmButtonColor: '#06b6d4',
    cancelButtonColor: '#334155',
    focusConfirm: false,
    didOpen: () => {
      const titleInput = document.getElementById('quest-edit-title') as HTMLInputElement | null
      titleInput?.focus()
      titleInput?.select()
    },
    preConfirm: () => {
      const title = (document.getElementById('quest-edit-title') as HTMLInputElement | null)?.value.trim() ?? ''
      const description = (document.getElementById('quest-edit-description') as HTMLTextAreaElement | null)?.value.trim() ?? ''
      const minutesValue = (document.getElementById('quest-edit-minutes') as HTMLInputElement | null)?.value ?? ''
      const priority = (document.getElementById('quest-edit-priority') as HTMLSelectElement | null)?.value as QuestPriorityPayload | undefined
      const resource = (document.getElementById('quest-edit-resource') as HTMLInputElement | null)?.value.trim() ?? ''
      const estimatedMinutes = Number(minutesValue)

      if (!title) {
        Swal.showValidationMessage('Title is required.')
        return false
      }
      if (!Number.isFinite(estimatedMinutes) || estimatedMinutes < 5) {
        Swal.showValidationMessage('Estimated minutes must be at least 5.')
        return false
      }
      if (!priority || !['low', 'medium', 'high'].includes(priority)) {
        Swal.showValidationMessage('Priority must be low, medium, or high.')
        return false
      }

      return {
        title,
        description: description || null,
        estimated_minutes: Math.min(300, Math.round(estimatedMinutes)),
        priority,
        recommended_resource: resource || null,
      } satisfies QuestUpdatePayload
    },
    customClass: {
      popup: 'rounded-3xl border border-white/10 shadow-2xl',
      title: 'text-white',
      htmlContainer: 'text-slate-300',
      confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      cancelButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
    },
  })
  editingItemId.value = ''

  if (result.isConfirmed && result.value) {
    await updateQuest(task, result.value as QuestUpdatePayload)
  }
}

const updateQuest = async (task: PlanTask, payload: QuestUpdatePayload) => {
  editingItemId.value = task.id
  errorMessage.value = ''
  try {
    const updated = await updateStudyPlanItem(task.id, payload)
    activePlan.value = mapPlan(updated)
    saveKanbanStatuses()
    await refreshPlanList()
    showSuccess('Quest updated.')
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to update this quest.'
    await Swal.fire({
      title: 'Failed to update quest',
      text: error.apiMessage ?? 'Please try again in a moment.',
      icon: 'error',
      background: '#111827',
      color: '#e5e7eb',
      confirmButtonColor: '#06b6d4',
      customClass: {
        popup: 'rounded-3xl border border-white/10 shadow-2xl',
        title: 'text-white',
        htmlContainer: 'text-slate-300',
        confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      },
    })
  } finally {
    editingItemId.value = ''
  }
}

const confirmDeleteQuest = async (task: PlanTask) => {
  const result = await Swal.fire({
    title: 'Delete quest?',
    text: 'This quest will be removed from the study plan.',
    icon: 'warning',
    showCancelButton: true,
    reverseButtons: true,
    confirmButtonText: 'Delete',
    cancelButtonText: 'Cancel',
    background: '#111827',
    color: '#e5e7eb',
    confirmButtonColor: '#e11d48',
    cancelButtonColor: '#334155',
    customClass: {
      popup: 'rounded-3xl border border-white/10 shadow-2xl',
      title: 'text-white',
      htmlContainer: 'text-slate-300',
      confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      cancelButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
    },
  })

  if (!result.isConfirmed) return
  await deleteQuest(task)
}

const deleteQuest = async (task: PlanTask) => {
  deletingItemId.value = task.id
  errorMessage.value = ''
  try {
    const updated = await deleteStudyPlanItem(task.id)
    activePlan.value = mapPlan(updated)
    removeKanbanStatusForItem(task.id)
    await refreshPlanList()
    showSuccess('Quest deleted.')
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to delete this quest.'
    await Swal.fire({
      title: 'Failed to delete quest',
      text: error.apiMessage ?? 'Please try again in a moment.',
      icon: 'error',
      background: '#111827',
      color: '#e5e7eb',
      confirmButtonColor: '#06b6d4',
      customClass: {
        popup: 'rounded-3xl border border-white/10 shadow-2xl',
        title: 'text-white',
        htmlContainer: 'text-slate-300',
        confirmButton: 'rounded-xl px-4 py-2 text-sm font-semibold',
      },
    })
  } finally {
    deletingItemId.value = ''
  }
}

const completedTasks = computed(() => activePlan.value?.tasks.filter((task) => task.completed).length ?? 0)
const totalTasks = computed(() => activePlan.value?.tasks.length ?? 0)

const taskKanbanStatus = (task: PlanTask): KanbanColumnId => {
  if (task.completed) return 'mastered'
  return kanbanStatuses.value[task.id] === 'in_progress' ? 'in_progress' : 'recommended'
}

const recommendedTasks = computed(() => activePlan.value?.tasks.filter((task) => taskKanbanStatus(task) === 'recommended') ?? [])
const inProgressTasks = computed(() => activePlan.value?.tasks.filter((task) => taskKanbanStatus(task) === 'in_progress') ?? [])
const masteredTasks = computed(() => activePlan.value?.tasks.filter((task) => taskKanbanStatus(task) === 'mastered') ?? [])

const kanbanColumns = computed<Array<{ id: KanbanColumnId; title: string; description: string; emptyText: string; tasks: PlanTask[] }>>(() => [
  {
    id: 'recommended',
    title: 'Recommended by AI',
    description: 'Suggested quests from the generated roadmap.',
    emptyText: 'No recommended quests left.',
    tasks: recommendedTasks.value,
  },
  {
    id: 'in_progress',
    title: 'In Progress / Learning',
    description: 'Local workspace for quests you are studying now.',
    emptyText: 'Start a quest to move it here.',
    tasks: inProgressTasks.value,
  },
  {
    id: 'mastered',
    title: 'Mastered / Completed',
    description: 'Completed quests synced with the backend.',
    emptyText: 'Mastered quests will appear here.',
    tasks: masteredTasks.value,
  },
])
const progress = computed(() => activePlan.value?.progressPercentage ?? 0)
const energyPercent = computed(() => (totalTasks.value ? Math.round((completedTasks.value / totalTasks.value) * 100) : 0))
const totalMinutes = computed(() => activePlan.value?.tasks.reduce((total, task) => total + task.duration, 0) ?? 0)
const planStatusText = computed(() => (isLoadingPlan.value ? 'Loading active quest plan.' : 'Fill the generator form to create a personalized quest plan.'))
const completedDays = computed(() => completedTasks.value)
const totalDays = computed(() => totalTasks.value)
const treeProgressPercentage = computed(() => (totalDays.value ? Math.round((completedDays.value / totalDays.value) * 100) : 0))

const clampTreeFrame = (frame: number) => Math.min(TREE_TOTAL_FRAMES, Math.max(1, Math.round(frame)))
const treeTargetFrame = computed(() => clampTreeFrame((treeProgressPercentage.value / 100) * TREE_TOTAL_FRAMES))
const treePhaseLabel = computed(() => {
  const value = treeProgressPercentage.value
  if (value <= 15) return 'Seed phase'
  if (value <= 35) return 'New sprout'
  if (value <= 60) return 'Growing strong'
  if (value <= 85) return 'Blooming progress'
  return 'Mastery tree'
})
const completedDateKeys = computed(() => {
  const keys = new Set<string>()
  for (const task of activePlan.value?.tasks ?? []) {
    if (!task.completed || !task.completedAt) continue
    const date = new Date(task.completedAt)
    if (!Number.isNaN(date.getTime())) keys.add(date.toISOString().slice(0, 10))
  }
  return keys
})

const streakCount = computed(() => {
  if (!activePlan.value || completedTasks.value === 0) return 0
  if (completedDateKeys.value.size === 0) return 1

  let streak = 0
  const cursor = new Date()
  for (let index = 0; index < 30; index += 1) {
    const key = cursor.toISOString().slice(0, 10)
    if (!completedDateKeys.value.has(key)) break
    streak += 1
    cursor.setDate(cursor.getDate() - 1)
  }
  return Math.max(streak, completedTasks.value > 0 ? 1 : 0)
})

const plantVisual = computed(() => {
  if (treeProgressPercentage.value > 70) return { stage: 'full', label: 'Full bloom' }
  if (treeProgressPercentage.value >= 30) return { stage: 'growing', label: 'Growing plant' }
  return { stage: 'sprout', label: 'New sprout' }
})

const sortedRoadmapTasks = computed(() => [...(activePlan.value?.tasks ?? [])].sort((a, b) => a.dayNumber - b.dayNumber))

const currentRoadmapIndex = computed(() => {
  const firstOpenIndex = sortedRoadmapTasks.value.findIndex((task) => !task.completed)
  return firstOpenIndex === -1 ? sortedRoadmapTasks.value.length : firstOpenIndex
})

const roadmapStatusLabel = (status: RoadmapNodeStatus) => {
  if (status === 'completed') return 'Mastered'
  if (status === 'current') return 'Current'
  if (status === 'available') return 'Available'
  return 'Locked'
}

const roadmapNodeClass = (status: RoadmapNodeStatus) => {
  if (status === 'completed') return 'roadmap-node-completed'
  if (status === 'current') return 'roadmap-node-current'
  if (status === 'available') return 'roadmap-node-available'
  return 'roadmap-node-future'
}

const roadmapBadgeClass = (status: RoadmapNodeStatus) => {
  if (status === 'completed') return 'bg-emerald-300/10 text-emerald-100'
  if (status === 'current') return 'bg-cyan-300/10 text-cyan-100'
  if (status === 'available') return 'bg-violet-300/10 text-violet-100'
  return 'bg-white/[0.06] text-slate-400'
}

const roadmapNodes = computed<RoadmapNode[]>(() => {
  const tasks = sortedRoadmapTasks.value
  const currentIndex = currentRoadmapIndex.value

  return tasks.map((task, index) => {
    let status: RoadmapNodeStatus = 'future'
    if (task.completed) status = 'completed'
    else if (index === currentIndex) status = 'current'
    else if (index <= currentIndex + 1) status = 'available'

    const nextTask = tasks[index + 1]
    const connectorClass = task.completed && nextTask?.completed ? 'roadmap-connector-completed' : status === 'future' ? 'roadmap-connector-future' : 'roadmap-connector-active'

    return {
      id: task.id,
      task,
      index,
      label: task.day,
      status,
      statusLabel: roadmapStatusLabel(status),
      nodeClass: roadmapNodeClass(status),
      badgeClass: roadmapBadgeClass(status),
      connectorClass,
      positionClass: index % 2 === 0 ? 'roadmap-step-high' : 'roadmap-step-low',
      hasReviewBranch: task.priority === 'High',
    }
  })
})

const roadmapTrackStyle = computed(() => ({ '--roadmap-count': String(Math.max(roadmapNodes.value.length, 1)) }))

const selectedRoadmapNode = computed(() => {
  return (
    roadmapNodes.value.find((node) => node.id === selectedRoadmapItemId.value) ??
    roadmapNodes.value.find((node) => node.status === 'current') ??
    roadmapNodes.value[0] ??
    null
  )
})

const selectRoadmapNode = (node: RoadmapNode, mode: RoadmapDetailMode = 'quest') => {
  selectedRoadmapItemId.value = node.id
  selectedRoadmapDetailMode.value = mode
}

const completeRoadmapNode = async (node: RoadmapNode) => {
  selectedRoadmapItemId.value = node.id
  selectedRoadmapDetailMode.value = 'quest'
  await markTaskAsMastered(node.task.id)
}

const undoRoadmapNode = async (node: RoadmapNode) => {
  selectedRoadmapItemId.value = node.id
  selectedRoadmapDetailMode.value = 'quest'
  await undoTaskMastery(node.task.id)
}

const getTreeIdleRange = (): [number, number] => {
  const value = treeProgressPercentage.value
  if (value <= 15) return [1, 15]
  if (value <= 35) return [30, 45]
  if (value <= 60) return [70, 90]
  if (value <= 85) return [115, 140]
  return [155, TREE_TOTAL_FRAMES]
}

const destroyTreeLottie = () => {
  if (treeAnimation) {
    treeAnimation.destroy()
    treeAnimation = null
  }
  treePlaybackMode = 'stopped'
  lottieReady.value = false
}

const startTreeIdleLoop = () => {
  if (!treeAnimation || !lottieReady.value || lottieLoadFailed.value) return
  currentIdleRange = getTreeIdleRange()
  treePlaybackMode = 'idle'
  treeAnimation.setDirection(1)
  treeAnimation.setSpeed(0.5)
  treeAnimation.playSegments(currentIdleRange, true)
}

const stopTreeIdleLoop = () => {
  if (!treeAnimation) return
  treeAnimation.pause()
  treePlaybackMode = 'stopped'
}

const handleTreeAnimationComplete = () => {
  if (!treeAnimation || lottieLoadFailed.value) return

  if (treePlaybackMode === 'transition') {
    currentTreeFrame = treeTargetFrame.value
    startTreeIdleLoop()
    return
  }

  if (treePlaybackMode === 'idle') {
    treeAnimation.setDirection(1)
    treeAnimation.setSpeed(0.5)
    treeAnimation.playSegments(currentIdleRange, true)
  }
}

const syncTreeFrame = (frame: number, animate = true) => {
  const nextFrame = clampTreeFrame(frame)
  if (!treeAnimation || lottieLoadFailed.value) {
    currentTreeFrame = nextFrame
    return
  }

  stopTreeIdleLoop()

  if (!lottieReady.value || !animate || Math.abs(nextFrame - currentTreeFrame) <= 1) {
    treeAnimation.goToAndStop(nextFrame, true)
    currentTreeFrame = nextFrame
    startTreeIdleLoop()
    return
  }

  if (nextFrame > currentTreeFrame) {
    treePlaybackMode = 'transition'
    treeAnimation.setDirection(1)
    treeAnimation.setSpeed(0.85)
    treeAnimation.playSegments([currentTreeFrame, nextFrame], true)
    return
  }

  treeAnimation.goToAndStop(nextFrame, true)
  currentTreeFrame = nextFrame
  startTreeIdleLoop()
}

const initializeTreeLottie = async () => {
  await nextTick()
  if (!treeLottieContainer.value) return

  destroyTreeLottie()
  lottieLoadFailed.value = false
  currentTreeFrame = treeTargetFrame.value

  try {
    treeAnimation = lottie.loadAnimation({
      container: treeLottieContainer.value,
      renderer: 'svg',
      loop: false,
      autoplay: false,
      animationData: treeGrowthAnimation,
      rendererSettings: {
        preserveAspectRatio: 'xMidYMid meet',
        progressiveLoad: true,
      },
    })

    treeAnimation.addEventListener('DOMLoaded', () => {
      lottieReady.value = true
      syncTreeFrame(treeTargetFrame.value, false)
    })
    treeAnimation.addEventListener('complete', handleTreeAnimationComplete)
    treeAnimation.addEventListener('data_failed', () => {
      lottieLoadFailed.value = true
    })
  } catch (error) {
    console.error('Tree Lottie failed to load.', error)
    lottieLoadFailed.value = true
  }
}
watch(
  () => activePlan.value?.id,
  async (planId) => {
    loadKanbanStatuses(planId)

    if (!planId) {
      destroyTreeLottie()
      return
    }
    await initializeTreeLottie()
  },
  { flush: 'post', immediate: true },
)


watch(
  treeTargetFrame,
  (frame, previousFrame) => {
    syncTreeFrame(frame, previousFrame !== undefined)
  },
  { flush: 'post' },
)

onMounted(loadPlans)

onBeforeUnmount(() => {
  if (noticeTimer) window.clearTimeout(noticeTimer)
  if (feedbackTimer) window.clearTimeout(feedbackTimer)
  if (celebrationTimer) window.clearTimeout(celebrationTimer)
  destroyTreeLottie()
})
</script>

<style scoped>
.kanban-column {
  min-height: 24rem;
}

.kanban-quest-card {
  cursor: grab;
}

.kanban-quest-card:active {
  cursor: grabbing;
}

.kanban-description {
  display: -webkit-box;
  overflow: hidden;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}

.roadmap-scroll {
  min-height: 22rem;
}

.roadmap-track {
  position: relative;
  display: flex;
  min-width: max(100%, calc(var(--roadmap-count) * 9.75rem));
  min-height: 20rem;
  align-items: center;
  gap: 2.5rem;
  padding: 2.5rem 2rem 4.75rem;
}

.roadmap-step {
  position: relative;
  z-index: 2;
  display: flex;
  width: 7rem;
  flex: 0 0 7rem;
  flex-direction: column;
  align-items: center;
}

.roadmap-step-high {
  transform: translateY(-1.25rem);
}

.roadmap-step-low {
  transform: translateY(1.5rem);
}

.roadmap-node-button {
  position: relative;
  z-index: 3;
  display: inline-flex;
  height: 4.75rem;
  width: 4.75rem;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(15, 23, 42, 0.82);
  color: rgb(203, 213, 225);
  transition: border-color 200ms ease, background 200ms ease, box-shadow 200ms ease, transform 200ms ease;
}

.roadmap-node-button:hover,
.roadmap-node-selected {
  transform: translateY(-2px) scale(1.03);
}

.roadmap-node-completed {
  border-color: rgba(34, 211, 238, 0.42);
  background: linear-gradient(135deg, rgba(34, 211, 238, 0.9), rgba(127, 86, 255, 0.86));
  color: white;
  box-shadow: 0 0 28px rgba(34, 211, 238, 0.18);
}

.roadmap-node-current {
  border-color: rgba(103, 232, 249, 0.7);
  background: rgba(8, 47, 73, 0.72);
  color: rgb(207, 250, 254);
  box-shadow: 0 0 0 7px rgba(34, 211, 238, 0.08), 0 0 34px rgba(34, 211, 238, 0.18);
}

.roadmap-node-available {
  border-color: rgba(167, 139, 250, 0.38);
  background: rgba(46, 16, 101, 0.45);
  color: rgb(221, 214, 254);
}

.roadmap-node-future {
  border-color: rgba(148, 163, 184, 0.16);
  background: rgba(15, 23, 42, 0.5);
  color: rgb(100, 116, 139);
}

.roadmap-connector {
  position: absolute;
  left: calc(50% + 2.45rem);
  top: 2.35rem;
  z-index: 1;
  height: 3px;
  width: 6.15rem;
  border-radius: 999px;
  transform: rotate(0deg);
}

.roadmap-step-high .roadmap-connector {
  transform: rotate(16deg);
  transform-origin: left center;
}

.roadmap-step-low .roadmap-connector {
  transform: rotate(-16deg);
  transform-origin: left center;
}

.roadmap-connector-completed {
  background: linear-gradient(90deg, rgba(34, 211, 238, 0.9), rgba(127, 86, 255, 0.9));
  box-shadow: 0 0 18px rgba(34, 211, 238, 0.12);
}

.roadmap-connector-active {
  background: linear-gradient(90deg, rgba(34, 211, 238, 0.46), rgba(127, 86, 255, 0.32));
}

.roadmap-connector-future {
  background-image: linear-gradient(90deg, rgba(148, 163, 184, 0.28) 50%, transparent 50%);
  background-size: 0.8rem 3px;
}

.roadmap-branch-node {
  position: absolute;
  bottom: -3.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  border: 0;
  background: transparent;
  color: rgb(253, 230, 138);
}

.roadmap-branch-line {
  height: 1.1rem;
  width: 1px;
  background: rgba(251, 191, 36, 0.45);
}

.roadmap-branch-dot {
  height: 1.35rem;
  width: 1.35rem;
  border-radius: 999px;
  border: 1px solid rgba(251, 191, 36, 0.38);
  background: rgba(251, 191, 36, 0.14);
  box-shadow: 0 0 18px rgba(251, 191, 36, 0.12);
}

.roadmap-branch-selected .roadmap-branch-dot,
.roadmap-branch-node:hover .roadmap-branch-dot {
  border-color: rgba(251, 191, 36, 0.7);
  background: rgba(251, 191, 36, 0.22);
}

.roadmap-detail-panel {
  align-self: stretch;
}

@media (max-width: 768px) {
  .roadmap-scroll {
    overflow-x: hidden;
    overflow-y: visible;
  }

  .roadmap-track {
    min-width: 0;
    min-height: auto;
    flex-direction: column;
    align-items: flex-start;
    gap: 2rem;
    padding: 1rem 1rem 2rem 3.5rem;
  }

  .roadmap-step {
    width: 100%;
    min-height: 5.25rem;
    flex: 0 0 auto;
    align-items: flex-start;
    padding-left: 0;
    transform: none;
  }

  .roadmap-node-button {
    height: 4rem;
    width: 4rem;
  }

  .roadmap-step > .mt-3 {
    margin-left: 5rem;
    margin-top: -3.85rem;
    text-align: left;
  }

  .roadmap-connector {
    left: 2rem;
    top: 4rem;
    height: 4.3rem;
    width: 3px;
    transform: none !important;
  }

  .roadmap-connector-future {
    background-image: linear-gradient(180deg, rgba(148, 163, 184, 0.28) 50%, transparent 50%);
    background-size: 3px 0.8rem;
  }

  .roadmap-branch-node {
    bottom: -1.85rem;
    left: 5rem;
    flex-direction: row;
  }

  .roadmap-branch-line {
    height: 1px;
    width: 1.1rem;
  }
}

.tree-growth-scene {
  position: relative;
  min-width: 0;
  overflow: visible;
  border-radius: 2rem;
  padding: 0.25rem 0 0;
  background:
    radial-gradient(circle at 50% 46%, rgba(34, 211, 238, 0.12), transparent 38%),
    radial-gradient(circle at 50% 72%, rgba(127, 86, 255, 0.12), transparent 46%);
}

.tree-energy-overlay {
  position: relative;
  z-index: 4;
  margin-inline: auto;
  width: min(100%, 42rem);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(15, 23, 42, 0.42);
  padding: 1rem;
  backdrop-filter: blur(16px);
}

.tree-lottie-stage {
  position: relative;
  z-index: 2;
  display: flex;
  min-height: 360px;
  height: clamp(360px, 34vw, 440px);
  width: 100%;
  align-items: center;
  justify-content: center;
  overflow: visible;
  border: 0;
  background: transparent;
  box-shadow: none;
}

.tree-lottie-scale {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  transform: scale(2.35) translateY(60px);
  transform-origin: center center;
  pointer-events: none;
}

.tree-lottie-canvas {
  width: 100%;
  height: 100%;
}

.tree-lottie-canvas :deep(svg) {
  display: block;
  width: 100% !important;
  height: 100% !important;
  overflow: visible !important;
}

.tree-lottie-fallback {
  display: flex;
  width: 100%;
  height: 100%;
  align-items: flex-end;
  justify-content: center;
  padding-bottom: 0;
}

.tree-lottie-fallback .plant-icon {
  transform: scale(3);
  transform-origin: center bottom;
}


.tree-lottie-empty {
  display: flex;
  height: 5rem;
  width: 5rem;
  align-items: center;
  justify-content: center;
  border-radius: 1.5rem;
  border: 1px solid rgba(103, 232, 249, 0.2);
  background: rgba(103, 232, 249, 0.08);
}

@media (max-width: 768px) {
  .tree-lottie-stage {
    min-height: 300px;
    height: 300px;
    overflow: hidden;
  }

  .tree-lottie-scale {
    transform: scale(1.55);
  }
}
.plant-icon {
  position: relative;
  width: 2.6rem;
  height: 2.6rem;
  filter: drop-shadow(0 0 14px rgba(34, 211, 238, 0.18));
}

.plant-pot {
  position: absolute;
  left: 50%;
  bottom: 0.1rem;
  width: 1.45rem;
  height: 0.65rem;
  border-radius: 0.25rem 0.25rem 0.45rem 0.45rem;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.75), rgba(124, 58, 237, 0.65));
  transform: translateX(-50%);
}

.plant-stem {
  position: absolute;
  left: 50%;
  bottom: 0.65rem;
  width: 0.16rem;
  height: 1.25rem;
  border-radius: 999px;
  background: linear-gradient(180deg, #67e8f9, #34d399);
  transform: translateX(-50%);
}

.plant-leaf,
.plant-canopy {
  position: absolute;
  border-radius: 999px 999px 999px 0;
  background: linear-gradient(135deg, #67e8f9, #34d399);
  box-shadow: 0 0 16px rgba(34, 211, 238, 0.16);
}

.plant-leaf-left {
  left: 0.7rem;
  bottom: 1.45rem;
  width: 0.9rem;
  height: 0.55rem;
  transform: rotate(-34deg);
}

.plant-leaf-right {
  right: 0.7rem;
  bottom: 1.6rem;
  width: 0.9rem;
  height: 0.55rem;
  transform: scaleX(-1) rotate(-34deg);
}

.plant-canopy {
  opacity: 0;
}

.plant-icon.sprout .plant-canopy,
.plant-icon.sprout .plant-leaf-right {
  display: none;
}

.plant-icon.growing .plant-stem,
.plant-icon.full .plant-stem {
  height: 1.55rem;
}

.plant-icon.full .plant-canopy {
  opacity: 1;
}

.plant-canopy-left {
  left: 0.55rem;
  top: 0.35rem;
  width: 1.05rem;
  height: 0.72rem;
  transform: rotate(-24deg);
}

.plant-canopy-right {
  right: 0.55rem;
  top: 0.35rem;
  width: 1.05rem;
  height: 0.72rem;
  transform: scaleX(-1) rotate(-24deg);
}

.quest-energy-pop {
  animation: quest-energy-pop 1.1s ease-out both;
}

.quest-confetti-piece {
  position: absolute;
  display: block;
  width: 0.45rem;
  height: 0.75rem;
  border-radius: 999px;
  opacity: 0;
  transform: translateY(0) rotate(0deg);
  animation: quest-confetti 1s ease-out both;
}

.quest-complete-pulse {
  animation: quest-card-pulse 0.9s ease-out both;
}

@keyframes quest-energy-pop {
  0% {
    opacity: 0;
    transform: translateY(8px) scale(0.94);
  }
  20% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  100% {
    opacity: 0;
    transform: translateY(-18px) scale(0.98);
  }
}

@keyframes quest-confetti {
  0% {
    opacity: 0;
    transform: translateY(0) rotate(0deg) scale(0.8);
  }
  15% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateY(44px) rotate(38deg) scale(1.05);
  }
}

@keyframes quest-card-pulse {
  0% {
    box-shadow: 0 0 0 rgba(34, 211, 238, 0);
  }
  45% {
    box-shadow: 0 0 30px rgba(34, 211, 238, 0.16);
  }
  100% {
    box-shadow: 0 0 0 rgba(34, 211, 238, 0);
  }
}
</style>






















