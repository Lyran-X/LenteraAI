<script setup>
const services = [
  {
    number: '01',
    title: '3D Modeling',
    description: 'Creation of detailed objects, characters, or environments tailored to specific client needs, ideal for games, products, and visualizations.'
  },
  {
    number: '02',
    title: 'Rendering',
    description: 'High-quality, photorealistic renders that showcase designs with custom lighting, textures, and materials to bring concepts to life.'
  },
  {
    number: '03',
    title: 'Motion Design',
    description: 'Dynamic animations and motion graphics that add energy and storytelling to brands, products, and digital experiences.'
  },
  {
    number: '04',
    title: 'Branding',
    description: 'Crafting cohesive visual identities — from logos to full brand systems — that communicate a clear and memorable presence.'
  },
  {
    number: '05',
    title: 'Web Design',
    description: 'Designing clean, modern, and conversion-focused websites with attention to layout, typography, and user experience.'
  }
]
</script>

<template>
  <section id="services" class="py-section-gap-mobile md:py-section-gap px-margin-x-mobile md:px-margin-x bg-white text-black rounded-t-[60px] relative z-10 -mt-[60px]">
    <div class="max-w-container-max mx-auto">
      <div class="mb-20">
        <span class="font-label-sm text-label-sm text-black/40 uppercase tracking-widest mb-4 block">Capabilities</span>
        <h2 class="font-display-xl-mobile text-display-xl-mobile md:font-display-xl md:text-[120px] font-extrabold uppercase tracking-tighter text-black">Services</h2>
      </div>

      <div class="flex flex-col">
        <div v-for="service in services" :key="service.number" class="border-t last:border-b border-black/10 py-12 md:py-20 flex flex-col md:flex-row md:items-center group">
          <div class="font-display-xl text-4xl md:text-8xl font-extrabold text-black mb-4 md:mb-0 md:w-1/4">{{ service.number }}</div>
          <div class="md:w-1/4">
            <h3 class="font-headline-md text-2xl md:text-4xl font-bold uppercase tracking-tight text-black">{{ service.title }}</h3>
          </div>
          <div class="md:w-2/4">
            <p class="font-body-lg text-body-lg text-black/70 max-w-xl">{{ service.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
