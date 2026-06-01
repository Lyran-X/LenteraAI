<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-8 text-white sm:px-6 lg:px-8">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_18%_14%,rgba(0,194,255,0.16),transparent_34%),radial-gradient(circle_at_84%_16%,rgba(127,86,255,0.18),transparent_34%),linear-gradient(135deg,#070b19_0%,#0d1226_56%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.2] [background-image:linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] [background-size:48px_48px]" />
      <div class="absolute -left-28 top-24 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
      <div class="absolute -right-24 bottom-8 h-96 w-96 rounded-full bg-violet-500/20 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-6xl items-center">
      <div class="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.035] shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl lg:grid-cols-[minmax(0,0.92fr)_minmax(0,1.08fr)]">
        <aside class="relative min-h-[360px] overflow-hidden border-b border-white/10 bg-[#0d1226]/70 p-6 sm:p-8 lg:min-h-[680px] lg:border-b-0 lg:border-r lg:p-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_34%,rgba(0,194,255,0.18),transparent_34%),radial-gradient(circle_at_48%_74%,rgba(127,86,255,0.16),transparent_40%)]" />
          <div class="absolute inset-x-8 top-8 h-px bg-gradient-to-r from-transparent via-cyan-300/40 to-transparent" />

          <div class="relative z-10 flex h-full items-center justify-center rounded-[2rem] border border-white/10 bg-white/[0.035] p-6 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl sm:p-8">
            <img :src="termsImage" alt="Terms of Use illustration" class="w-full max-w-md object-contain drop-shadow-2xl" />
          </div>
        </aside>

        <article class="relative min-w-0 bg-slate-950/35 p-6 sm:p-8 lg:p-10 xl:p-12">
          <div class="mx-auto flex h-full max-w-2xl flex-col justify-center">
            <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200/80">LenteraAI policy</p>
            <h1 class="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl lg:text-5xl">
              Terms of
              <span class="bg-gradient-to-r from-white via-cyan-100 to-violet-200 bg-clip-text text-transparent">Use</span>
            </h1>
            <p class="mt-4 text-sm leading-6 text-slate-400 sm:text-base">
              By using LenteraAI, you agree to the following terms and responsibilities.
            </p>

            <div class="mt-8 space-y-4">
              <section v-for="term in terms" :key="term.title" class="rounded-2xl border border-white/10 bg-white/[0.04] p-4 shadow-lg shadow-slate-950/10 backdrop-blur-sm sm:p-5">
                <h2 class="text-base font-semibold text-white">{{ term.title }}</h2>
                <p class="mt-2 text-sm leading-6 text-slate-300">{{ term.body }}</p>
              </section>
            </div>

            <p class="mt-8 text-sm text-slate-500">Last updated: Mei 2026</p>

            <router-link
              to="/register"
              class="mt-6 inline-flex w-fit items-center gap-2 rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-sm font-semibold text-cyan-100 transition hover:border-cyan-300/35 hover:bg-cyan-300/15 hover:text-white"
            >
              <span aria-hidden="true">&larr;</span>
              Back to Register
            </router-link>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>

<script setup>
import termsImage from '@/asset_landing/terms.svg'

const terms = [
  {
    title: '1. Your Account',
    body: "You're responsible for your login credentials and all learning activity under your account.",
  },
  {
    title: '2. Use of Content',
    body: 'Learning materials, AI responses, notes, quizzes, and study plans are intended for personal learning use and may not be redistributed without permission.',
  },
  {
    title: '3. User Behavior',
    body: 'Use LenteraAI respectfully. Abuse, attempts to disrupt the platform, or harmful behavior may lead to account restrictions or suspension.',
  },
  {
    title: '4. Changes',
    body: 'We may update these terms as the platform evolves. Continued use of LenteraAI means you accept the latest version.',
  },
]
</script>
