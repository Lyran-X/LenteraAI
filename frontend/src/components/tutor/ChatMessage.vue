<template>
  <article :class="['flex min-w-0 gap-3', message.role === 'user' ? 'justify-end' : 'justify-start']">
    <div v-if="message.role === 'assistant'" class="mt-1 hidden h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-cyan-300/20 bg-cyan-300/10 text-xs font-bold text-cyan-100 sm:flex">
      AI
    </div>

    <div
      :class="[
        'min-w-0 break-words',
        message.role === 'user' ? 'order-1 max-w-[85%] sm:max-w-[75%]' : 'max-w-[90%] sm:max-w-[82%]',
      ]"
    >
      <div
        :class="[
          'min-w-0 rounded-3xl px-4 py-3 text-sm leading-6 shadow-lg transition duration-200',
          message.role === 'user'
            ? 'rounded-br-lg bg-gradient-to-r from-cyan-500 via-blue-500 to-violet-500 text-white shadow-blue-500/18'
            : 'rounded-bl-lg border border-white/10 bg-white/[0.065] text-slate-200 shadow-black/18',
        ]"
      >
        <div v-if="message.modeLabel && message.role === 'assistant'" class="mb-2 inline-flex rounded-full border border-cyan-300/16 bg-cyan-300/10 px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-cyan-100">
          {{ message.modeLabel }}
        </div>

        <div
          v-if="message.role === 'assistant'"
          class="ai-markdown"
          v-html="renderedMarkdown"
        />
        <p v-else class="whitespace-pre-wrap break-words">{{ message.content }}</p>
      </div>

      <div
        :class="[
          'mt-2 flex flex-wrap items-center gap-2 text-xs text-slate-500 sm:gap-3',
          message.role === 'user' ? 'justify-end' : 'justify-start',
        ]"
      >
        <span>{{ message.createdAt }}</span>
        <button
          v-if="message.role === 'assistant'"
          class="rounded-full border border-white/10 px-3 py-1 font-medium text-slate-300 transition hover:border-cyan-300/30 hover:bg-cyan-300/10 hover:text-cyan-100 disabled:cursor-default disabled:border-emerald-300/20 disabled:bg-emerald-300/10 disabled:text-emerald-200"
          type="button"
          :disabled="saved"
          @click="$emit('save', message.id)"
        >
          {{ saved ? 'Saved' : 'Save answer' }}
        </button>
      </div>
    </div>

    <div v-if="message.role === 'user'" class="mt-1 hidden h-9 w-9 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-300 to-violet-400 text-xs font-bold text-white sm:flex">
      You
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

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

const props = defineProps<{
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    createdAt: string
    modeLabel?: string
  }
  saved?: boolean
}>()

defineEmits<{
  save: [messageId: string]
}>()

const renderMarkdown = (content: string) => md.render(content || '')
const renderedMarkdown = computed(() => renderMarkdown(props.message.content))
</script>
