<script setup>
import TopNavBar from './components/TopNavBar.vue'
import HeroSection from './components/HeroSection.vue'
import AboutSection from './components/AboutSection.vue'
import FeatureSection from './components/FeatureSection.vue'
import PhilosophySection from './components/PhilosophySection.vue'
import MarqueeShowcase from './components/MarqueeShowcase.vue'
import SelectedProjectsSection from './components/SelectedProjectsSection.vue'
import AppFooter from './components/AppFooter.vue'

// Opsional, kalau masih ingin dipakai
// import ServicesSection from './components/ServicesSection.vue'
// import StrategyCards from './components/StrategyCards.vue'
</script>

<template>
  <div class="landing-layout min-h-screen overflow-x-hidden text-on-surface">
    <TopNavBar />

    <main>
      <HeroSection />
      <AboutSection />
      <FeatureSection />
      <PhilosophySection />
      <MarqueeShowcase />
      <SelectedProjectsSection />
    </main>

    <AppFooter />
  </div>
</template>