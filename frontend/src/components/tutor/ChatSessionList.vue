<template>
  <GlassCard padding="p-3.5 sm:p-4" extra-class="flex h-full min-w-0 flex-col">
    <div class="flex flex-none items-center justify-between gap-3">
      <div>
        <p class="text-sm font-medium text-cyan-200/80">Chat history</p>
        <h2 class="mt-1 text-lg font-semibold text-white">Sessions</h2>
      </div>
      <span class="rounded-full border border-white/10 px-2.5 py-1 text-xs font-medium text-slate-400">
        {{ sessions.length }}
      </span>
    </div>

    <div v-if="sessions.length" class="thin-scrollbar mt-4 min-h-0 flex-1 space-y-2 overflow-y-auto pr-1">
      <button
        v-for="session in sessions"
        :key="session.id"
        class="group w-full min-w-0 rounded-2xl border p-3.5 text-left transition duration-200"
        :class="
          session.id === activeSessionId
            ? 'border-cyan-300/35 bg-cyan-300/10 shadow-lg shadow-cyan-500/10'
            : 'border-white/8 bg-white/[0.04] hover:border-white/16 hover:bg-white/[0.07]'
        "
        type="button"
        @click="$emit('select', session.id)"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="truncate text-sm font-semibold text-white">{{ session.title }}</p>
            <p class="mt-1 truncate text-xs text-slate-500">{{ session.topic }}</p>
          </div>
          <span class="shrink-0 rounded-full bg-white/[0.06] px-2 py-1 text-[11px] font-medium text-slate-400">
            {{ session.updatedAt }}
          </span>
        </div>
        <p class="mt-3 line-clamp-2 text-sm leading-5 text-slate-400">{{ session.preview }}</p>
        <div class="mt-4 flex items-center justify-between text-xs text-slate-500">
          <span>{{ session.messagesCount }} messages</span>
          <span class="text-cyan-200/80 transition group-hover:text-cyan-100">Open</span>
        </div>
      </button>
    </div>

    <div v-else class="mt-4 flex min-h-0 flex-1 items-center justify-center rounded-2xl border border-white/8 bg-white/[0.035] p-4 text-center">
      <p class="text-sm leading-6 text-slate-400">Your chat sessions will appear here after you start a conversation.</p>
    </div>
  </GlassCard>
</template>

<script setup lang="ts">
import GlassCard from '../GlassCard.vue'

defineProps<{
  sessions: Array<{
    id: string
    title: string
    topic: string
    preview: string
    updatedAt: string
    messagesCount: number
  }>
  activeSessionId: string
}>()

defineEmits<{
  select: [sessionId: string]
}>()
</script>
