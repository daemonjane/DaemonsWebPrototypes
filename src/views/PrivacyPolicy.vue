<script setup>
import { ref } from 'vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const lastUpdated = 'June 15, 2026'
const tocOpen = ref(false)
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Privacy' }, { label: 'Privacy Policy' }]" />
    <!-- Header -->
    <div class="mb-10">
      <span class="text-xs font-mono text-cyan-500 uppercase tracking-wider bg-cyan-950/30 px-2 py-1 rounded">Legal</span>
      <h1 class="text-3xl sm:text-4xl font-bold text-white mt-3">Privacy Policy</h1>
      <p class="text-slate-400 mt-2 text-sm">Last updated: {{ lastUpdated }}</p>
    </div>

    <!-- Table of Contents -->
    <div class="bg-slate-900 rounded-xl border border-slate-800 p-5 mb-8">
      <button @click="tocOpen = !tocOpen" class="flex items-center justify-between w-full text-left">
        <span class="text-sm font-semibold text-white">Table of Contents</span>
        <svg class="w-4 h-4 text-slate-400 transition-transform" :class="{ 'rotate-180': tocOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
      </button>
      <div v-if="tocOpen" class="mt-3 space-y-1.5">
        <a href="#information" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">1. Information We Collect</a>
        <a href="#use" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">2. How We Use Your Information</a>
        <a href="#sharing" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">3. Data Sharing & Third Parties</a>
        <a href="#security" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">4. Data Security</a>
        <a href="#rights" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">5. Your Rights</a>
        <a href="#cookies" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">6. Cookies</a>
        <a href="#contact" class="block text-sm text-slate-400 hover:text-cyan-400 transition-colors">7. Contact</a>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-8 text-sm leading-relaxed">
      <section id="information">
        <h2 class="text-xl font-semibold text-white mb-3">1. Information We Collect</h2>
        <p class="text-slate-400">We collect information you provide directly when creating an account, placing an order, or contacting support. This includes your name, email address, shipping address, and payment details. We also automatically collect certain technical data such as IP address, browser type, and device information through standard analytics and cookies.</p>
      </section>

      <section id="use">
        <h2 class="text-xl font-semibold text-white mb-3">2. How We Use Your Information</h2>
        <p class="text-slate-400">Your information is used to process orders, deliver products, send order updates, provide customer support, improve our services, and comply with legal obligations. We may send promotional emails if you opt in; you can unsubscribe at any time.</p>
      </section>

      <section id="sharing">
        <h2 class="text-xl font-semibold text-white mb-3">3. Data Sharing & Third Parties</h2>
        <p class="text-slate-400">We do not sell your personal data. We share information with trusted third-party service providers who assist in payment processing, shipping, analytics, and email delivery. These providers are contractually bound to protect your data.</p>
      </section>

      <section id="security">
        <h2 class="text-xl font-semibold text-white mb-3">4. Data Security</h2>
        <p class="text-slate-400">We implement industry-standard encryption (TLS 1.3) for all data in transit. Payment information is processed by PCI-compliant gateways and is never stored on our servers. Access to personal data is restricted to authorized personnel only.</p>
      </section>

      <section id="rights">
        <h2 class="text-xl font-semibold text-white mb-3">5. Your Rights</h2>
        <p class="text-slate-400">You have the right to access, correct, or delete your personal data at any time. You may also request a copy of the data we hold about you. To exercise these rights, contact us at <a href="mailto:privacy@techstore.test" class="text-cyan-400 hover:underline">privacy@techstore.test</a>.</p>
      </section>

      <section id="cookies">
        <h2 class="text-xl font-semibold text-white mb-3">6. Cookies</h2>
        <p class="text-slate-400">We use essential cookies for cart and session functionality, as well as analytics cookies to improve our store. You can manage cookie preferences in your browser settings. See our <router-link to="/cookies" class="text-cyan-400 hover:underline">Cookie Policy</router-link> for details.</p>
      </section>

      <section id="contact">
        <h2 class="text-xl font-semibold text-white mb-3">7. Contact</h2>
        <p class="text-slate-400">For privacy-related inquiries, email <a href="mailto:privacy@techstore.test" class="text-cyan-400 hover:underline">privacy@techstore.test</a> or write to: TechStore Privacy, 1000 Innovation Drive, San Francisco, CA 94105.</p>
      </section>
    </div>

    <div class="mt-10 pt-6 border-t border-slate-800 text-xs text-slate-600">
      <p>This policy was last updated on {{ lastUpdated }}. We encourage you to review it periodically.</p>
    </div>
  </div>
</template>
