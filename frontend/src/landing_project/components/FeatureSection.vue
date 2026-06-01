<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { videos } from '../../landing_assets/media'

gsap.registerPlugin(ScrollTrigger)

const sectionRef = ref(null)
const videoWrapRef = ref(null)
const videoRef = ref(null)
const contentRef = ref(null)
const labelRef = ref(null)
const textRef = ref(null)
const buttonRef = ref(null)

let ctx

onMounted(() => {
  ctx = gsap.context(() => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: sectionRef.value,
        start: 'top top',
        end: '+=1800',
        scrub: 1.4,
        pin: true
      }
    })

    tl.fromTo(
      videoRef.value,
      {
        scale: 0.92,
        yPercent: -4
      },
      {
        scale: 1.12,
        yPercent: 4,
        ease: 'none'
      },
      0
    )

    tl.fromTo(
      videoWrapRef.value,
      {
        yPercent: 5
      },
      {
        yPercent: -5,
        ease: 'none'
      },
      0
    )

    tl.fromTo(
      contentRef.value,
      {
        opacity: 0,
        y: 48,
        scale: 0.96
      },
      {
        opacity: 1,
        y: 0,
        scale: 1,
        ease: 'power3.out'
      },
      0.18
    )

    tl.fromTo(
      [labelRef.value, textRef.value, buttonRef.value],
      {
        opacity: 0,
        y: 28
      },
      {
        opacity: 1,
        y: 0,
        stagger: 0.08,
        ease: 'power3.out'
      },
      0.28
    )
  }, sectionRef.value)
})

onBeforeUnmount(() => {
  ctx?.revert()
})
</script>

<template>
  <section
    ref="sectionRef"
    class="relative h-screen bg-black"
  >
    <div class="sticky top-0 h-screen overflow-hidden">
      <div
        ref="videoWrapRef"
        class="absolute inset-0 will-change-transform"
      >
        <video
          ref="videoRef"
          autoplay
          loop
          muted
          playsinline
          preload="metadata"
          class="absolute inset-0 h-full w-full object-cover will-change-transform brightness-[0.78] contrast-[1.04] saturate-[0.92]"
        >
          <source :src="videos.featured" type="video/mp4" />
        </video>
      </div>

      <div
        class="pointer-events-none absolute inset-0"
        style="
          background:
            linear-gradient(90deg, rgba(0, 0, 0, 0.58) 0%, rgba(0, 0, 0, 0.18) 46%, rgba(0, 0, 0, 0.62) 100%),
            linear-gradient(180deg, rgba(0, 0, 0, 0.22) 0%, rgba(0, 0, 0, 0.08) 42%, rgba(0, 0, 0, 0.38) 100%);
        "
      />

      <div class="pointer-events-none absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-black/55 to-transparent" />
      <div class="pointer-events-none absolute inset-x-0 bottom-0 h-44 bg-gradient-to-t from-black/65 to-transparent" />

      <div class="pointer-events-none absolute -left-40 top-1/3 h-72 w-72 rounded-full bg-cyan-400/[0.018] blur-3xl" />
      <div class="pointer-events-none absolute -right-40 bottom-20 h-80 w-80 rounded-full bg-violet-500/[0.018] blur-3xl" />

      <div class="relative z-10 mx-auto flex h-full max-w-container-max items-end px-margin-x-mobile pb-16 md:px-margin-x md:pb-24">
        <div
          ref="contentRef"
          class="flex w-full flex-col items-start justify-between gap-8 md:flex-row md:items-end"
        >
          <div class="max-w-xl rounded-2xl border border-white/10 bg-black/38 p-6 text-left shadow-[0_30px_120px_rgba(0,0,0,0.52)] backdrop-blur-md md:p-8">
            <span
              ref="labelRef"
              class="mb-4 block font-label-sm text-label-sm uppercase tracking-[0.28em] text-[#00C2FF]"
            >
              Our Approach
            </span>

            <p
              ref="textRef"
              class="font-body-md text-body-md leading-relaxed text-[#CBD5E1] md:text-[22px]"
            >
              LenteraAI turns every question into a guided learning path: explain, verify with sources, practice with quizzes, and track progress with clarity.
            </p>
          </div>

          <a
            ref="buttonRef"
            class="landing-cta-gradient whitespace-nowrap rounded-full px-8 py-4 font-label-sm text-label-sm font-bold uppercase tracking-widest transition-all duration-500 hover:scale-105"
            href="#philosophy"
          >
            Explore More
          </a>
        </div>
      </div>
    </div>
  </section>
</template>