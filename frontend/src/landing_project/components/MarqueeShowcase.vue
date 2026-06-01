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
    class="relative overflow-hidden bg-[#070B19] py-24 md:py-32"
  >
    <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_8%_18%,rgba(0,194,255,0.08),transparent_30%),radial-gradient(circle_at_92%_76%,rgba(127,86,255,0.08),transparent_32%)]" />
    <div class="pointer-events-none absolute inset-0 bg-gradient-to-b from-[#070B19] via-[#0D1226]/48 to-[#070B19]" />
    <div class="pointer-events-none absolute inset-0 opacity-30 [background-image:linear-gradient(rgba(17,22,45,0.48)_1px,transparent_1px),linear-gradient(90deg,rgba(17,22,45,0.48)_1px,transparent_1px)] [background-size:36px_36px]" />
    <div class="pointer-events-none absolute left-0 top-0 z-20 h-full w-24 bg-gradient-to-r from-[#070B19] to-transparent md:w-48" />
    <div class="pointer-events-none absolute right-0 top-0 z-20 h-full w-24 bg-gradient-to-l from-[#070B19] to-transparent md:w-48" />

    <div class="relative z-10 mx-auto mb-14 max-w-container-max px-margin-x-mobile text-center md:px-margin-x">
      <span class="mb-4 block font-label-sm text-label-sm uppercase tracking-[0.28em] text-[#00C2FF]">
        Cinematic Archive
      </span>

      <h2 class="landing-archive-heading mx-auto max-w-4xl font-headline-lg-mobile text-headline-lg-mobile md:font-headline-lg md:text-headline-lg">
        A cinematic learning archive powered by intelligent systems.
      </h2>
    </div>

    <div class="relative z-10 space-y-8 md:space-y-10">
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
  gap: 1.5rem;
  will-change: transform;
}

.marquee-track-right {
  animation: marqueeRight 95s linear infinite;
}

.marquee-track-left {
  animation: marqueeLeft 110s linear infinite;
}

.marquee-card {
  position: relative;
  flex: 0 0 auto;
  width: clamp(260px, 28vw, 460px);
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border-radius: 1.75rem;
  background: #151b35;
  border: 1px solid rgba(0, 194, 255, 0.12);
  box-shadow:
    0 28px 90px rgba(0, 0, 0, 0.48),
    0 0 58px rgba(0, 194, 255, 0.05),
    0 0 64px rgba(127, 86, 255, 0.045),
    inset 0 1px 0 rgba(255, 255, 255, 0.07);
  transform: translateZ(0);
  animation:
    cardFloat 8s ease-in-out infinite,
    cardBreath 12s ease-in-out infinite;
  animation-delay: var(--float-delay), var(--breath-delay);
  transition: border-color 280ms ease, box-shadow 280ms ease;
  will-change: transform;
}

.marquee-card:hover {
  border-color: rgba(127, 86, 255, 0.35);
  box-shadow:
    0 30px 100px rgba(0, 0, 0, 0.5),
    0 0 72px rgba(0, 194, 255, 0.08),
    0 0 82px rgba(127, 86, 255, 0.08),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

.marquee-card-alt {
  width: clamp(240px, 25vw, 420px);
  aspect-ratio: 4 / 3;
}

.marquee-card::before {
  content: '';
  position: absolute;
  inset: 0;
  z-index: 2;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(7, 11, 25, 0.08), rgba(0, 0, 0, 0.26));
}

.marquee-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  z-index: 3;
  pointer-events: none;
  border-radius: inherit;
  box-shadow:
    inset 0 0 0 1px rgba(255, 255, 255, 0.06),
    inset 0 -40px 80px rgba(7, 11, 25, 0.34);
}

.marquee-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: scale(1.04);
  filter: contrast(1.06) brightness(0.86);
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
    translate: 0 -30px;
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
    scale: 1.025;
  }

  100% {
    scale: 1;
  }
}

@media (max-width: 768px) {
  .marquee-track {
    gap: 1rem;
  }

  .marquee-track-right {
    animation-duration: 80s;
  }

  .marquee-track-left {
    animation-duration: 92s;
  }

  .marquee-card {
    width: 74vw;
    border-radius: 1.25rem;
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