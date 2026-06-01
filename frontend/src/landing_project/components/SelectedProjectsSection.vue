<script setup>
import { videos } from '../../landing_assets/media.js'
</script>

<template>
  <section
    class="relative flex min-h-[420px] w-full items-center justify-center overflow-hidden bg-black py-16 md:min-h-[500px] md:py-20"
  >
    <video
      autoplay
      class="absolute inset-0 z-0 h-full w-full object-cover brightness-[0.82] contrast-[1.03] saturate-[0.88]"
      loop
      muted
      playsinline
      preload="metadata"
    >
      <source :src="videos.selectedProjects" type="video/mp4" />
    </video>

    <!-- Natural dark overlay: dominan hitam, bukan navy/cyan, supaya video tidak kebiruan -->
    <div
      class="pointer-events-none absolute inset-0 z-10"
      style="
        background:
          linear-gradient(180deg, rgba(0, 0, 0, 0.58) 0%, rgba(0, 0, 0, 0.20) 45%, rgba(0, 0, 0, 0.66) 100%),
          linear-gradient(90deg, rgba(0, 0, 0, 0.30) 0%, rgba(0, 0, 0, 0.06) 50%, rgba(0, 0, 0, 0.30) 100%);
      "
    />

    <!-- Edge fade agar transisi section tetap halus tanpa blue tint -->
    <div class="pointer-events-none absolute inset-x-0 top-0 z-10 h-32 bg-gradient-to-b from-black/55 to-transparent" />
    <div class="pointer-events-none absolute inset-x-0 bottom-0 z-10 h-40 bg-gradient-to-t from-black/65 to-transparent" />

    <!-- Brand glow dibuat sangat kecil dan hanya di pinggir, bukan menutupi video -->
    <div class="pointer-events-none absolute -right-32 top-8 z-10 h-72 w-72 rounded-full bg-cyan-400/[0.015] blur-3xl" />
    <div class="pointer-events-none absolute -left-32 bottom-8 z-10 h-72 w-72 rounded-full bg-violet-500/[0.015] blur-3xl" />

    <div class="relative z-20 container mx-auto flex flex-col items-center px-margin-x-mobile text-center md:px-margin-x">
      <h2
        class="landing-cta-title mb-5 max-w-3xl font-headline-lg-mobile text-[clamp(2rem,5vw,3rem)] font-bold leading-tight md:text-[clamp(2.6rem,4vw,4rem)]"
      >
        Ready to learn with clarity?
      </h2>

      <p class="mb-10 max-w-2xl font-body-lg text-[18px] leading-relaxed text-[#CBD5E1] md:text-[22px]">
        Turn your documents, questions, and study goals into a personalized AI-powered learning journey.
      </p>

      <div class="flex w-full flex-col justify-center gap-4 sm:w-auto sm:flex-row">
        <a
          class="landing-cta-gradient rounded-full px-8 py-4 text-center font-label-sm font-bold uppercase tracking-widest transition-all hover:scale-105"
          href="/register"
        >
          Start Learning
        </a>

        <a
          id="contact"
          class="rounded-full border border-white/15 bg-black/30 px-8 py-4 text-center font-label-sm uppercase tracking-widest text-white shadow-[0_18px_60px_rgba(0,0,0,0.28)] backdrop-blur-md transition-all hover:scale-105 hover:border-cyan-300/30 hover:bg-black/45 hover:text-cyan-100"
          href="#work"
        >
          Explore Features
        </a>
      </div>
    </div>
  </section>
</template>