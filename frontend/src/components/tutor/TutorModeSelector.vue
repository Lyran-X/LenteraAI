<template>
  <div class="space-y-2.5">
    <button
      v-for="mode in modes"
      :key="mode.id"
      class="w-full rounded-2xl border p-3.5 text-left transition duration-200"
      :class="
        mode.id === selectedMode
          ? 'border-cyan-300/35 bg-cyan-300/10 shadow-lg shadow-cyan-500/10'
          : 'border-white/8 bg-white/[0.04] hover:border-white/16 hover:bg-white/[0.07]'
      "
      type="button"
      @click="$emit('select', mode.id)"
    >
      <div class="flex items-start gap-3">
        <span :class="['mt-1 h-2.5 w-2.5 shrink-0 rounded-full', mode.dotClass]" />
        <div class="min-w-0">
          <p class="text-sm font-semibold text-white">{{ mode.label }}</p>
          <p class="mt-1 text-xs leading-5 text-slate-400">{{ mode.description }}</p>
        </div>
      </div>
    </button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  selectedMode: string
  modes: Array<{
    id: string
    label: string
    description: string
    dotClass: string
  }>
}>()

defineEmits<{
  select: [modeId: string]
}>()
</script>
