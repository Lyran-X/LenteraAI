<script setup>
import { videos } from '../landing_assets/media'

const cards = [
  {
    label: 'Strategy',
    title: 'Research & Insight',
    description: 'We dig deep into data, culture, and human behavior to surface the insights that drive meaningful, lasting change.',
    video: videos.strategy
  },
  {
    label: 'Craft',
    title: 'Design & Execution',
    description: 'From concept to launch, we obsess over every detail to deliver experiences that feel effortless and look extraordinary.',
    video: videos.craft
  }
]
</script>

<template>
  <section class="py-20 md:py-32 px-margin-x-mobile md:px-margin-x bg-[#0C0C0C]">
    <div class="max-w-container-max mx-auto">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div v-for="card in cards" :key="card.title" class="relative aspect-[4/5] md:aspect-[3/4] rounded-xl overflow-hidden glass-panel group">
          <video autoplay class="absolute inset-0 w-full h-full object-cover opacity-60 transition-transform duration-700 group-hover:scale-105" loop muted playsinline>
            <source :src="card.video" type="video/mp4" />
          </video>
          <div class="absolute inset-0 bg-gradient-to-t from-black via-black/20 to-transparent" />
          <div class="absolute inset-0 p-8 flex flex-col justify-end">
            <span class="font-label-sm text-label-sm text-primary uppercase tracking-widest mb-4 block">{{ card.label }}</span>
            <h3 class="font-headline-md text-headline-md text-white mb-4">{{ card.title }}</h3>
            <p class="font-body-md text-body-md text-on-surface-variant max-w-sm">{{ card.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
