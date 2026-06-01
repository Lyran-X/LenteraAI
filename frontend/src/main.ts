import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.ts'
import { useAuthStore } from './stores/authStore'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

if (typeof window !== 'undefined') {
  window.addEventListener('edupath:unauthorized', () => {
    const authStore = useAuthStore(pinia)
    authStore.logout()

    const currentRoute = router.currentRoute.value
    const requiresAuth = currentRoute.matched.some((route) => Boolean(route.meta.requiresAuth))

    if (requiresAuth && currentRoute.name !== 'Login') {
      router.push({ name: 'Login', query: { redirect: currentRoute.fullPath } })
    }
  })
}

app.use(router)
app.mount('#app')