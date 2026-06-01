<template>
  <div class="w-full min-w-0 space-y-5 overflow-x-hidden xl:space-y-6">
    <div
      v-if="isLoading"
      class="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-sm font-medium text-cyan-100"
    >
      Loading profile settings...
    </div>

    <div
      v-else-if="errorMessage"
      class="rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-sm font-medium text-rose-100"
    >
      {{ errorMessage }}
    </div>

    <section class="grid min-w-0 grid-cols-1 gap-5 xl:grid-cols-[minmax(18rem,0.78fr)_minmax(0,1.22fr)] xl:gap-6">
      <div class="min-w-0 space-y-5">
        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
          <div class="flex min-w-0 items-center gap-4">
            <button
              class="relative flex h-20 w-20 shrink-0 items-center justify-center overflow-hidden rounded-3xl bg-gradient-to-br from-cyan-300 via-blue-500 to-violet-500 text-xl font-bold text-white shadow-lg shadow-cyan-500/20 transition hover:brightness-110 disabled:cursor-wait disabled:opacity-70"
              type="button"
              :disabled="isUploadingAvatar"
              aria-label="Change profile photo"
              @click="openAvatarPicker"
            >
              <img
                v-if="avatarImageUrl"
                :src="avatarImageUrl"
                alt="Profile avatar"
                class="h-full w-full object-cover"
              />
              <span v-else>{{ avatarInitials }}</span>

              <span
                v-if="isUploadingAvatar"
                class="absolute inset-0 flex items-center justify-center bg-slate-950/70 text-[11px] font-semibold text-cyan-100"
              >
                Uploading...
              </span>
            </button>

            <input
              ref="avatarInput"
              class="hidden"
              type="file"
              accept=".png,.jpg,.jpeg,image/png,image/jpeg"
              @change="handleAvatarSelected"
            />

            <div class="min-w-0 flex-1">
              <h2 class="truncate text-lg font-semibold text-white sm:text-xl">
                {{ displayName }}
              </h2>

              <p class="mt-1 truncate text-sm text-slate-400">
                {{ displayEmail }}
              </p>

              <div class="mt-3 flex flex-wrap gap-2">
                <button
                  class="rounded-xl border border-cyan-300/20 bg-cyan-300/10 px-3 py-2 text-xs font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-wait disabled:opacity-60"
                  type="button"
                  :disabled="isUploadingAvatar"
                  @click="openAvatarPicker"
                >
                  Change profile photo
                </button>

                <button
                  v-if="profile?.avatar_url"
                  class="rounded-xl border border-white/10 bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-wait disabled:opacity-60"
                  type="button"
                  :disabled="isDeletingAvatar"
                  @click="handleDeleteAvatar"
                >
                  {{ isDeletingAvatar ? 'Removing...' : 'Remove photo' }}
                </button>
              </div>
            </div>
          </div>

          <div class="mt-5 divide-y divide-white/8">
            <div
              v-for="item in profileDetails"
              :key="item.label"
              class="flex justify-between gap-4 py-4 text-sm"
            >
              <span class="min-w-0 truncate text-slate-400">{{ item.label }}</span>
              <span class="shrink-0 font-medium text-white">{{ item.value }}</span>
            </div>
          </div>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
          <p class="text-sm font-medium text-rose-200/80">Account settings</p>
          <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">
            Security and data
          </h2>

          <div class="mt-5 space-y-3">
            <button
              class="flex w-full items-center justify-between gap-4 rounded-2xl border border-white/10 bg-white/[0.055] px-4 py-3 text-left text-sm font-semibold text-slate-200 transition hover:bg-white/[0.08]"
              type="button"
              @click="openPasswordModal"
            >
              <span>Change password</span>
              <span class="text-xs text-slate-500">Secure</span>
            </button>

            <button
              class="flex w-full items-center justify-between gap-4 rounded-2xl border border-cyan-300/20 bg-cyan-300/10 px-4 py-3 text-left text-sm font-semibold text-cyan-100 transition hover:bg-cyan-300/15 disabled:cursor-wait disabled:opacity-60"
              type="button"
              :disabled="isExporting"
              @click="handleExportLearningData"
            >
              <span>{{ isExporting ? 'Exporting...' : 'Export learning data' }}</span>
              <span class="text-xs text-cyan-100/70">JSON</span>
            </button>

            <button
              class="flex w-full items-center justify-between gap-4 rounded-2xl border border-rose-300/20 bg-rose-300/10 px-4 py-3 text-left text-sm font-semibold text-rose-100 transition hover:bg-rose-300/15"
              type="button"
              @click="showDeleteAccountUnavailable"
            >
              <span>Delete account</span>
              <span class="text-xs text-rose-100/70">Unavailable</span>
            </button>
          </div>
        </GlassCard>
      </div>

      <form class="min-w-0 space-y-5" @submit.prevent="saveSettings">
        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
          <div>
            <p class="text-sm font-medium text-cyan-200/80">Learning preferences</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">
              Study setup
            </h2>
          </div>

          <div class="mt-5 grid min-w-0 gap-4 md:grid-cols-2">
            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Display name</span>
              <input
                v-model="profileForm.name"
                class="form-control"
                placeholder="Your name"
              />
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Learning level</span>
              <input
                v-model="profileForm.learning_level"
                class="form-control"
                placeholder="Grade 11 / Intermediate"
              />
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Preferred learning style</span>
              <select v-model="profileForm.preferred_learning_style" class="form-control">
                <option
                  v-for="option in tutorModeOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Daily study duration</span>
              <select v-model="profileForm.daily_study_duration" class="form-control">
                <option value="25">25 minutes</option>
                <option value="45">45 minutes</option>
                <option value="60">60 minutes</option>
                <option value="90">90 minutes</option>
              </select>
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Preferred quiz difficulty</span>
              <select v-model="profileForm.preferred_quiz_difficulty" class="form-control">
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
                <option value="adaptive">Adaptive</option>
              </select>
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Target subject</span>
              <input
                v-model="profileForm.target_subject"
                class="form-control"
                placeholder="Linear Algebra"
              />
            </label>

            <label class="grid min-w-0 gap-2 md:col-span-2">
              <span class="text-sm font-medium text-slate-300">Reminder time</span>
              <input
                v-model="profileForm.reminder_time"
                class="form-control"
                type="time"
              />
            </label>
          </div>
        </GlassCard>

        <GlassCard padding="p-4 sm:p-5 lg:p-6" extra-class="min-w-0">
          <div>
            <p class="text-sm font-medium text-violet-200/80">AI settings</p>
            <h2 class="mt-1 text-lg font-semibold text-white sm:text-xl">
              Tutor behavior
            </h2>
          </div>

          <div class="mt-5 grid min-w-0 gap-4 md:grid-cols-2">
            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Default tutor mode</span>
              <select v-model="aiForm.default_tutor_mode" class="form-control">
                <option
                  v-for="option in tutorModeOptions"
                  :key="option.value"
                  :value="option.value"
                >
                  {{ option.label }}
                </option>
              </select>
            </label>

            <label class="grid min-w-0 gap-2">
              <span class="text-sm font-medium text-slate-300">Answer length</span>
              <select v-model="aiForm.answer_length" class="form-control">
                <option value="concise">Concise</option>
                <option value="balanced">Balanced</option>
                <option value="detailed">Detailed</option>
              </select>
            </label>
          </div>

          <div class="mt-5 space-y-3">
            <div
              v-for="toggle in aiToggles"
              :key="toggle.key"
              class="flex items-center justify-between gap-4 rounded-2xl border border-white/8 bg-white/[0.045] p-4"
            >
              <div class="min-w-0">
                <p class="font-semibold text-white">{{ toggle.label }}</p>
                <p class="mt-1 text-sm leading-5 text-slate-400">
                  {{ toggle.description }}
                </p>
              </div>

              <button
                class="relative h-7 w-12 shrink-0 rounded-full border transition"
                :class="aiForm[toggle.key] ? 'border-cyan-300/30 bg-cyan-400/30' : 'border-white/10 bg-white/[0.08]'"
                type="button"
                role="switch"
                :aria-checked="aiForm[toggle.key]"
                @click="aiForm[toggle.key] = !aiForm[toggle.key]"
              >
                <span
                  class="absolute top-1 h-5 w-5 rounded-full bg-white transition"
                  :class="aiForm[toggle.key] ? 'left-6' : 'left-1'"
                />
              </button>
            </div>
          </div>
        </GlassCard>

        <div class="flex flex-col gap-3 sm:flex-row sm:justify-end">
          <button
            class="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-60"
            type="button"
            :disabled="isSaving || isLoading"
            @click="resetSettings"
          >
            Reset
          </button>

          <GradientButton type="submit" :disabled="isSaving || isLoading">
            {{ isSaving ? 'Saving...' : 'Save Settings' }}
          </GradientButton>
        </div>
      </form>
    </section>

    <div
      v-if="showPasswordModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/75 px-4 py-6 backdrop-blur-sm"
    >
      <div class="w-full max-w-lg rounded-3xl border border-white/10 bg-slate-950 p-5 shadow-2xl shadow-cyan-950/40 sm:p-6">
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-sm font-medium text-rose-200/80">Security</p>
            <h2 class="mt-1 text-lg font-semibold text-white">Change password</h2>
          </div>

          <button
            class="rounded-xl border border-white/10 bg-white/[0.06] px-3 py-2 text-xs font-semibold text-slate-300 transition hover:bg-white/10"
            type="button"
            @click="closePasswordModal"
          >
            Close
          </button>
        </div>

        <form class="mt-5 grid gap-4" @submit.prevent="submitPasswordChange">
          <label class="grid gap-2">
            <span class="text-sm font-medium text-slate-300">Current password</span>
            <input
              v-model="passwordForm.current_password"
              class="form-control"
              type="password"
              autocomplete="current-password"
              required
            />
          </label>

          <label class="grid gap-2">
            <span class="text-sm font-medium text-slate-300">New password</span>
            <input
              v-model="passwordForm.new_password"
              class="form-control"
              type="password"
              autocomplete="new-password"
              required
              minlength="8"
            />
          </label>

          <label class="grid gap-2">
            <span class="text-sm font-medium text-slate-300">Confirm new password</span>
            <input
              v-model="passwordForm.confirm_new_password"
              class="form-control"
              type="password"
              autocomplete="new-password"
              required
              minlength="8"
            />
          </label>

          <div class="flex flex-col gap-3 pt-2 sm:flex-row sm:justify-end">
            <button
              class="inline-flex min-h-11 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] px-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10"
              type="button"
              @click="closePasswordModal"
            >
              Cancel
            </button>

            <GradientButton type="submit" :disabled="isChangingPassword">
              {{ isChangingPassword ? 'Changing password...' : 'Change password' }}
            </GradientButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import Swal from 'sweetalert2'

import GlassCard from '../components/GlassCard.vue'
import GradientButton from '../components/GradientButton.vue'
import {
  changePassword,
  deleteAvatar,
  exportLearningData,
  getAssetUrl,
  getProfile,
  updateAiSettings,
  updateProfile,
  uploadAvatar,
} from '../services/profileService'
import { useAuthStore } from '../stores/authStore'

type ToggleKey = 'citation_required' | 'socratic_mode_enabled'

type ProfileResponse = {
  id: string
  name: string
  email: string
  role: string
  avatar_url?: string | null
  learning_level?: string | null
  current_streak?: number
  completed_quizzes?: number
  preferences?: Record<string, any>
  ai_settings?: Record<string, any>
}

const MAX_AVATAR_SIZE = 2 * 1024 * 1024
const AVATAR_TYPES = ['image/png', 'image/jpeg']

const authStore = useAuthStore()

const profile = ref<ProfileResponse | null>(null)
const isLoading = ref(false)
const isSaving = ref(false)
const isUploadingAvatar = ref(false)
const isDeletingAvatar = ref(false)
const isChangingPassword = ref(false)
const isExporting = ref(false)
const showPasswordModal = ref(false)
const errorMessage = ref('')
const avatarInput = ref<HTMLInputElement | null>(null)
const avatarPreviewUrl = ref('')

const profileForm = reactive({
  name: '',
  learning_level: '',
  preferred_learning_style: 'step_by_step',
  daily_study_duration: '45',
  preferred_quiz_difficulty: 'adaptive',
  target_subject: '',
  reminder_time: '',
})

const aiForm = reactive({
  default_tutor_mode: 'explain_simply',
  answer_length: 'balanced',
  citation_required: true,
  socratic_mode_enabled: false,
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_new_password: '',
})

const tutorModeOptions = [
  { value: 'explain_simply', label: 'Explain Simply' },
  { value: 'step_by_step', label: 'Step-by-step' },
  { value: 'socratic', label: 'Socratic' },
  { value: 'give_example', label: 'Give Example' },
  { value: 'practice_question', label: 'Practice Question' },
]

const aiToggles: Array<{
  key: ToggleKey
  label: string
  description: string
}> = [
  {
    key: 'citation_required',
    label: 'Citation required',
    description: 'Ask Document QA to include source references whenever possible.',
  },
  {
    key: 'socratic_mode_enabled',
    label: 'Socratic mode',
    description: 'Encourage the tutor to guide with questions before giving direct answers.',
  },
]

const swalTheme = {
  background: '#0f172a',
  color: '#e5e7eb',
  confirmButtonColor: '#06b6d4',
  cancelButtonColor: '#334155',
}

/**
 * Nilai seperti "string" biasanya muncul dari contoh Swagger/Pydantic
 * atau data dummy saat testing. Helper ini mencegah nilai dummy tampil ke user.
 */
const INVALID_PLACEHOLDER_VALUES = ['string', 'null', 'undefined', 'none', 'n/a', '-']

const normalizeText = (value?: string | number | null, fallback = '') => {
  const text = String(value ?? '').trim()

  if (!text || INVALID_PLACEHOLDER_VALUES.includes(text.toLowerCase())) {
    return fallback
  }

  return text
}

const normalizeSelectValue = (
  value: unknown,
  allowedValues: string[],
  fallback: string,
) => {
  const text = normalizeText(typeof value === 'string' ? value : '', fallback)

  return allowedValues.includes(text) ? text : fallback
}

const normalizeBoolean = (value: unknown, fallback: boolean) => {
  if (typeof value === 'boolean') return value
  return fallback
}

const normalizeProfile = (rawProfile: ProfileResponse): ProfileResponse => {
  return {
    ...rawProfile,
    name: normalizeText(rawProfile.name, ''),
    email: normalizeText(rawProfile.email, ''),
    role: normalizeText(rawProfile.role, 'student'),
    avatar_url: normalizeText(rawProfile.avatar_url, '') || null,
    learning_level: normalizeText(rawProfile.learning_level, '') || null,
    current_streak: Number(rawProfile.current_streak ?? 0),
    completed_quizzes: Number(rawProfile.completed_quizzes ?? 0),
    preferences: rawProfile.preferences || {},
    ai_settings: rawProfile.ai_settings || {},
  }
}

const displayName = computed(() =>
  normalizeText(profile.value?.name || authStore.user?.name, 'EduPath Learner'),
)

const displayEmail = computed(() =>
  normalizeText(profile.value?.email || authStore.user?.email, 'No email available'),
)

const avatarImageUrl = computed(() => {
  const avatarUrl = normalizeText(profile.value?.avatar_url, '')
  return avatarPreviewUrl.value || getAssetUrl(avatarUrl)
})

const avatarInitials = computed(() => {
  const words = displayName.value.trim().split(/\s+/).filter(Boolean)

  if (words.length === 0) return 'EA'

  return words
    .slice(0, 2)
    .map((word: string) => word[0]?.toUpperCase())
    .join('')
})

const profileDetails = computed(() => [
  {
    label: 'Role',
    value: formatRole(normalizeText(profile.value?.role || authStore.user?.role, 'student')),
  },
  {
    label: 'Learning level',
    value: normalizeText(profile.value?.learning_level, 'Not set'),
  },
  {
    label: 'Current streak',
    value: `${profile.value?.current_streak ?? 0} days`,
  },
  {
    label: 'Completed quizzes',
    value: String(profile.value?.completed_quizzes ?? 0),
  },
])

const formatRole = (role: string) => {
  const safeRole = normalizeText(role, 'student')
  return safeRole.charAt(0).toUpperCase() + safeRole.slice(1)
}

const showSuccess = async (message: string) => {
  await Swal.fire({
    ...swalTheme,
    toast: true,
    position: 'top-end',
    icon: 'success',
    title: message,
    showConfirmButton: false,
    timer: 1800,
    timerProgressBar: true,
  })
}

const showError = async (title: string, message?: string) => {
  await Swal.fire({
    ...swalTheme,
    icon: 'error',
    title,
    text: message || 'Please try again.',
  })
}

const syncAuthUser = (nextProfile: ProfileResponse) => {
  authStore.updateUserProfile?.({
    id: nextProfile.id,
    name: normalizeText(nextProfile.name, 'EduPath Learner'),
    email: normalizeText(nextProfile.email, ''),
    role: normalizeText(nextProfile.role, 'student'),
    avatar_url: normalizeText(nextProfile.avatar_url, '') || null,
  })
}

const hydrateForms = (nextProfile: ProfileResponse) => {
  const preferences = nextProfile.preferences || {}
  const aiSettings = nextProfile.ai_settings || {}

  const tutorModeValues = tutorModeOptions.map((option) => option.value)
  const durationValues = ['25', '45', '60', '90']
  const quizDifficultyValues = ['easy', 'medium', 'hard', 'adaptive']
  const answerLengthValues = ['concise', 'balanced', 'detailed']

  profileForm.name = normalizeText(nextProfile.name, '')
  profileForm.learning_level = normalizeText(nextProfile.learning_level, '')
  profileForm.preferred_learning_style = normalizeSelectValue(
    preferences.preferred_learning_style,
    tutorModeValues,
    'step_by_step',
  )
  profileForm.daily_study_duration = normalizeSelectValue(
    String(preferences.daily_study_duration ?? ''),
    durationValues,
    '45',
  )
  profileForm.preferred_quiz_difficulty = normalizeSelectValue(
    preferences.preferred_quiz_difficulty,
    quizDifficultyValues,
    'adaptive',
  )
  profileForm.target_subject = normalizeText(preferences.target_subject, '')
  profileForm.reminder_time = normalizeText(preferences.reminder_time, '')

  aiForm.default_tutor_mode = normalizeSelectValue(
    aiSettings.default_tutor_mode,
    tutorModeValues,
    'explain_simply',
  )
  aiForm.answer_length = normalizeSelectValue(
    aiSettings.answer_length,
    answerLengthValues,
    'balanced',
  )
  aiForm.citation_required = normalizeBoolean(aiSettings.citation_required, true)
  aiForm.socratic_mode_enabled = normalizeBoolean(aiSettings.socratic_mode_enabled, false)
}

const setProfile = (nextProfile: ProfileResponse) => {
  const cleanProfile = normalizeProfile(nextProfile)

  profile.value = cleanProfile
  hydrateForms(cleanProfile)
  syncAuthUser(cleanProfile)
}

const loadProfile = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const data = await getProfile()
    setProfile(data)
  } catch (error: any) {
    errorMessage.value = error.apiMessage ?? 'Unable to load profile settings.'
  } finally {
    isLoading.value = false
  }
}

const saveSettings = async () => {
  isSaving.value = true
  errorMessage.value = ''

  try {
    const cleanName = normalizeText(profileForm.name, '')

    if (!cleanName) {
      await showError('Display name is required', 'Please enter your display name.')
      return
    }

    const profilePayload = {
      name: cleanName,
      learning_level: normalizeText(profileForm.learning_level, '') || null,
      target_subject: normalizeText(profileForm.target_subject, '') || null,
      preferred_learning_style: profileForm.preferred_learning_style,
      daily_study_duration: profileForm.daily_study_duration,
      preferred_quiz_difficulty: profileForm.preferred_quiz_difficulty,
      reminder_time: normalizeText(profileForm.reminder_time, '') || null,
    }

    const aiPayload = {
      default_tutor_mode: aiForm.default_tutor_mode,
      answer_length: aiForm.answer_length,
      citation_required: aiForm.citation_required,
      socratic_mode_enabled: aiForm.socratic_mode_enabled,
    }

    await updateProfile(profilePayload)
    const updated = await updateAiSettings(aiPayload)

    setProfile(updated)
    await showSuccess('Settings saved')
  } catch (error: any) {
    await showError('Failed to save settings', error.apiMessage)
  } finally {
    isSaving.value = false
  }
}

const resetSettings = () => {
  if (profile.value) {
    hydrateForms(profile.value)
    void showSuccess('Settings reset')
  }
}

const openAvatarPicker = () => {
  avatarInput.value?.click()
}

const clearAvatarPreview = () => {
  if (avatarPreviewUrl.value) {
    URL.revokeObjectURL(avatarPreviewUrl.value)
    avatarPreviewUrl.value = ''
  }
}

const handleAvatarSelected = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]

  input.value = ''

  if (!file) return

  if (!AVATAR_TYPES.includes(file.type)) {
    await showError('Unsupported file type', 'Please upload a JPG or PNG image.')
    return
  }

  if (file.size > MAX_AVATAR_SIZE) {
    await showError('File is too large', 'Profile photo must be 2 MB or smaller.')
    return
  }

  clearAvatarPreview()
  avatarPreviewUrl.value = URL.createObjectURL(file)
  isUploadingAvatar.value = true

  try {
    const updated = await uploadAvatar(file)
    setProfile(updated)
    clearAvatarPreview()
    await showSuccess('Profile photo updated')
  } catch (error: any) {
    clearAvatarPreview()
    await showError('Failed to upload profile photo', error.apiMessage)
  } finally {
    isUploadingAvatar.value = false
  }
}

const handleDeleteAvatar = async () => {
  const result = await Swal.fire({
    ...swalTheme,
    icon: 'warning',
    title: 'Remove profile photo?',
    text: 'Your current profile photo will be removed.',
    showCancelButton: true,
    confirmButtonText: 'Remove photo',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#e11d48',
    reverseButtons: true,
  })

  if (!result.isConfirmed) return

  isDeletingAvatar.value = true

  try {
    const updated = await deleteAvatar()
    setProfile(updated)
    await showSuccess('Profile photo removed')
  } catch (error: any) {
    await showError('Failed to remove profile photo', error.apiMessage)
  } finally {
    isDeletingAvatar.value = false
  }
}

const openPasswordModal = () => {
  passwordForm.current_password = ''
  passwordForm.new_password = ''
  passwordForm.confirm_new_password = ''
  showPasswordModal.value = true
}

const closePasswordModal = () => {
  showPasswordModal.value = false
}

const submitPasswordChange = async () => {
  if (passwordForm.new_password !== passwordForm.confirm_new_password) {
    await showError('Passwords do not match', 'Please confirm the same new password.')
    return
  }

  isChangingPassword.value = true

  try {
    await changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password,
    })

    closePasswordModal()

    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_new_password = ''

    await showSuccess('Password changed')
  } catch (error: any) {
    await showError('Failed to change password', error.apiMessage)
  } finally {
    isChangingPassword.value = false
  }
}

const handleExportLearningData = async () => {
  isExporting.value = true

  try {
    const data = await exportLearningData()
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = url
    link.download = 'edupath-learning-data.json'

    document.body.appendChild(link)
    link.click()
    link.remove()

    URL.revokeObjectURL(url)

    await showSuccess('Learning data exported')
  } catch (error: any) {
    await showError('Failed to export learning data', error.apiMessage)
  } finally {
    isExporting.value = false
  }
}

const showDeleteAccountUnavailable = async () => {
  await Swal.fire({
    ...swalTheme,
    icon: 'warning',
    title: 'Delete account is not available yet',
    text: 'Account deletion is intentionally disabled until the backend endpoint is added safely.',
    confirmButtonText: 'Got it',
    confirmButtonColor: '#06b6d4',
  })
}

onMounted(loadProfile)

onBeforeUnmount(() => {
  clearAvatarPreview()
})
</script>

<style scoped>
.form-control {
  min-width: 0;
  border-radius: 1rem;
  border: 1px solid rgb(255 255 255 / 0.1);
  background: rgb(255 255 255 / 0.06);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: white;
  outline: none;
}

.form-control:focus {
  border-color: rgb(103 232 249 / 0.5);
}

select.form-control {
  background-color: rgb(2 6 23);
}

.form-control::placeholder {
  color: rgb(100 116 139);
}
</style>