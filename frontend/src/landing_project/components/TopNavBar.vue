<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import lenteraLogo from '@/assets/brand/lenteraai-logo.png'

const router = useRouter()
const isMenuOpen = ref(false)

const navLinks = [
  { label: 'Work', href: '#work' },
  { label: 'About', href: '#about' },
  { label: 'Philosophy', href: '#philosophy' },
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const goToRegister = () => {
  closeMenu()
  router.push('/register')
}
</script>

<template>
  <nav class="fixed top-0 z-50 w-full border-b border-[rgba(0,194,255,0.12)] bg-[#060C24]/90 shadow-[0_1px_0_rgba(255,255,255,0.04),0_12px_40px_rgba(0,194,255,0.04)] backdrop-blur-[20px]">
    <div class="flex h-20 w-full items-center justify-between px-margin-x-mobile md:h-24 md:px-margin-x">
      <a
        class="flex min-w-0 items-center bg-transparent p-0"
        href="#"
        aria-label="LenteraAI home"
        @click="closeMenu"
      >
        <img
          :src="lenteraLogo"
          alt="LenteraAI"
          class="h-14 w-auto max-w-[12rem] select-none object-contain md:h-16 md:max-w-[16rem] lg:h-20 lg:max-w-[18rem]"
          draggable="false"
        />
      </a>

      <div class="hidden items-center gap-2 rounded-full border border-[rgba(0,194,255,0.16)] bg-[#151B35]/72 px-3 py-2 shadow-[0_16px_50px_rgba(0,0,0,0.18)] md:flex">
        <a
          v-for="link in navLinks"
          :key="link.href"
          class="rounded-full px-5 py-2.5 font-label-sm text-label-sm uppercase tracking-widest text-[#94A3B8] transition-all duration-300 hover:bg-gradient-to-r hover:from-cyan-400/10 hover:to-violet-500/10 hover:text-white"
          :href="link.href"
        >
          {{ link.label }}
        </a>
      </div>

      <div class="hidden items-center gap-6 md:flex">
        <router-link
          to="/login"
          class="font-label-sm text-label-sm uppercase tracking-widest text-[#94A3B8] transition-colors hover:text-[#00C2FF]"
        >
          Log in
        </router-link>

        <button
          type="button"
          class="landing-cta-gradient flex items-center justify-center rounded-full px-8 py-4 font-label-sm text-label-sm uppercase tracking-widest transition-all duration-300"
          @click="router.push('/register')"
        >
          Get Started
        </button>
      </div>

      <button
        type="button"
        class="flex h-11 w-11 items-center justify-center rounded-full border border-[rgba(0,194,255,0.16)] bg-[#151B35]/80 text-white md:hidden"
        :aria-label="isMenuOpen ? 'Close menu' : 'Open menu'"
        @click="toggleMenu"
      >
        <span class="material-symbols-outlined text-3xl">
          {{ isMenuOpen ? 'close' : 'menu' }}
        </span>
      </button>
    </div>

    <Transition
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="-translate-y-4 opacity-0"
      enter-to-class="translate-y-0 opacity-100"
      leave-active-class="transition-all duration-200 ease-in"
      leave-from-class="translate-y-0 opacity-100"
      leave-to-class="-translate-y-4 opacity-0"
    >
      <div
        v-if="isMenuOpen"
        class="absolute left-0 top-20 w-full border-b border-[rgba(0,194,255,0.12)] bg-[#060C24]/95 px-margin-x-mobile pb-6 backdrop-blur-[20px] md:hidden"
      >
        <div class="flex flex-col gap-3 rounded-3xl border border-[rgba(0,194,255,0.14)] bg-[#151B35]/80 p-4 shadow-2xl">
          <a
            v-for="link in navLinks"
            :key="link.href"
            :href="link.href"
            class="rounded-2xl px-5 py-4 font-label-sm text-label-sm uppercase tracking-widest text-[#94A3B8] transition-all hover:bg-cyan-300/10 hover:text-white"
            @click="closeMenu"
          >
            {{ link.label }}
          </a>

          <div class="my-2 h-px bg-cyan-300/10"></div>

          <router-link
            to="/login"
            class="rounded-2xl px-5 py-4 font-label-sm text-label-sm uppercase tracking-widest text-[#94A3B8] transition-all hover:bg-cyan-300/10 hover:text-white"
            @click="closeMenu"
          >
            Log in
          </router-link>

          <button
            type="button"
            class="landing-cta-gradient mt-2 flex items-center justify-center rounded-full px-6 py-4 font-label-sm text-label-sm uppercase tracking-widest transition-all duration-300"
            @click="goToRegister"
          >
            Get Started
          </button>
        </div>
      </div>
    </Transition>
  </nav>
</template>