import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

import './styles/main.css'

// Lottie Global
import { Vue3Lottie } from 'vue3-lottie'

// AOS (Animate On Scroll)
import AOS from 'aos'
import 'aos/dist/aos.css'

// Create Vue
const app = createApp(App)
const pinia = createPinia()

// Directive outside click
app.directive('click-outside', {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function (event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  },
})

// Register Lottie global
app.component('Vue3Lottie', Vue3Lottie)

// AOS init
AOS.init({
  once: true,
  duration: 500,
  easing: 'ease-in-out',
  offset: 100,
  mirror: false,
})

app.use(pinia)
app.use(router)
app.mount('#app')