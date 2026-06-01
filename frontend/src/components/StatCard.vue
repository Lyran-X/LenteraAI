<template>
  <GlassCard padding="p-4" extra-class="min-h-28">
    <div class="flex h-full flex-col justify-between gap-4">
      <div class="flex items-start justify-between gap-3">
        <div class="min-w-0">
          <p class="text-sm font-medium text-slate-400">{{ label }}</p>
          <p :class="['mt-2 break-words text-2xl font-semibold tracking-normal text-white sm:text-3xl', valueClass]">{{ value }}</p>
        </div>
        <div :class="['flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl border shadow-lg', accentClasses]">
          <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path :d="iconPath" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
        </div>
      </div>

      <div class="flex items-center justify-between gap-3 text-sm">
        <span :class="trendPositive ? 'text-emerald-300' : 'text-amber-300'">{{ trend }}</span>
        <span class="text-right text-slate-500">{{ caption }}</span>
      </div>
    </div>
  </GlassCard>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import GlassCard from './GlassCard.vue'

const props = withDefaults(
  defineProps<{
    label: string
    value: string
    trend: string
    caption: string
    accent?: 'cyan' | 'blue' | 'violet' | 'emerald' | 'amber'
    icon?: 'chart' | 'plans' | 'notes' | 'tutor'
    valueClass?: string
    trendPositive?: boolean
  }>(),
  {
    accent: 'cyan',
    icon: 'chart',
    valueClass: '',
    trendPositive: true,
  },
)

const accentClasses = computed(() => {
  const classes = {
    cyan: 'border-cyan-300/25 bg-cyan-400/16 text-cyan-100 shadow-cyan-500/10',
    blue: 'border-blue-300/25 bg-blue-400/16 text-blue-100 shadow-blue-500/10',
    violet: 'border-violet-300/25 bg-violet-400/16 text-violet-100 shadow-violet-500/10',
    emerald: 'border-emerald-300/25 bg-emerald-400/16 text-emerald-100 shadow-emerald-500/10',
    amber: 'border-amber-300/25 bg-amber-400/16 text-amber-100 shadow-amber-500/10',
  }

  return classes[props.accent]
})

const iconPath = computed(() => {
  const paths = {
    chart: 'M4 19V5m0 14h16M8 16v-4m4 4V8m4 8v-6',
    plans: 'M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01',
    notes: 'M6 4h9l3 3v13H6V4Zm8 0v4h4M9 12h6M9 16h6',
    tutor: 'M12 4a7 7 0 0 0-7 7v2a4 4 0 0 0 4 4h1l2 3 2-3h1a4 4 0 0 0 4-4v-2a7 7 0 0 0-7-7Z',
  }

  return paths[props.icon]
})
</script>