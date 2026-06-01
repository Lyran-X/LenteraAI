<template>
  <footer class="w-full border-t border-[rgba(0,194,255,0.12)] bg-[linear-gradient(180deg,#070B19_0%,#060C24_100%)] py-14 md:py-20">
    <div class="mx-auto flex w-full max-w-container-max flex-col items-center justify-between gap-8 px-margin-x-mobile text-center md:flex-row md:px-margin-x md:text-left">
      <div>
        <div class="lentera-footer-gradient mb-2 font-headline-md text-5xl">
          LenteraAI
        </div>

        <div class="font-body-md text-body-md text-[#526484]">
          &copy; 2026 LenteraAI. Guided by intelligence.
        </div>
      </div>

      <div class="flex flex-wrap justify-center gap-6 md:justify-end md:gap-8">
        <RouterLink class="font-body-md text-body-md text-[#94A3B8] transition-colors hover:text-[#00C2FF]" to="/privacy">
          Privacy
        </RouterLink>
        <RouterLink class="font-body-md text-body-md text-[#94A3B8] transition-colors hover:text-[#00C2FF]" to="/terms">
          Terms
        </RouterLink>
        <a
          class="font-body-md text-body-md text-[#94A3B8] transition-colors hover:text-[#00C2FF]"
          href="https://www.instagram.com/radn.aly/"
          rel="noopener noreferrer"
          target="_blank"
        >
          Contact
        </a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.lentera-footer-gradient {
  display: inline-block;
  background: linear-gradient(90deg, #ffffff 0%, #e5e7eb 58%, #00c2ff 78%, #7f56ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  -webkit-text-fill-color: transparent;
  text-shadow:
    0 0 24px rgba(0, 194, 255, 0.12),
    0 0 34px rgba(127, 86, 255, 0.1);
}
</style>
