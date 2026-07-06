<script setup>
/**
 * Contact page with validated form and info section.
 * @view
 */
import { reactive, ref } from 'vue'
import { validateForm } from '../utils/validation'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const form = reactive({ name: '', email: '', message: '' })
const errors = reactive({})
const submitted = ref(false)

function submitForm() {
  Object.keys(errors).forEach(k => delete errors[k])
  submitted.value = false
  const validationErrors = validateForm(form, {
    name: ['required'],
    email: ['required', 'email'],
    message: ['required']
  })
  if (Object.keys(validationErrors).length > 0) {
    Object.assign(errors, validationErrors)
    return
  }
  submitted.value = true
  form.name = ''
  form.email = ''
  form.message = ''
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Contact' }]" />
    <h1 class="text-3xl font-bold text-white mb-2">Contact Us</h1>
    <p class="text-slate-400 mb-8">Have a question about a product, build, or order? We're here to help.</p>

    <div class="grid md:grid-cols-2 gap-8">
      <div>
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <h2 class="text-xl font-semibold text-white mb-4">Send a Message</h2>

          <div v-if="submitted" class="bg-emerald-900/30 border border-emerald-800/50 rounded-lg p-4 mb-4 text-emerald-300 text-sm" role="alert" aria-live="polite">
            Thanks for reaching out! We'll get back to you within 24 hours.
          </div>

          <form @submit.prevent="submitForm" novalidate>
            <div class="mb-4">
              <input
                v-model="form.name"
                type="text"
                placeholder="Full Name"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all"
                :class="{ 'border-pink-500': errors.name }"
                :aria-describedby="errors.name ? 'contact-name-error' : undefined"
                aria-required="true"
              >
              <p v-if="errors.name" id="contact-name-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.name }}</p>
            </div>
            <div class="mb-4">
              <input
                v-model="form.email"
                type="email"
                placeholder="Email"
                class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all"
                :class="{ 'border-pink-500': errors.email }"
                :aria-describedby="errors.email ? 'contact-email-error' : undefined"
                aria-required="true"
              >
              <p v-if="errors.email" id="contact-email-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
            </div>
            <div class="mb-4">
              <textarea
                v-model="form.message"
                rows="4"
                placeholder="Your message..."
                class="w-full bg-slate-800 border border-slate-700 rounded-lg p-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-400 transition-all resize-none"
                :class="{ 'border-pink-500': errors.message }"
                :aria-describedby="errors.message ? 'contact-msg-error' : undefined"
                aria-required="true"
              ></textarea>
              <p v-if="errors.message" id="contact-msg-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.message }}</p>
            </div>
            <button type="submit" class="w-full bg-cyan-600 text-white py-3 rounded-lg font-semibold hover:bg-cyan-500 active:scale-95 transition-all" aria-label="Send message">
              Send Message
            </button>
          </form>
        </div>
      </div>

      <div class="space-y-6">
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 space-y-4">
          <h2 class="text-xl font-semibold text-white">Contact Info</h2>
          <div class="space-y-3 text-sm">
            <div class="flex items-center gap-3 text-slate-400">
              <svg class="w-4 h-4 text-cyan-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              <span>support@techstore.com</span>
            </div>
            <div class="flex items-center gap-3 text-slate-400">
              <svg class="w-4 h-4 text-cyan-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
              <span>+1 (555) 789-0123</span>
            </div>
            <div class="flex items-center gap-3 text-slate-400">
              <svg class="w-4 h-4 text-cyan-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
              <span>123 Cyber Lane, Silicon Valley, CA</span>
            </div>
          </div>
        </div>

        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <h2 class="text-xl font-semibold text-white mb-3">Business Hours</h2>
          <div class="space-y-2 text-sm text-slate-400">
            <div class="flex justify-between"><span>Monday - Friday</span><span class="text-slate-300">9:00 AM - 6:00 PM</span></div>
            <div class="flex justify-between"><span>Saturday</span><span class="text-slate-300">10:00 AM - 4:00 PM</span></div>
            <div class="flex justify-between"><span>Sunday</span><span class="text-slate-300">Closed</span></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
