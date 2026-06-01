<script setup lang="ts">
import { useRouter } from 'vue-router'
import Sidebar from '@/components/Sidebar.vue'
import Topbar from '@/components/Topbar.vue'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  router.push({ name: 'Login' })
}
</script>

<template>
  <div class="app-shell flex min-h-screen w-full min-w-0 overflow-x-hidden">
    <Sidebar />

    <div class="flex min-h-screen w-full min-w-0 flex-1 flex-col overflow-x-hidden lg:pl-64">
      <Topbar @logout="logout" />

      <main class="flex-1 min-w-0 overflow-x-hidden px-4 pb-24 pt-4 sm:px-6 lg:pb-8 xl:px-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>