<script setup>
import { videos } from '../../landing_assets/media'
</script>

<template>
  <section class="landing-section-grid relative flex h-screen flex-col items-center justify-center overflow-hidden px-margin-x-mobile md:px-margin-x">
    <video autoplay class="absolute inset-0 z-0 h-full w-full object-cover object-bottom" loop muted playsinline>
      <source :src="videos.hero" type="video/mp4" />
    </video>

    <div
      class="absolute inset-0 z-0"
      style="background: linear-gradient(180deg, rgba(7, 11, 25, 0.50) 0%, rgba(7, 11, 25, 0.38) 45%, rgba(7, 11, 25, 0.72) 100%), linear-gradient(90deg, rgba(0, 0, 0, 0.28) 0%, rgba(0, 0, 0, 0.08) 50%, rgba(0, 0, 0, 0.35) 100%);"
    />
    <div class="pointer-events-none absolute -right-36 top-28 z-0 h-80 w-80 rounded-full bg-cyan-400/[0.04] blur-3xl" />
    <div class="pointer-events-none absolute -left-40 bottom-20 z-0 h-96 w-96 rounded-full bg-violet-500/[0.035] blur-3xl" />

    <div class="relative z-10 mx-auto mt-20 flex w-full max-w-5xl flex-col items-center text-center">
      <h1 class="landing-hero-title mb-6 font-display-xl-mobile text-display-xl-mobile font-bold md:font-display-xl md:text-display-xl">
        LenteraAI
      </h1>
      <p class="mb-12 max-w-3xl font-body-lg text-body-lg text-[#94A3B8] md:text-[22px]">
        A cinematic AI learning companion for smarter study plans, document Q&amp;A, adaptive quizzes, and personalized progress insights.
      </p>

      <form class="glass-panel mb-10 flex w-full max-w-md items-center rounded-full border border-cyan-300/18 bg-[#151B35]/75 p-2 pl-6 shadow-[0_18px_70px_rgba(0,194,255,0.08)] focus-within:border-cyan-300/40 focus-within:ring-2 focus-within:ring-cyan-300/20" @submit.prevent>
        <input class="min-w-0 flex-grow border-none bg-transparent font-body-md text-body-md text-white placeholder:text-[#94A3B8] focus:outline-none focus:ring-0" placeholder="Enter your email" type="email" />
        <button class="landing-cta-gradient flex h-12 w-12 shrink-0 items-center justify-center rounded-full transition-all" type="submit" aria-label="Submit email">
          <span class="material-symbols-outlined">arrow_forward</span>
        </button>
      </form>

      <div class="flex flex-col justify-center gap-4 sm:flex-row">
        <a class="landing-cta-gradient inline-flex items-center justify-center rounded-full px-8 py-4 font-label-sm text-label-sm uppercase tracking-widest transition-all duration-300" href="/register">
          Start Learning
        </a>
        <a class="landing-muted-button inline-flex items-center justify-center rounded-full border px-8 py-4 font-label-sm text-label-sm uppercase tracking-widest transition-all duration-300 hover:border-cyan-300/35 hover:text-cyan-100" href="#work">
          Explore Features
        </a>
      </div>
    </div>

    <div class="absolute bottom-10 left-0 z-10 flex w-full justify-center gap-4">
      <a v-for="icon in ['photo_camera', 'flutter_dash', 'public']" :key="icon" class="glass-panel flex h-12 w-12 items-center justify-center rounded-full border border-cyan-300/18 text-white transition-colors hover:bg-cyan-300/10" href="#">
        <span class="material-symbols-outlined text-xl">{{ icon }}</span>
      </a>
    </div>
  </section>
</template>