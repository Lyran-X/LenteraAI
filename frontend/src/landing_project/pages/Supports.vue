<template>
  <div class="min-h-screen bg-purple-50 py-20 px-6">
    <div class="max-w-5xl mx-auto bg-white rounded-2xl shadow-xl p-10">
      <h1 class="text-4xl font-bold text-purple-700 mb-6 text-center">Need Help?</h1>
      <p class="text-center text-gray-600 text-base leading-normal max-w-2xl mx-auto mb-10">
        We’re here to support you! If you have questions about your account, courses, or technical issues, please refer to the options below.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 text-base leading-normal text-gray-800">
        <div class="bg-purple-100 p-6 rounded-lg shadow hover:shadow-md transition">
          <h2 class="font-bold text-lg text-purple-700 mb-2">📨 Contact Us</h2>
          <p>Send us a message at <span class="font-semibold text-purple-700">support@suxz.com</span>. We'll get back to you within 24 hours.</p>
        </div>
        <div class="bg-purple-100 p-6 rounded-lg shadow hover:shadow-md transition">
          <h2 class="font-bold text-lg text-purple-700 mb-2">💡 Tutorials</h2>
          <p>Learn how to navigate the platform, enroll in courses, and manage your learning journey with ease.</p>
        </div>
        <div class="bg-purple-100 p-6 rounded-lg shadow hover:shadow-md transition">
          <h2 class="font-bold text-lg text-purple-700 mb-2">📁 Billing & Payments</h2>
          <p>Get help with invoices, refunds, and payment issues. All transactions are secure and encrypted.</p>
        </div>
        <div class="bg-purple-100 p-6 rounded-lg shadow hover:shadow-md transition">
          <h2 class="font-bold text-lg text-purple-700 mb-2">🔐 Account & Security</h2>
          <p>Having trouble logging in? Reset your password or update your profile information anytime.</p>
        </div>
      </div>

      <div class="mt-10 text-center">
        <router-link
          to="/"        
          class="inline-block text-purple-700 font-semibold hover:underline"
        >
          ← Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
