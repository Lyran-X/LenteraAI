<template>
  <button
    :type="type"
    :class="[
      'inline-flex min-h-11 items-center justify-center gap-2 rounded-xl px-4 text-sm font-semibold text-white transition duration-200',
      'focus:outline-none focus:ring-2 focus:ring-cyan-300/70 focus:ring-offset-2 focus:ring-offset-slate-950',
      variantClasses,
      fullWidth ? 'w-full' : '',
    ]"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    type?: 'button' | 'submit' | 'reset'
    variant?: 'primary' | 'secondary'
    fullWidth?: boolean
  }>(),
  {
    type: 'button',
    variant: 'primary',
    fullWidth: false,
  },
)

const variantClasses = computed(() => {
  if (props.variant === 'secondary') {
    return 'border border-white/12 bg-white/8 text-slate-100 hover:bg-white/12'
  }

  return 'bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 shadow-lg shadow-cyan-500/20 hover:brightness-110'
})
</script>
