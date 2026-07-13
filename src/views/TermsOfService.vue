<script setup>
import { ref } from 'vue'
import { useToast } from '../composables/useToast'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const { addToast } = useToast()
const accepted = ref(false)
const lastUpdated = 'June 15, 2026'

function handleAccept() {
  accepted.value = true
  addToast('Terms accepted — welcome aboard.', 3000, 'success')
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Legal' }, { label: 'Terms of Service' }]" />
    <div class="mb-10">
      <span class="text-xs font-mono text-gold-400 uppercase tracking-wider bg-gold-500/10 px-2 py-1 rounded">Legal</span>
      <h1 class="text-3xl sm:text-4xl font-bold text-surface-50 font-display mt-3">Terms of Service</h1>
      <p class="text-surface-400 mt-2 text-sm">Last updated: {{ lastUpdated }}</p>
    </div>

    <!-- Interactive acceptance card -->
    <div class="bg-gradient-to-br from-surface-900 to-surface-800 rounded-xl border border-surface-700 p-6 mb-8">
      <div class="flex items-start gap-4">
        <div class="w-10 h-10 rounded-full bg-gold-800/30 flex items-center justify-center text-gold-500 shrink-0">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
          </svg>
        </div>
        <div class="flex-1">
          <h2 class="text-surface-50 font-semibold mb-1">Acceptance of Terms</h2>
          <p class="text-surface-400 text-sm mb-3">By using Vertex, you agree to these terms. Please read them carefully before making a purchase.</p>
          <button v-if="!accepted" @click="handleAccept"
            class="bg-gold-500 hover:bg-gold-400 text-surface-50 text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
            I Accept
          </button>
          <span v-else class="text-success-500 text-sm font-medium flex items-center gap-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
            </svg>
            Accepted
          </span>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-8 text-sm leading-relaxed">
      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">1. General</h2>
        <p class="text-surface-400">These Terms of Service govern your use of the Vertex website and services. By accessing or purchasing from Vertex, you agree to be bound by these terms. If you do not agree, please discontinue use immediately.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">2. Products & Pricing</h2>
        <p class="text-surface-400">All product descriptions, images, and pricing are subject to change without notice. We reserve the right to modify or discontinue products at any time. Prices are listed in USD and do not include applicable taxes or shipping fees, which are calculated at checkout.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">3. Orders & Payment</h2>
        <p class="text-surface-400">By placing an order, you agree to provide accurate and complete information. We reserve the right to cancel any order due to pricing errors, stock limitations, or suspected fraud. Payment is due at the time of purchase and processed through secure PCI-compliant gateways.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">4. Shipping & Returns</h2>
        <p class="text-surface-400">Shipping estimates are provided as guidelines and are not guaranteed. You may return most unopened products within 30 days of delivery for a full refund. Custom-configured systems and engraved items are non-returnable unless defective.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">5. Limitation of Liability</h2>
        <p class="text-surface-400">Vertex shall not be liable for any indirect, incidental, or consequential damages arising from the use or inability to use our products or services. Our total liability is limited to the amount you paid for the product in question.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">6. Changes to Terms</h2>
        <p class="text-surface-400">We may update these terms at any time. Continued use of the site after changes constitutes acceptance of the new terms. We will notify registered users of material changes via email.</p>
      </section>
    </div>

    <div class="mt-10 pt-6 border-t border-surface-700 text-xs text-surface-600">
      <p>For questions about these terms, contact <a href="mailto:legal@vertexhw.com" class="text-gold-500 hover:underline">legal@vertexhw.com</a>.</p>
    </div>
  </div>
</template>
