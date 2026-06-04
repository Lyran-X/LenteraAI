<script setup>
import { computed } from 'vue'
import { marqueeImages } from '../../landing_assets/media.js'

const midpoint = Math.ceil(marqueeImages.length / 2)
const firstRow = computed(() => marqueeImages.slice(0, midpoint))
const secondRow = computed(() => marqueeImages.slice(midpoint))
</script>

<template>
  <section
    id="work"
    class="relative overflow-hidden bg-[#070B19] py-14 md:py-18 lg:py-20"
  >
    <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_8%_18%,rgba(0,194,255,0.06),transparent_30%),radial-gradient(circle_at_92%_76%,rgba(127,86,255,0.07),transparent_32%)]" />
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-b from-[#070B19] via-[#0D1226]/42 to-[#070B19]" />
    <div class="pointer-events-none absolute inset-0 opacity-24 [background-image:linear-gradient(rgba(17,22,45,0.42)_1px,transparent_1px),linear-gradient(90deg,rgba(17,22,45,0.42)_1px,transparent_1px)] [background-size:34px_34px]" />
    <div class="pointer-events-none absolute left-0 top-0 z-20 h-full w-20 bg-gradient-to-r from-[#070B19] to-transparent md:w-36" />
    <div class="pointer-events-none absolute right-0 top-0 z-20 h-full w-20 bg-gradient-to-l from-[#070B19] to-transparent md:w-36" />

    <div class="relative z-10 mx-auto mb-8 max-w-5xl px-margin-x-mobile text-center md:mb-10 md:px-margin-x">
      <span class="mb-3 block text-[11px] font-semibold uppercase tracking-[0.22em] text-[#00C2FF]">
        Cinematic Archive
      </span>

      <h2 class="landing-archive-heading mx-auto max-w-3xl text-[28px] font-bold leading-tight tracking-tight md:text-[40px] lg:text-[46px]">
        A cinematic learning archive powered by intelligent systems.
      </h2>
    </div>

    <div class="relative z-10 space-y-5 md:space-y-6">
      <div class="marquee-viewport">
        <div class="marquee-track marquee-track-right">
          <div
            v-for="(image, index) in [...firstRow, ...firstRow]"
            :key="`row-1-${index}`"
            class="marquee-card"
            :style="{ '--float-delay': `${index * 0.45}s`, '--breath-delay': `${index * 0.32}s` }"
          >
            <img :src="image" alt="Showcase project" loading="lazy" />
          </div>
        </div>
      </div>

      <div class="marquee-viewport">
        <div class="marquee-track marquee-track-left">
          <div
            v-for="(image, index) in [...secondRow, ...secondRow]"
            :key="`row-2-${index}`"
            class="marquee-card marquee-card-alt"
            :style="{ '--float-delay': `${index * 0.5}s`, '--breath-delay': `${index * 0.36}s` }"
          >
            <img :src="image" alt="Showcase project" loading="lazy" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.marquee-viewport {
  position: relative;
  display: flex;
  width: 100%;
  overflow: hidden;
}

.marquee-track {
  display: flex;
  width: max-content;
  gap: 1rem;
  will-change: transform;
}

.marquee-track-right {
  animation: marqueeRight 105s linear infinite;
}

.marquee-track-left {
  animation: marqueeLeft 120s linear infinite;
}

.marquee-card {
  position: relative;
  flex: 0 0 auto;
  width: clamp(210px, 22vw, 340px);
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border-radius: 1.25rem;
  background: #151b35;
  border: 1px solid rgba(0, 194, 255, 0.11);
  box-shadow:
    0 18px 58px rgba(0, 0, 0, 0.4),
    0 0 42px rgba(0, 194, 255, 0.04),
    0 0 48px rgba(127, 86, 255, 0.04),
    inset 0 1px 0 rgba(255, 255, 255, 0.06);
  transform: translateZ(0);
  animation:
    cardFloat 9s ease-in-out infinite,
    cardBreath 13s ease-in-out infinite;
  animation-delay: var(--float-delay), var(--breath-delay);
  transition:
    border-color 280ms ease,
    box-shadow 280ms ease;
  will-change: transform;
}

.marquee-card:hover {
  border-color: rgba(127, 86, 255, 0.3);
  box-shadow:
    0 20px 64px rgba(0, 0, 0, 0.42),
    0 0 52px rgba(0, 194, 255, 0.06),
    0 0 58px rgba(127, 86, 255, 0.06),
    inset 0 1px 0 rgba(255, 255, 255, 0.07);
}

.marquee-card-alt {
  width: clamp(200px, 20vw, 310px);
  aspect-ratio: 4 / 3;
}

.marquee-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(7, 11, 25, 0.06), rgba(0, 0, 0, 0.22));
}

.marquee-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  z-index: 3;
  pointer-events: none;
  border-radius: inherit;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.055),
    inset 0 -28px 58px rgba(7, 11, 25, 0.3);
}

.marquee-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.03);
  filter: contrast(1.04) brightness(0.88);
}

@keyframes marqueeRight {
  from {
    transform: translate3d(-50%, 0, 0);
  }

  to {
    transform: translate3d(0%, 0, 0);
  }
}

@keyframes marqueeLeft {
  from {
    transform: translate3d(0%, 0, 0);
  }

  to {
    transform: translate3d(-50%, 0, 0);
  }
}

@keyframes cardFloat {
  0% {
    translate: 0 0;
  }

  50% {
    translate: 0 -14px;
  }

  100% {
    translate: 0 0;
  }
}

@keyframes cardBreath {
  0% {
    scale: 1;
  }

  50% {
    scale: 1.014;
  }

  100% {
    scale: 1;
  }
}

@media (max-width: 768px) {
  .marquee-track {
    gap: 0.85rem;
  }

  .marquee-track-right {
    animation-duration: 90s;
  }

  .marquee-track-left {
    animation-duration: 104s;
  }

  .marquee-card {
    width: 68vw;
    border-radius: 1rem;
  }

  .marquee-card-alt {
    width: 62vw;
  }
}

@media (prefers-reduced-motion: reduce) {
  .marquee-track-right,
  .marquee-track-left,
  .marquee-card {
    animation: none;
  }
}
</style>