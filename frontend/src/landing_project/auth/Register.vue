<template>
  <main class="relative min-h-screen overflow-hidden bg-[#070b19] px-4 py-5 text-white sm:px-5 lg:px-6">
    <div class="pointer-events-none absolute inset-0">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_18%_12%,rgba(0,194,255,0.1),transparent_32%),radial-gradient(circle_at_82%_18%,rgba(127,86,255,0.12),transparent_32%),linear-gradient(135deg,#070b19_0%,#0d1226_54%,#060c24_100%)]" />
      <div class="absolute inset-0 opacity-[0.14] [background-image:linear-gradient(rgba(255,255,255,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.04)_1px,transparent_1px)] [background-size:40px_40px]" />
      <div class="absolute -left-20 top-20 h-52 w-52 rounded-full bg-cyan-400/14 blur-3xl" />
      <div class="absolute -right-16 bottom-8 h-64 w-64 rounded-full bg-violet-500/14 blur-3xl" />
    </div>

    <section class="relative z-10 mx-auto flex min-h-[calc(100vh-2.5rem)] w-full max-w-4xl items-center">
      <div class="grid w-full overflow-hidden rounded-[1.25rem] border border-white/10 bg-white/[0.035] shadow-[0_20px_64px_rgba(0,0,0,0.3)] backdrop-blur-2xl lg:grid-cols-[minmax(0,0.82fr)_minmax(0,1.18fr)]">
        <aside class="relative min-h-[280px] overflow-hidden border-b border-white/10 bg-[#0d1226]/70 p-4 sm:p-5 lg:min-h-[520px] lg:border-b-0 lg:border-r lg:p-5">
          <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_24%,rgba(0,194,255,0.12),transparent_32%),radial-gradient(circle_at_24%_78%,rgba(127,86,255,0.11),transparent_34%)]" />
          <div class="absolute inset-x-6 top-6 h-px bg-gradient-to-r from-transparent via-cyan-300/30 to-transparent" />

          <div class="relative z-10 flex h-full flex-col justify-between gap-4">
            <div>
              <div class="rounded-[1.15rem] border border-white/10 bg-white/[0.045] p-4 shadow-[0_14px_44px_rgba(8,47,73,0.18)] backdrop-blur-xl">
                <p class="text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-200/80">
                  AI learning workspace
                </p>

                <h1 class="mt-2 text-[25px] font-bold leading-tight text-white sm:text-[30px] lg:text-[34px]">
                  Welcome to
                  <span class="block bg-gradient-to-r from-white via-slate-100 to-cyan-200 bg-clip-text text-transparent">
                    LenteraAI
                  </span>
                </h1>

                <p class="mt-2.5 text-[12.5px] leading-5 text-slate-300 sm:text-[13px]">
                  Begin your smarter learning journey with AI-powered tutoring, quizzes, document learning, and adaptive study plans.
                </p>

                <router-link
                  to="/"
                  class="mt-3 inline-flex items-center gap-2 text-[12px] font-semibold text-cyan-200 transition hover:text-white"
                >
                  Learn more
                  <span aria-hidden="true">-></span>
                </router-link>
              </div>
            </div>

            <div class="relative mx-auto flex min-h-[190px] w-full max-w-xs items-center justify-center overflow-hidden rounded-[1.15rem] border border-cyan-300/15 bg-slate-950/35 px-3 py-3 shadow-[0_16px_54px_rgba(0,194,255,0.07)] backdrop-blur-xl sm:min-h-[220px] lg:min-h-[250px]">
              <div class="absolute inset-0 rounded-[1.15rem] bg-[radial-gradient(circle_at_50%_58%,rgba(0,194,255,0.14),transparent_58%),radial-gradient(circle_at_50%_92%,rgba(127,86,255,0.1),transparent_46%)]" />
              <div
                ref="lottieContainer"
                class="relative z-10 h-48 w-48 sm:h-56 sm:w-56 lg:h-[17rem] lg:w-[17rem]"
              />
            </div>
          </div>
        </aside>

        <section class="relative min-w-0 bg-slate-950/35 p-4 sm:p-5 lg:p-6">
          <div class="mx-auto flex h-full max-w-lg flex-col justify-center">
            <div class="mb-5">
              <p class="text-[10px] font-semibold uppercase tracking-[0.2em] text-cyan-200/80">
                Create your account
              </p>

              <h2 class="mt-1.5 text-[26px] font-bold leading-tight tracking-tight text-white sm:text-[32px]">
                Start learning smarter.
              </h2>

              <p class="mt-2 text-[12.5px] leading-5 text-slate-400 sm:text-[13px]">
                Register for free and unlock your personalized LenteraAI dashboard.
              </p>
            </div>

            <form class="space-y-3" @submit.prevent="handleRegister">
              <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <label class="block">
                  <span class="mb-1.5 block text-[12px] font-semibold text-slate-200">First name</span>
                  <input
                    v-model="form.firstname"
                    type="text"
                    placeholder="Your first name"
                    class="auth-input"
                    autocomplete="given-name"
                  />
                  <p v-if="errors.firstname?.length" class="mt-1.5 text-[12px] text-rose-300">
                    {{ errors.firstname[0] }}
                  </p>
                </label>

                <label class="block">
                  <span class="mb-1.5 block text-[12px] font-semibold text-slate-200">Surname</span>
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
                <span class="mb-1.5 block text-[12px] font-semibold text-slate-200">Email</span>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="you@example.com"
                  class="auth-input"
                  autocomplete="email"
                />
                <p v-if="errors.email?.length" class="mt-1.5 text-[12px] text-rose-300">
                  {{ errors.email[0] }}
                </p>
              </label>

              <label class="block">
                <span class="mb-1.5 block text-[12px] font-semibold text-slate-200">Password</span>
                <input
                  v-model="form.password"
                  type="password"
                  placeholder="Minimum 8 characters"
                  class="auth-input"
                  autocomplete="new-password"
                />
                <p v-if="errors.password?.length" class="mt-1.5 text-[12px] text-rose-300">
                  {{ errors.password[0] }}
                </p>
              </label>

              <label class="block">
                <span class="mb-1.5 block text-[12px] font-semibold text-slate-200">Confirm password</span>
                <input
                  v-model="form.password_confirmation"
                  type="password"
                  placeholder="Repeat your password"
                  class="auth-input"
                  autocomplete="new-password"
                />
              </label>

              <label class="flex items-start gap-2.5 rounded-xl border border-white/10 bg-white/[0.035] p-3 text-[12px] leading-5 text-slate-300">
                <input
                  id="terms"
                  v-model="form.terms"
                  type="checkbox"
                  class="mt-0.5 h-3.5 w-3.5 rounded border-white/20 bg-slate-950 text-cyan-400 focus:ring-2 focus:ring-cyan-300/40"
                />
                <span>
                  I agree to the
                  <router-link to="/terms" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">
                    Terms of Use
                  </router-link>
                  and
                  <router-link to="/privacy" class="font-semibold text-violet-200 transition hover:text-white hover:underline">
                    Privacy Policy
                  </router-link>.
                </span>
              </label>

              <button
                type="submit"
                :disabled="loading"
                class="group relative inline-flex min-h-10 w-full items-center justify-center overflow-hidden rounded-xl bg-gradient-to-r from-cyan-400 via-blue-500 to-violet-500 px-5 py-2.5 text-[13px] font-bold text-white shadow-[0_12px_34px_rgba(6,182,212,0.18)] transition duration-200 hover:-translate-y-0.5 hover:shadow-cyan-500/25 active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-70"
              >
                <span class="absolute inset-0 bg-white/0 transition group-hover:bg-white/10" />
                <span class="relative">{{ loading ? 'Creating account...' : 'Create Account' }}</span>
              </button>
            </form>

            <p class="mt-4 text-center text-[12.5px] text-slate-400">
              Already have an account?
              <router-link to="/login" class="font-semibold text-cyan-200 transition hover:text-white hover:underline">
                Log in
              </router-link>
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

const form = ref({
  firstname: '',
  surname: '',
  email: '',
  password: '',
  password_confirmation: '',
  terms: false
})

const errors = ref({
  firstname: [],
  email: [],
  password: []
})

const loading = ref(false)

const getRedirectTarget = () => {
  const redirect = route.query.redirect
  return typeof redirect === 'string' && redirect.startsWith('/') ? redirect : '/dashboard'
}

const getErrorMessage = (error) => error?.apiMessage ?? error?.message ?? 'Registration failed. Please try again.'

const handleRegister = async () => {
  errors.value = {
    firstname: [],
    email: [],
    password: []
  }

  if (!form.value.firstname) errors.value.firstname = ['Firstname is required.']
  if (!form.value.email) errors.value.email = ['Email is required.']
  if (!form.value.password) errors.value.password = ['Password is required.']
  if (form.value.password && form.value.password.length < 8) {
    errors.value.password = ['Password must be at least 8 characters.']
  }

  if (errors.value.firstname.length || errors.value.email.length || errors.value.password.length) {
    Swal.fire({
      icon: 'warning',
      title: 'Incomplete Data',
      text: 'Please complete the required fields.'
    })
    return
  }

  if (form.value.password !== form.value.password_confirmation) {
    errors.value.password = ['Password confirmation does not match.']
    Swal.fire({
      icon: 'warning',
      title: 'Password Mismatch',
      text: 'Please confirm your password correctly.'
    })
    return
  }

  if (!form.value.terms) {
    Swal.fire({
      icon: 'warning',
      title: 'Oops...',
      text: 'You must accept the Terms and Privacy Policy!'
    })
    return
  }

  loading.value = true

  try {
    await authStore.register({
      name: `${form.value.firstname} ${form.value.surname}`.trim(),
      email: form.value.email.trim(),
      password: form.value.password
    })

    await Swal.fire({
      title: 'Account Created!',
      text: 'Redirecting to Dashboard...',
      icon: 'success',
      timer: 900,
      showConfirmButton: false
    })

    router.push(getRedirectTarget())
  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Registration Failed',
      text: getErrorMessage(error)
    })
  } finally {
    loading.value = false
  }
}

const lottieContainer = ref(null)
let animation = null

onMounted(() => {
  animation = lottie.loadAnimation({
    container: lottieContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData
  })
})

onUnmounted(() => {
  animation?.destroy()
})
</script>

<style scoped>
.auth-input {
  width: 100%;
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.72);
  padding: 0.58rem 0.75rem;
  color: white;
  font-size: 0.8125rem;
  line-height: 1.25rem;
  outline: none;
  transition:
    border-color 180ms ease,
    box-shadow 180ms ease,
    background 180ms ease;
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
  box-shadow:
    0 0 0 3px rgba(34, 211, 238, 0.1),
    0 0 22px rgba(34, 211, 238, 0.07);
}
</style>