<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-5 text-white sm:px-5 lg:px-6">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_18%_14%,rgba(0,194,255,0.1),transparent_32%),radial-gradient(circle_at_84%_16%,rgba(127,86,255,0.12),transparent_32%),linear-gradient(135deg,#070b19_0%,#0d1226_56%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.14] [background-image:linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] [background-size:40px_40px]" />
      <div class="absolute -left-20 top-20 h-52 w-52 rounded-full bg-cyan-400/14 blur-3xl" />
      <div class="absolute -right-16 bottom-8 h-64 w-64 rounded-full bg-violet-500/14 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-2.5rem)] w-full max-w-4xl items-center">
      <div class="grid w-full overflow-hidden rounded-[1.25rem] border border-white/10 bg-white/[0.035] shadow-[0_20px_64px_rgba(0,0,0,0.3)] backdrop-blur-2xl lg:grid-cols-[minmax(0,0.82fr)_minmax(0,1.18fr)]">
        <aside class="relative min-h-[240px] overflow-hidden border-b border-white/10 bg-[#0d1226]/70 p-4 sm:p-5 lg:min-h-[440px] lg:border-b-0 lg:border-r lg:p-5">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_34%,rgba(0,194,255,0.12),transparent_34%),radial-gradient(circle_at_48%_74%,rgba(127,86,255,0.11),transparent_40%)]" />
          <div class="absolute inset-x-6 top-6 h-px bg-gradient-to-r from-transparent via-cyan-300/30 to-transparent" />

          <div class="relative z-10 flex h-full items-center justify-center rounded-[1.1rem] border border-white/10 bg-white/[0.035] p-4 shadow-[0_16px_54px_rgba(0,194,255,0.07)] backdrop-blur-xl sm:p-5">
            <img
              :src="termsImage"
              alt="Terms of Use illustration"
              class="w-full max-w-xs object-contain drop-shadow-2xl"
            />
          </div>
        </aside>

        <article class="relative min-w-0 bg-slate-950/35 p-4 sm:p-5 lg:p-6">
          <div class="mx-auto flex h-full max-w-lg flex-col justify-center">
            <p class="text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-200/80">
              LenteraAI policy
            </p>

            <h1 class="mt-1.5 text-[27px] font-bold leading-tight tracking-tight text-white sm:text-[32px] lg:text-[36px]">
              Terms of
              <span class="bg-gradient-to-r from-white via-cyan-100 to-violet-200 bg-clip-text text-transparent">
                Use
              </span>
            </h1>

            <p class="mt-2.5 text-[13px] leading-5 text-slate-400 sm:text-sm">
              By using LenteraAI, you agree to the following terms and responsibilities.
            </p>

            <div class="mt-5 space-y-2.5">
              <section
                v-for="term in terms"
                :key="term.title"
                class="rounded-xl border border-white/10 bg-white/[0.04] p-3 shadow-[0_10px_28px_rgba(2,6,23,0.16)] backdrop-blur-sm"
              >
                <h2 class="text-[14px] font-semibold text-white">
                  {{ term.title }}
                </h2>

                <p class="mt-1 text-[12.5px] leading-5 text-slate-300 sm:text-[13px]">
                  {{ term.body }}
                </p>
              </section>
            </div>

            <p class="mt-5 text-[12px] text-slate-500">
              Last updated: May 2026
            </p>

            <router-link
              to="/register"
              class="mt-3.5 inline-flex w-fit items-center gap-2 rounded-lg border border-cyan-300/20 bg-cyan-300/10 px-3 py-1.5 text-[12px] font-semibold text-cyan-100 transition hover:border-cyan-300/35 hover:bg-cyan-300/15 hover:text-white"
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