<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-8 text-white sm:px-6 lg:px-8">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_18%_14%,rgba(0,194,255,0.16),transparent_34%),radial-gradient(circle_at_82%_20%,rgba(127,86,255,0.2),transparent_34%),linear-gradient(135deg,#070b19_0%,#0d1226_56%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.2] [background-image:linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] [background-size:48px_48px]" />
      <div class="absolute -left-28 top-24 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
      <div class="absolute -right-24 bottom-8 h-96 w-96 rounded-full bg-violet-500/20 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-6xl items-center">
      <div class="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.035] shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl lg:grid-cols-[minmax(0,1fr)_minmax(420px,0.92fr)]">
        <section class="relative min-w-0 bg-slate-950/35 p-6 sm:p-8 lg:p-10 xl:p-12">
          <div class="mx-auto flex h-full max-w-xl flex-col justify-center">
            <div class="mb-8">
              <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200/80">Account recovery</p>
              <h1 class="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-5xl">
                Reset your
                <span class="block bg-gradient-to-r from-white via-cyan-100 to-violet-200 bg-clip-text text-transparent">password securely.</span>
              </h1>
              <p class="mt-3 text-sm leading-6 text-slate-400 sm:text-base">
                Enter your email and we'll send you a secure reset link to get back into LenteraAI.
              </p>
            </div>

            <form class="space-y-5" @submit.prevent="handleReset">
              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Email address</span>
                <input
                  id="email"
                  type="email"
                  placeholder="you@example.com"
                  class="recovery-input"
                  autocomplete="email"
                  required
                />
              </label>

              <button
                type="submit"
                class="group relative inline-flex min-h-12 w-full items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:shadow-cyan-500/30 active:translate-y-0"
              >
                <span class="absolute inset-0 bg-white/0 transition group-hover:bg-white/10" />
                <span class="relative">Send Reset Link</span>
              </button>
            </form>

            <div class="mt-6 rounded-2xl border border-white/10 bg-white/[0.035] p-4 text-center text-sm leading-6 text-slate-400">
              Remembered your password?
              <router-link to="/login" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">
                Back to Login
              </router-link>
            </div>
          </div>
        </section>

        <aside class="relative hidden min-h-[640px] overflow-hidden border-l border-white/10 bg-[#0d1226]/70 lg:flex lg:items-center lg:justify-center lg:p-8 xl:p-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_28%,rgba(0,194,255,0.2),transparent_34%),radial-gradient(circle_at_42%_78%,rgba(127,86,255,0.2),transparent_40%)]" />
          <div class="absolute inset-x-8 top-8 h-px bg-gradient-to-r from-transparent via-cyan-300/40 to-transparent" />

          <div class="relative z-10 flex h-full w-full flex-col justify-center gap-8 rounded-[2rem] border border-white/10 bg-white/[0.04] p-6 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl">
            <div class="mx-auto flex min-h-[360px] w-full max-w-md items-center justify-center overflow-hidden rounded-[1.75rem] border border-cyan-300/15 bg-slate-950/35 p-3">
              <div ref="lottieRight" class="h-[22rem] w-[22rem] xl:h-[25rem] xl:w-[25rem]"></div>
            </div>

            <div class="text-center">
              <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200/80">Secure reset</p>
              <h2 class="mt-3 text-2xl font-bold text-white">We'll help you recover access.</h2>
              <p class="mx-auto mt-3 max-w-sm text-sm leading-6 text-slate-300">
                Request a reset link, verify your email, and return to your learning dashboard safely.
              </p>
            </div>
          </div>
        </aside>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import lottie from 'lottie-web'
import forgotAnim from '@/landing_assets/lottie/forgot-password.json'

const lottieRight = ref(null)

onMounted(() => {
  lottie.loadAnimation({
    container: lottieRight.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: forgotAnim
  })
})

const handleReset = () => {
  alert('A reset link has been sent to your email.')
}
</script>

<style scoped>
.recovery-input {
  width: 100%;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.72);
  padding: 0.85rem 1rem;
  color: white;
  outline: none;
  transition: border-color 180ms ease, box-shadow 180ms ease, background 180ms ease;
}

.recovery-input::placeholder {
  color: rgba(148, 163, 184, 0.72);
}

.recovery-input:hover {
  border-color: rgba(255, 255, 255, 0.18);
  background: rgba(15, 23, 42, 0.86);
}

.recovery-input:focus {
  border-color: rgba(34, 211, 238, 0.7);
  background: rgba(15, 23, 42, 0.92);
  box-shadow: 0 0 0 4px rgba(34, 211, 238, 0.12), 0 0 28px rgba(34, 211, 238, 0.08);
}
</style>
