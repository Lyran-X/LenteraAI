<template>
  <form class="min-w-0 border-t border-white/8 bg-slate-950/45 p-3 backdrop-blur-2xl sm:p-4" @submit.prevent="submit">
    <div class="flex min-w-0 flex-col gap-2.5 rounded-3xl border border-white/10 bg-white/[0.055] p-2 transition focus-within:border-cyan-300/40 sm:flex-row sm:items-end">
      <textarea
        class="thin-scrollbar max-h-32 min-h-12 min-w-0 flex-1 resize-none bg-transparent px-3 py-3 text-sm leading-6 text-white placeholder:text-slate-500 focus:outline-none"
        :disabled="disabled"
        :placeholder="placeholder"
        :value="modelValue"
        rows="1"
        @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
        @keydown.enter.exact.prevent="submit"
      />

      <button
        class="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-2xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-4 text-sm font-semibold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-50 sm:min-w-24"
        type="submit"
        :disabled="disabled || !modelValue.trim()"
      >
        <span>{{ disabled ? 'Thinking' : 'Send' }}</span>
        <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="m5 12 14-7-4 14-3-6-7-1Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </button>
    </div>
    <p class="mt-2 text-xs text-slate-500">Mode: {{ selectedModeLabel }} / Press Enter to send, Shift+Enter for a new line.</p>
  </form>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: string
    disabled?: boolean
    selectedModeLabel: string
    placeholder?: string
  }>(),
  {
    disabled: false,
    placeholder: 'Ask EduPath AI about your lesson',
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
  submit: []
}>()

const submit = () => {
  if (props.disabled || !props.modelValue.trim()) {
    return
  }

  emit('submit')
}
</script>
