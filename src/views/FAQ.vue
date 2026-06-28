<script setup>
import { ref } from 'vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const faqs = [
  { q: 'How do I place an order?', a: 'Browse the Shop, add items to your cart, and proceed to Checkout. Fill in your shipping details and confirm the order. Since this is a demo, no real payment is processed.' },
  { q: 'What payment methods do you accept?', a: 'We accept all major credit cards (Visa, Mastercard, Amex), PayPal, and cryptocurrency (BTC/ETH). Payment processing is simulated in this demo.' },
  { q: 'How long does shipping take?', a: 'Domestic orders typically arrive within 3-5 business days. International shipping takes 7-14 business days depending on customs clearance.' },
  { q: 'Can I modify or cancel my order?', a: 'Orders can be modified or cancelled within 1 hour of placement. Contact support with your order ID for assistance.' },
  { q: 'What is your return policy?', a: 'We offer a 30-day no-questions-asked return policy on all unopened items. Opened items may be subject to a 15% restocking fee.' },
  { q: 'Do you offer warranty on products?', a: 'All products come with a minimum 1-year manufacturer warranty. Premium systems include a 3-year extended warranty with on-site support.' },
  { q: 'What is the Insights Membership?', a: 'Our membership gives you access to real-time market data, price alerts, historical charts, and priority allocation drops. Monthly and annual plans available.' },
  { q: 'Can I build a custom configuration?', a: 'Yes! Contact our team with your requirements and we\'ll put together a custom quote with optimized pricing for your workload.' },
]

const openIndex = ref(null)

function toggle(i) {
  openIndex.value = openIndex.value === i ? null : i
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Home', to: '/' }, { label: 'FAQ' }]" />
    <h1 class="text-3xl font-bold text-white mb-2">Frequently Asked Questions</h1>
    <p class="text-slate-400 mb-8">Everything you need to know about TechStore, orders, and membership.</p>

    <div class="space-y-3">
      <div
        v-for="(faq, i) in faqs"
        :key="i"
        class="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden transition-all duration-200"
        :class="{ 'border-cyan-800/50': openIndex === i }"
      >
        <button
          @click="toggle(i)"
          class="w-full flex items-center justify-between p-4 sm:p-5 text-left transition-colors hover:bg-slate-800/50"
          :aria-expanded="openIndex === i"
          :aria-controls="`faq-answer-${i}`"
        >
          <span class="text-sm sm:text-base font-medium text-white pr-4">{{ faq.q }}</span>
          <svg
            class="w-4 h-4 shrink-0 text-slate-500 transition-transform duration-200"
            :class="{ 'rotate-180': openIndex === i }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </button>
        <transition
          enter-active-class="transition-all duration-200 ease-out"
          leave-active-class="transition-all duration-150 ease-in"
          enter-from-class="max-h-0 opacity-0"
          enter-to-class="max-h-96 opacity-100"
          leave-from-class="max-h-96 opacity-100"
          leave-to-class="max-h-0 opacity-0"
        >
          <div v-if="openIndex === i" :id="`faq-answer-${i}`" class="overflow-hidden" role="region">
            <p class="px-4 sm:px-5 pb-4 sm:pb-5 text-sm text-slate-400 leading-relaxed border-t border-slate-800 pt-4">{{ faq.a }}</p>
          </div>
        </transition>
      </div>
    </div>

    <div class="mt-10 text-center bg-slate-900 rounded-xl border border-slate-800 p-6 sm:p-8">
      <h2 class="text-lg font-semibold text-white mb-2">Still have questions?</h2>
      <p class="text-sm text-slate-400 mb-4">Our team is ready to help with any inquiries.</p>
      <router-link to="/contact" class="inline-block bg-cyan-600 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-cyan-500 transition-colors">
        Contact Support
      </router-link>
    </div>
  </div>
</template>
