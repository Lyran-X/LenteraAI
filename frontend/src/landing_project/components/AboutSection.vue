<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { aboutDecorations } from '../../landing_assets/media'

const aboutSection = ref(null)
const isInView = ref(false)

let observer = null

const decorationClasses = [
  {
    base: 'top-8 left-4 w-52 md:left-8 md:top-10 md:w-72 lg:w-80',
    from: '-translate-x-16 -translate-y-10 md:-translate-x-28 md:-translate-y-16',
    to: 'translate-x-0 translate-y-0',
    float: 'about-float'
  },
  {
    base: 'top-8 right-4 w-52 md:right-8 md:top-10 md:w-72 lg:w-80',
    from: 'translate-x-16 -translate-y-10 md:translate-x-28 md:-translate-y-16',
    to: 'translate-x-0 translate-y-0',
    float: 'about-float-delayed'
  },
  {
    base: 'bottom-8 left-4 w-44 md:bottom-10 md:left-8 md:w-60 lg:w-72',
    from: '-translate-x-14 translate-y-12 md:-translate-x-24 md:translate-y-20',
    to: 'translate-x-0 translate-y-0',
    float: 'about-float-soft'
  },
  {
    base: 'bottom-8 right-4 w-52 md:bottom-10 md:right-8 md:w-72 lg:w-80',
    from: 'translate-x-14 translate-y-12 md:translate-x-24 md:translate-y-20',
    to: 'translate-x-0 translate-y-0',
    float: 'about-float'
  }
]

onMounted(() => {
  observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isInView.value = true
      }
    },
    {
      threshold: 0.75
    }
  )

  if (aboutSection.value) {
    observer.observe(aboutSection.value)
  }
})

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<template>
  <section
    id="about"
    ref="aboutSection"
    class="landing-section-grid relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-margin-x-mobile py-20 md:px-margin-x"
  >
    <div
      class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_18%_22%,rgba(0,194,255,0.025),transparent_32%),radial-gradient(circle_at_82%_72%,rgba(127,86,255,0.025),transparent_36%)]"
    />
    <div class="pointer-events-none absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-[#070B19]/70 to-transparent" />
    <div class="pointer-events-none absolute inset-x-0 bottom-0 h-44 bg-gradient-to-t from-[#070B19]/80 to-transparent" />

    <!-- Decorations dibuat z-20 agar tampil di depan card -->
    <div
      v-for="(image, index) in aboutDecorations"
      :key="image"
      class="pointer-events-none absolute z-20 will-change-transform"
      :class="[
        decorationClasses[index].base,
        isInView ? 'opacity-40 scale-100' : 'opacity-0 scale-90',
        isInView ? decorationClasses[index].to : decorationClasses[index].from
      ]"
      :style="{
        transition:
          'opacity 1800ms cubic-bezier(0.16, 1, 0.3, 1), transform 1400ms cubic-bezier(0.16, 1, 0.3, 1)',
        transitionDelay: `${index * 120}ms`
      }"
    >
      <img
        :src="image"
        alt=""
        loading="lazy"
        class="h-auto w-full select-none opacity-95 brightness-90 contrast-110"
        :class="decorationClasses[index].float"
      />
    </div>

    <!-- Card utama z-10, jadi decoration berada di depan -->
    <div
      class="relative z-10 mx-auto max-w-4xl rounded-[2rem] border border-cyan-300/10 bg-[#0D1226]/58 px-6 py-10 text-center shadow-[0_32px_120px_rgba(0,0,0,0.34)] backdrop-blur-sm md:px-10"
    >
      <h2
        class="mb-8 font-display-xl text-[40px] font-extrabold tracking-tighter text-white md:text-[72px]"
      >
        <span>ABOUT</span>
        <br />
        <span class="lentera-title-gradient">LenteraAI</span>
      </h2>

      <p class="mb-12 font-body-lg text-body-lg leading-relaxed text-[#94A3B8] md:text-[24px]">
        LenteraAI helps students transform scattered learning materials into structured understanding through AI tutoring, document-based answers, study planning, quizzes, and progress insights.
      </p>

      <a
        class="landing-cta-gradient inline-block rounded-full px-10 py-5 font-label-sm text-label-sm font-bold uppercase tracking-widest transition-transform duration-300 hover:scale-105"
        href="/register"
      >
        Start Learning
      </a>
    </div>
  </section>
</template>

<style scoped>
.lentera-title-gradient {
  display: inline-block;
  background: linear-gradient(90deg, #ffffff 0%, #e5e7eb 58%, #00c2ff 78%, #7f56ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  text-shadow:
    0 0 24px rgba(0, 194, 255, 0.12),
    0 0 34px rgba(127, 86, 255, 0.1);
}

.about-float {
  animation: aboutFloat 6s ease-in-out infinite;
}

.about-float-delayed {
  animation: aboutFloat 7s ease-in-out infinite;
  animation-delay: 1.2s;
}

.about-float-soft {
  animation: aboutFloatSoft 8s ease-in-out infinite;
  animation-delay: 0.6s;
}

@keyframes aboutFloat {
  0% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-16px);
  }

  100% {
    transform: translateY(0);
  }
}

@keyframes aboutFloatSoft {
  0% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(12px);
  }

  100% {
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .about-float,
  .about-float-delayed,
  .about-float-soft {
    animation: none;
  }
}
</style>