<template>
  <button
    class="group w-full rounded-2xl border border-white/8 bg-white/[0.04] p-3.5 text-left transition duration-200 hover:border-cyan-300/30 hover:bg-cyan-300/8"
    type="button"
    @click="$emit('use', prompt)"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="min-w-0">
        <p class="text-sm font-semibold text-white">{{ prompt.title }}</p>
        <p class="mt-2 text-sm leading-5 text-slate-400">{{ prompt.text }}</p>
      </div>
      <svg class="mt-0.5 h-4 w-4 shrink-0 text-slate-500 transition group-hover:text-cyan-200" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M5 12h14M13 5l7 7-7 7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
      </svg>
    </div>
    <span class="mt-3 inline-flex rounded-full bg-white/[0.06] px-2.5 py-1 text-xs font-medium text-cyan-100/80">
      {{ prompt.modeLabel }}
    </span>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  prompt: {
    title: string
    text: string
    modeId: string
    modeLabel: string
  }
}>()

defineEmits<{
  use: [
    prompt: {
      title: string
      text: string
      modeId: string
      modeLabel: string
    },
  ]
}>()
</script>
