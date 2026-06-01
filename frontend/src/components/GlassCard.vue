<template>
  <section :class="['glass-card w-full min-w-0 overflow-hidden rounded-2xl break-words', padding, extraClass]">
    <slot />
  </section>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    padding?: string
    extraClass?: string
  }>(),
  {
    padding: 'p-5',
    extraClass: '',
  },
)
</script>
