<template>
  <div class="rounded-2xl border border-dashed border-white/14 bg-white/[0.04] p-5 text-center sm:p-6">
    <div class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10">
      <svg class="h-6 w-6 text-cyan-200" viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path
          d="M12 5v14M5 12h14"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
        />
      </svg>
    </div>
    <h3 class="mt-4 text-lg font-semibold text-white">{{ title }}</h3>
    <p class="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-400">{{ description }}</p>
    <div v-if="$slots.default" class="mt-5">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
