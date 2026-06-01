<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-8 text-white sm:px-6 lg:px-8">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_16%_14%,rgba(0,194,255,0.16),transparent_34%),radial-gradient(circle_at_84%_18%,rgba(127,86,255,0.2),transparent_34%),linear-gradient(135deg,#070b19_0%,#0d1226_56%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.2] [background-image:linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] [background-size:48px_48px]" />
      <div class="absolute -left-28 top-20 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
      <div class="absolute -right-24 bottom-8 h-96 w-96 rounded-full bg-violet-500/20 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-6xl items-center">
      <div class="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.035] shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl lg:grid-cols-[minmax(0,1fr)_430px] xl:grid-cols-[minmax(0,1fr)_470px]">
        <section class="relative min-w-0 bg-slate-950/35 p-6 sm:p-8 lg:p-10 xl:p-12">
          <div class="mx-auto flex h-full max-w-xl flex-col justify-center">
            <div class="mb-7">
              <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200/80">Welcome back</p>
              <h1 class="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-5xl">
                Continue your
                <span class="block bg-gradient-to-r from-white via-cyan-100 to-violet-200 bg-clip-text text-transparent">learning flow.</span>
              </h1>
              <p class="mt-3 text-sm leading-6 text-slate-400 sm:text-base">
                Sign in to reopen your AI tutor, study quests, quizzes, and progress insights.
              </p>
            </div>

            <div class="mb-7 flex justify-center">
              <div class="relative flex h-52 w-52 items-center justify-center overflow-hidden rounded-[1.75rem] border border-cyan-300/15 bg-slate-950/35 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl sm:h-60 sm:w-60 lg:h-64 lg:w-64">
                <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_45%,rgba(0,194,255,0.2),transparent_58%),radial-gradient(circle_at_50%_88%,rgba(127,86,255,0.13),transparent_48%)]" />
                <div ref="lottieContainer" class="relative z-10 h-44 w-44 bg-transparent sm:h-52 sm:w-52 lg:h-56 lg:w-56"></div>
              </div>
            </div>

            <div class="space-y-5">
              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Email</span>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="you@example.com"
                  class="auth-input"
                  autocomplete="email"
                />
              </label>

              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Password</span>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Enter your password"
                    class="auth-input pr-12"
                    autocomplete="current-password"
                    @focus="onFocusPassword"
                    @input="handleTyping"
                  />
                  <button
                    class="absolute right-3 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-xl border border-white/10 bg-white/[0.04] transition hover:bg-white/[0.08]"
                    type="button"
                    :aria-label="showPassword ? 'Hide password' : 'Show password'"
                    @click="togglePassword"
                  >
                    <img :src="showPassword ? eyeOpen : eyeClosed" alt="" class="auth-eye-icon h-5 w-5" />
                  </button>
                </div>
              </label>

              <div class="flex w-full flex-col gap-3 text-sm text-slate-300 sm:flex-row sm:items-center sm:justify-between">
                <label class="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.035] px-3 py-2">
                  <input v-model="remember" type="checkbox" class="auth-checkbox" />
                  <span>Remember for 30 days</span>
                </label>
                <router-link to="/forgot-password" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">Forgot password?</router-link>
              </div>

              <button
                @click="handleLogin"
                :disabled="loading"
                class="group relative inline-flex min-h-12 w-full items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:shadow-cyan-500/30 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
              >
                <span class="absolute inset-0 bg-white/0 transition group-hover:bg-white/10" />
                <span class="relative">{{ loading ? 'Signing in...' : 'Sign in' }}</span>
              </button>
            </div>

            <p class="mt-6 text-center text-sm text-slate-400">
              Don't have an account?
              <router-link to="/register" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">Sign up for free</router-link>
            </p>
          </div>
        </section>

        <aside class="relative hidden min-h-[660px] overflow-hidden border-l border-white/10 bg-[#0d1226]/70 lg:block">
          <img :src="womenImage" alt="Student learning online" class="h-full w-full object-cover" />
          <div class="absolute inset-0 bg-gradient-to-br from-[#060c24]/80 via-[#060c24]/35 to-violet-950/55" />
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_35%_20%,rgba(0,194,255,0.18),transparent_34%),radial-gradient(circle_at_80%_78%,rgba(127,86,255,0.24),transparent_42%)]" />
          <div class="absolute inset-x-6 top-6 h-px bg-gradient-to-r from-transparent via-cyan-300/40 to-transparent" />

          <div class="absolute bottom-8 left-8 right-8 rounded-3xl border border-white/10 bg-slate-950/35 p-6 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl">
            <p class="text-3xl font-bold tracking-[0.2em] text-cyan-200/80">LenteraAI Workspace</p>
            <blockquote class="mt-4 text-2xl font-semibold leading-snug text-white">
              Learn smarter, stay focused, and let your roadmap grow with every session.
            </blockquote>
            <p class="mt-4 text-sm leading-6 text-slate-300">
              AI tutoring, document learning, quizzes, and progress insights in one cinematic dashboard.
            </p>
          </div>
        </aside>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import lottie from 'lottie-web'
import Swal from 'sweetalert2'
import { useAuthStore } from '@/stores/authStore'
import eyeOpen from '@/landing_assets/picture/eye-open.svg'
import eyeClosed from '@/landing_assets/picture/eye-close.svg'
import animationData from '@/landing_assets/lottie/eye-animation.json'
import womenImage from '@/asset_landing/women.jpg'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const lottieContainer = ref(null)
const animation = ref(null)
const showPassword = ref(false)
const remember = ref(false)
const loading = ref(false)

const form = ref({ email: '', password: '' })

const getRedirectTarget = () => {
  const redirect = route.query.redirect
  return typeof redirect === 'string' && redirect.startsWith('/') ? redirect : '/dashboard'
}

const getErrorMessage = (error) => error?.apiMessage ?? error?.message ?? 'Please check your credentials and try again.'

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    Swal.fire({ icon: 'warning', title: 'Incomplete Data', text: 'Please enter both email and password.' })
    return
  }

  loading.value = true

  try {
    await authStore.login({
      email: form.value.email.trim(),
      password: form.value.password,
    })

    await Swal.fire({ icon: 'success', title: 'Login Successful', text: 'Redirecting to Dashboard...', timer: 900, showConfirmButton: false })
    router.push(getRedirectTarget())
  } catch (error) {
    Swal.fire({ icon: 'error', title: 'Login Failed', text: getErrorMessage(error) })
  } finally {
    loading.value = false
  }
}

let typingLoop = null
let peekingLoop = null
let typingTimeout = null
let hasPlayedIntro = false

onMounted(() => {
  animation.value = lottie.loadAnimation({ container: lottieContainer.value, renderer: 'svg', loop: false, autoplay: false, animationData })
})

onUnmounted(() => {
  stopTypingLoop()
  stopPeekingLoop()
  if (typingTimeout) clearTimeout(typingTimeout)
  animation.value?.destroy()
})

const onFocusPassword = () => {
  if (!hasPlayedIntro && !showPassword.value) {
    animation.value?.playSegments([31, 50], true)
    hasPlayedIntro = true
  }
}

const startTypingLoop = () => {
  if (typingLoop || showPassword.value) return
  animation.value?.playSegments([51, 72], true)
  typingLoop = setInterval(() => animation.value?.playSegments([51, 72], true), 1300)
}

const stopTypingLoop = () => {
  if (typingLoop) clearInterval(typingLoop)
  typingLoop = null
  animation.value?.pause()
}

const handleTyping = () => {
  if (!showPassword.value) startTypingLoop()
  resetTypingTimeout()
}

const resetTypingTimeout = () => {
  if (typingTimeout) clearTimeout(typingTimeout)
  typingTimeout = setTimeout(() => stopTypingLoop(), 6000)
}

const togglePassword = () => {
  showPassword.value = !showPassword.value
  if (showPassword.value) {
    stopTypingLoop()
    clearTimeout(typingTimeout)
    startPeekingLoop()
  } else {
    stopPeekingLoop()
    if (form.value.password) {
      startTypingLoop()
      resetTypingTimeout()
    }
  }
}

const startPeekingLoop = () => {
  if (peekingLoop || !animation.value) return
  animation.value.playSegments([73, 89], true)
  animation.value.addEventListener('complete', handlePeekLoopOnce)

  function handlePeekLoopOnce() {
    animation.value.removeEventListener('complete', handlePeekLoopOnce)
    peekingLoop = setInterval(() => animation.value?.playSegments([0, 30], true), 2000)
  }
}

const stopPeekingLoop = () => {
  if (peekingLoop) clearInterval(peekingLoop)
  peekingLoop = null
  animation.value?.pause()
}
</script>

<style scoped>
.auth-input {
  width: 100%;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.72);
  padding: 0.85rem 1rem;
  color: white;
  outline: none;
  transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
}

.auth-input::placeholder {
  color: rgba(148, 163, 184, 0.72);
}

.auth-input:hover {
  border-color: rgba(255, 255, 255, 0.18);
  background: rgba(15, 23, 42, 0.86);
}

.auth-input:focus {
  border-color: rgba(34, 211, 238, 0.7);
  background: rgba(15, 23, 42, 0.92);
  box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.12), 0 0 28px rgba(34, 211, 238, 0.08);
}

.auth-eye-icon {
  opacity: 0.82;
  filter: invert(1) brightness(1.65) saturate(0.3);
}

.auth-checkbox {
  height: 1rem;
  width: 1rem;
  border-radius: 0.35rem;
  border: 1px solid rgba(255, 255, 255, 0.18);
  background: rgba(15, 23, 42, 0.9);
  accent-color: #22d3ee;
}
</style>
