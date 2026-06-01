<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { videos } from '../../landing_assets/media'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref(null)
const eyebrowRef = ref(null)
const headingMaskRef = ref(null)
const headingRef = ref(null)
const videoWrapRef = ref(null)
const videoRef = ref(null)
const contentRefs = ref([])

let ctx

const contents = [
  {
    label: 'Guided Understanding',
    body: 'AI Tutor helps students unpack difficult ideas through concise explanations, step-by-step guidance, and Socratic prompts that stop when the concept is clear.'
  },
  {
    label: 'Evidence-Based Practice',
    body: 'Document Q&A, personal study plans, adaptive quizzes, and analytics connect each learning action back to sources, goals, weak topics, and measurable progress.'
  }
]

const setContentRef = (el) => {
  if (el) contentRefs.value.push(el)
}

onMounted(() => {
  ctx = gsap.context(() => {
    gsap.set(eyebrowRef.value, {
      opacity: 0,
      y: 18,
      filter: 'blur(10px)'
    })

    gsap.set(headingMaskRef.value, {
      clipPath: 'inset(0 100% 0 0)'
    })

    gsap.set(headingRef.value, {
      y: 32,
      opacity: 0
    })

    gsap.set(videoWrapRef.value, {
      opacity: 0,
      y: 80,
      scale: 0.96,
      filter: 'blur(14px)'
    })

    gsap.set(videoRef.value, {
      scale: 2,
      transformOrigin: 'center center',
      force3D: true
    })

    gsap.set(contentRefs.value, {
      opacity: 0,
      y: 44,
      filter: 'blur(14px)'
    })

    const introTl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionRef.value,
        start: 'top 10%',
        end: 'top 28%',
        scrub: 2
      }
    })

    introTl
      .to(
        eyebrowRef.value,
        {
          opacity: 1,
          y: 0,
          filter: 'blur(0px)',
          ease: 'power3.out'
        },
        0
      )
      .to(
        headingMaskRef.value,
        {
          clipPath: 'inset(0 0% 0 0)',
          ease: 'power4.out'
        },
        0.12
      )
      .to(
        headingRef.value,
        {
          opacity: 1,
          y: 0,
          ease: 'power4.out'
        },
        0.12
      )
      .to(
        videoWrapRef.value,
        {
          opacity: 1,
          y: 0,
          scale: 1,
          filter: 'blur(0px)',
          ease: 'power4.out'
        },
        0.22
      )
      .to(
        contentRefs.value,
        {
          opacity: 1,
          y: 0,
          filter: 'blur(0px)',
          stagger: 0.18,
          ease: 'power4.out'
        },
        0.36
      )

    const scrollTl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionRef.value,
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1.5
      }
    })

    scrollTl
      .to(
        videoRef.value,
        {
          scale: 0.7,
          yPercent: 4,
          ease: 'none'
        },
        0
      )
      .to(
        videoWrapRef.value,
        {
          yPercent: -2,
          ease: 'none'
        },
        0
      )
      .to(
        contentRefs.value,
        {
          yPercent: -4,
          ease: 'none',
          stagger: 0.04
        },
        0
      )
  }, sectionRef.value)
})

onBeforeUnmount(() => {
  ctx?.revert()
  contentRefs.value = []
})
</script>

<template>
  <section
    id="philosophy"
    ref="sectionRef"
    class="landing-section-grid relative mx-auto max-w-container-max overflow-hidden px-margin-x-mobile py-16 md:px-margin-x md:py-24"
  >
    <div class="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_18%_26%,rgba(0,194,255,0.07),transparent_30%),radial-gradient(circle_at_82%_72%,rgba(127,86,255,0.08),transparent_34%)]" />

    <div class="mb-10 md:mb-14">
      <span
        ref="eyebrowRef"
        class="mb-4 block font-label-sm text-label-sm uppercase tracking-widest text-[#00C2FF] will-change-transform"
      >
        The Lentera Method
      </span>

      <div
        ref="headingMaskRef"
        class="overflow-hidden will-change-transform"
      >
        <h2
          ref="headingRef"
          class="font-headline-lg-mobile text-headline-lg-mobile md:font-headline-lg md:text-headline-lg will-change-transform"
        >
          <span class="landing-method-heading">Personalized Learning</span>
          <span class="landing-method-x mx-2 italic">x</span>
          <span class="landing-method-heading">Intelligent Guidance</span>
        </h2>
      </div>
    </div>

    <div class="grid grid-cols-1 items-center gap-10 md:grid-cols-2 md:gap-12">
      <div
        ref="videoWrapRef"
        class="relative will-change-transform"
      >
        <div
          class="relative aspect-[4/3] overflow-hidden rounded-[2rem] bg-[#151B35] shadow-[0_40px_140px_rgba(0,0,0,0.5)] will-change-transform md:aspect-[0.95/1]"
        >
          <video
            ref="videoRef"
            autoplay
            class="backface-hidden absolute inset-0 h-full w-full transform-gpu object-cover will-change-transform"
            loop
            muted
            playsinline
            preload="metadata"
          >
            <source :src="videos.philosophy" type="video/mp4" />
          </video>

          <div class="absolute inset-0 bg-gradient-to-t from-[#070B19]/68 via-black/10 to-black/24" />
          <div class="absolute inset-0 bg-gradient-to-r from-black/28 via-transparent to-black/16" />
          <div class="absolute inset-0 rounded-[2rem] ring-1 ring-cyan-300/12" />
        </div>
      </div>

      <div class="flex flex-col gap-8 md:gap-10">
        <template v-for="(item, index) in contents" :key="item.label">
          <div
            v-if="index !== 0"
            :ref="setContentRef"
            class="h-px w-full bg-gradient-to-r from-transparent via-cyan-300/18 to-violet-400/16"
          />

          <div
            :ref="setContentRef"
            class="space-y-4 rounded-3xl border border-cyan-300/12 bg-[#151B35]/72 p-6 shadow-[0_24px_90px_rgba(0,0,0,0.22)] backdrop-blur-md will-change-transform"
          >
            <span class="block font-label-sm text-label-sm uppercase tracking-widest text-[#00C2FF]">
              {{ item.label }}
            </span>

            <p class="font-body-lg text-body-lg leading-relaxed text-[#94A3B8]">
              {{ item.body }}
            </p>
          </div>
        </template>
      </div>
    </div>
  </section>
</template>