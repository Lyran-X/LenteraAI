<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-8 text-white sm:px-6 lg:px-8">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_18%_12%,rgba(0,194,255,0.16),transparent_34%),radial-gradient(circle_at_82%_18%,rgba(127,86,255,0.18),transparent_32%),linear-gradient(135deg,#070b19_0%,#0d1226_54%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.22] [background-image:linear-gradient(rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.05)_1px,transparent_1px)] [background-size:48px_48px]" />
      <div class="absolute -left-28 top-24 h-72 w-72 rounded-full bg-cyan-400/20 blur-3xl" />
      <div class="absolute -right-20 bottom-10 h-80 w-80 rounded-full bg-violet-500/20 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-6xl items-center">
      <div class="grid w-full overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.035] shadow-2xl shadow-cyan-950/30 backdrop-blur-2xl lg:grid-cols-[minmax(0,0.95fr)_minmax(420px,1.05fr)]">
        <aside class="relative min-h-[420px] overflow-hidden border-b border-white/10 bg-[#0d1226]/70 p-6 sm:p-8 lg:min-h-[720px] lg:border-b-0 lg:border-r lg:p-10">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_24%,rgba(0,194,255,0.18),transparent_32%),radial-gradient(circle_at_24%_78%,rgba(127,86,255,0.16),transparent_34%)]" />
          <div class="absolute inset-x-8 top-8 h-px bg-gradient-to-r from-transparent via-cyan-300/40 to-transparent" />

          <div class="relative z-10 flex h-full flex-col justify-between gap-6">
            <div class="pt-1 lg:pt-3">
              <div class="rounded-3xl border border-white/10 bg-white/[0.045] p-5 shadow-xl shadow-cyan-950/20 backdrop-blur-xl sm:p-6">
                <p class="text-sm font-semibold uppercase tracking-[0.22em] text-cyan-200/80">AI learning workspace</p>
                <h1 class="mt-4 text-3xl font-bold leading-tight text-white sm:text-4xl lg:text-5xl">
                  Welcome to
                  <span class="block bg-gradient-to-r from-white via-slate-100 to-cyan-200 bg-clip-text text-transparent">LenteraAI</span>
                </h1>
                <p class="mt-4 text-sm leading-6 text-slate-300 sm:text-base">
                  Begin your smarter learning journey with AI-powered tutoring, quizzes, document learning, and adaptive study plans.
                </p>
                <router-link to="/" class="mt-5 inline-flex items-center gap-2 text-sm font-semibold text-cyan-200 transition hover:text-white">
                  Learn more
                  <span aria-hidden="true">-></span>
                </router-link>
              </div>
            </div>

            <div class="relative mx-auto flex min-h-[300px] w-full max-w-md items-center justify-center overflow-hidden rounded-[2rem] border border-cyan-300/15 bg-slate-950/35 px-3 pb-2 pt-4 shadow-2xl shadow-cyan-500/10 backdrop-blur-xl sm:min-h-[360px] sm:px-4 sm:pb-3 lg:min-h-[420px] lg:max-w-lg lg:pb-4">
              <div class="absolute inset-0 rounded-[2rem] bg-[radial-gradient(circle_at_50%_58%,rgba(0,194,255,0.18),transparent_58%),radial-gradient(circle_at_50%_92%,rgba(127,86,255,0.12),transparent_46%)]" />
              <div ref="lottieContainer" class="relative z-10 h-80 w-80 sm:h-[22rem] sm:w-[22rem] lg:h-[27rem] lg:w-[27rem]"></div>
            </div>
          </div>
        </aside>

        <section class="relative min-w-0 bg-slate-950/35 p-6 sm:p-8 lg:p-10 xl:p-12">
          <div class="mx-auto flex h-full max-w-xl flex-col justify-center">
            <div class="mb-8">
              <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-200/80">Create your account</p>
              <h2 class="mt-3 text-3xl font-bold tracking-tight text-white sm:text-4xl">Start learning smarter.</h2>
              <p class="mt-3 text-sm leading-6 text-slate-400 sm:text-base">
                Register for free and unlock your personalized LenteraAI dashboard.
              </p>
            </div>

            <form class="space-y-5" @submit.prevent="handleRegister">
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <label class="block">
                  <span class="mb-2 block text-sm font-semibold text-slate-200">First name</span>
                  <input
                    v-model="form.firstname"
                    type="text"
                    placeholder="Your first name"
                    class="auth-input"
                    autocomplete="given-name"
                  />
                  <p v-if="errors.firstname?.length" class="mt-2 text-sm text-rose-300">{{ errors.firstname[0] }}</p>
                </label>

                <label class="block">
                  <span class="mb-2 block text-sm font-semibold text-slate-200">Surname</span>
                  <input
                    v-model="form.surname"
                    type="text"
                    placeholder="Your surname"
                    class="auth-input"
                    autocomplete="family-name"
                  />
                </label>
              </div>

              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Email</span>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="you@example.com"
                  class="auth-input"
                  autocomplete="email"
                />
                <p v-if="errors.email?.length" class="mt-2 text-sm text-rose-300">{{ errors.email[0] }}</p>
              </label>

              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Password</span>
                <input
                  v-model="form.password"
                  type="password"
                  placeholder="Minimum 8 characters"
                  class="auth-input"
                  autocomplete="new-password"
                />
                <p v-if="errors.password?.length" class="mt-2 text-sm text-rose-300">{{ errors.password[0] }}</p>
              </label>

              <label class="block">
                <span class="mb-2 block text-sm font-semibold text-slate-200">Confirm password</span>
                <input
                  v-model="form.password_confirmation"
                  type="password"
                  placeholder="Repeat your password"
                  class="auth-input"
                  autocomplete="new-password"
                />
              </label>

              <label class="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.035] p-4 text-sm leading-6 text-slate-300">
                <input
                  id="terms"
                  v-model="form.terms"
                  type="checkbox"
                  class="mt-1 h-4 w-4 rounded border-white/20 bg-slate-950 text-cyan-400 focus:ring-2 focus:ring-cyan-300/40"
                />
                <span>
                  I agree to the
                  <router-link to="/terms" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">Terms of Use</router-link>
                  and
                  <router-link to="/privacy" class="font-semibold text-violet-200 transition hover:text-white hover:underline">Privacy Policy</router-link>.
                </span>
              </label>

              <button
                type="submit"
                :disabled="loading"
                class="group relative inline-flex min-h-12 w-full items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-6 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/20 transition duration-200 hover:-translate-y-0.5 hover:shadow-cyan-500/30 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
              >
                <span class="absolute inset-0 bg-white/0 transition group-hover:bg-white/10" />
                <span class="relative">{{ loading ? 'Creating account...' : 'Create Account' }}</span>
              </button>
            </form>

            <p class="mt-6 text-center text-sm text-slate-400">
              Already have an account?
              <router-link to="/login" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">Log in</router-link>
            </p>
          </div>
        </section>
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
import animationData from '@/landing_assets/lottie/register-animation.json'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const form = ref({ firstname: '', surname: '', email: '', password: '', password_confirmation: '', terms: false })
const errors = ref({ firstname: [], email: [], password: [] })
const loading = ref(false)

const getRedirectTarget = () => {
  const redirect = route.query.redirect
  return typeof redirect === 'string' && redirect.startsWith('/') ? redirect : '/dashboard'
}

const getErrorMessage = (error) => error?.apiMessage ?? error?.message ?? 'Registration failed. Please try again.'

const handleRegister = async () => {
  errors.value = { firstname: [], email: [], password: [] }

  if (!form.value.firstname) errors.value.firstname = ['Firstname is required.']
  if (!form.value.email) errors.value.email = ['Email is required.']
  if (!form.value.password) errors.value.password = ['Password is required.']
  if (form.value.password && form.value.password.length < 8) errors.value.password = ['Password must be at least 8 characters.']

  if (errors.value.firstname.length || errors.value.email.length || errors.value.password.length) {
    Swal.fire({ icon: 'warning', title: 'Incomplete Data', text: 'Please complete the required fields.' })
    return
  }

  if (form.value.password !== form.value.password_confirmation) {
    errors.value.password = ['Password confirmation does not match.']
    Swal.fire({ icon: 'warning', title: 'Password Mismatch', text: 'Please confirm your password correctly.' })
    return
  }

  if (!form.value.terms) {
    Swal.fire({ icon: 'warning', title: 'Oops...', text: 'You must accept the Terms and Privacy Policy!' })
    return
  }

  loading.value = true

  try {
    await authStore.register({
      name: `${form.value.firstname} ${form.value.surname}`.trim(),
      email: form.value.email.trim(),
      password: form.value.password,
    })

    await Swal.fire({ title: 'Account Created!', text: 'Redirecting to Dashboard...', icon: 'success', timer: 900, showConfirmButton: false })
    router.push(getRedirectTarget())
  } catch (error) {
    Swal.fire({ icon: 'error', title: 'Registration Failed', text: getErrorMessage(error) })
  } finally {
    loading.value = false
  }
}

const lottieContainer = ref(null)
let animation = null

onMounted(() => {
  animation = lottie.loadAnimation({ container: lottieContainer.value, renderer: 'svg', loop: true, autoplay: true, animationData })
})

onUnmounted(() => {
  animation?.destroy()
})
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
</style>

