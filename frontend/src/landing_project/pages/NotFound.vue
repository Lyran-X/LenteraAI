<template>
  <div class="min-h-screen bg-gradient-to-r from-purple-300 to-pink-200 flex flex-col justify-center items-center px-6 text-center">
    <!-- Animasi JSON -->
    <div ref="lottieContainer" class="w-[300px] h-[300px] mb-6"></div>

    <!-- Teks Error -->
    <h1 class="text-[6rem] md:text-[8rem] font-bold text-white drop-shadow-lg leading-none">404</h1>
    <p class="text-2xl md:text-3xl text-white mb-4 font-semibold">Oops! Page not found.</p>
    <p class="text-white mb-6 max-w-xl">
      The page you're looking for doesn't exist, has been moved, or is temporarily unavailable.
    </p>

    <!-- Tombol -->
    <router-link
      to="/"
      class="bg-white text-purple-600 font-semibold px-6 py-3 rounded-md shadow-md hover:bg-purple-100 transition"
    >
      ← Back to Home
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import lottie from 'lottie-web'
import errorAnim from '@/landing_assets/lottie/404-error.json' 

const lottieContainer = ref(null)

onMounted(() => {
  lottie.loadAnimation({
    container: lottieContainer.value,
    renderer: 'svg',
    loop: true,
    autoplay: true,
    animationData: errorAnim,
  })
})
</script>

<style scoped>

</style>
