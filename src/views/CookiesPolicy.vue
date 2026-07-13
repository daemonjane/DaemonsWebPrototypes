<script setup>
import { ref, computed } from 'vue'
import { useToast } from '../composables/useToast'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const { addToast } = useToast()
const lastUpdated = 'June 15, 2026'

const preferences = ref({
  essential: true,
  analytics: false,
  marketing: false,
})

const allAccepted = computed(() => preferences.value.essential && preferences.value.analytics && preferences.value.marketing)

function savePreferences() {
  localStorage.setItem('cookie_preferences', JSON.stringify(preferences.value))
  addToast('Cookie preferences saved.', 3000, 'success')
}

function acceptAll() {
  preferences.value = { essential: true, analytics: true, marketing: true }
  savePreferences()
}

function rejectAll() {
  preferences.value = { essential: true, analytics: false, marketing: false }
  savePreferences()
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 py-12">
    <Breadcrumbs :crumbs="[{ label: 'Privacy' }, { label: 'Cookie Policy' }]" />
    <div class="mb-10">
      <span class="text-xs font-mono text-electric-400 uppercase tracking-wider bg-electric-500/10 px-2 py-1 rounded">Legal</span>
      <h1 class="text-3xl sm:text-4xl font-bold text-surface-50 font-display mt-3">Cookie Policy</h1>
      <p class="text-surface-400 mt-2 text-sm">Last updated: {{ lastUpdated }}</p>
    </div>

    <!-- Cookie preference panel -->
    <div class="bg-surface-900 rounded-xl border border-surface-700 p-6 mb-8 space-y-5">
      <h2 class="text-lg font-semibold text-surface-50">Manage Cookie Preferences</h2>

      <div class="space-y-4">
        <!-- Essential -->
        <div class="flex items-center justify-between p-4 bg-surface-800/50 rounded-lg">
          <div class="flex-1">
            <p class="text-surface-50 text-sm font-medium">Essential <span class="text-xs text-surface-500 ml-1">(Always active)</span></p>
            <p class="text-xs text-surface-400 mt-0.5">Required for cart, checkout, and basic site functionality.</p>
          </div>
          <div class="w-10 h-6 bg-success-600 rounded-full flex items-center px-1 justify-end opacity-50 cursor-not-allowed">
            <div class="w-4 h-4 bg-surface-50 rounded-full shadow"></div>
          </div>
        </div>

        <!-- Analytics -->
        <label class="flex items-center justify-between p-4 bg-surface-800/50 rounded-lg cursor-pointer hover:bg-surface-700 transition-colors">
          <div class="flex-1">
            <p class="text-surface-50 text-sm font-medium">Analytics</p>
            <p class="text-xs text-surface-400 mt-0.5">Help us improve by tracking page visits and usage patterns.</p>
          </div>
          <input type="checkbox" v-model="preferences.analytics" class="sr-only">
          <div class="w-10 h-6 rounded-full flex items-center px-1 transition-colors duration-200"
            :class="preferences.analytics ? 'bg-electric-500 justify-end' : 'bg-surface-700 justify-start'">
            <div class="w-4 h-4 bg-surface-50 rounded-full shadow"></div>
          </div>
        </label>

        <!-- Marketing -->
        <label class="flex items-center justify-between p-4 bg-surface-800/50 rounded-lg cursor-pointer hover:bg-surface-700 transition-colors">
          <div class="flex-1">
            <p class="text-surface-50 text-sm font-medium">Marketing</p>
            <p class="text-xs text-surface-400 mt-0.5">Enable personalized product recommendations and offers.</p>
          </div>
          <input type="checkbox" v-model="preferences.marketing" class="sr-only">
          <div class="w-10 h-6 rounded-full flex items-center px-1 transition-colors duration-200"
            :class="preferences.marketing ? 'bg-electric-500 justify-end' : 'bg-surface-700 justify-start'">
            <div class="w-4 h-4 bg-surface-50 rounded-full shadow"></div>
          </div>
        </label>
      </div>

      <div class="flex flex-wrap gap-3 pt-2">
        <button @click="savePreferences"
          class="bg-electric-500 hover:bg-electric-400 text-surface-50 text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Save Preferences
        </button>
        <button @click="acceptAll"
          class="bg-success-600 hover:bg-success-500 text-surface-50 text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Accept All
        </button>
        <button @click="rejectAll"
          class="border border-surface-700 text-surface-400 hover:text-surface-50 text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Reject All
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-8 text-sm leading-relaxed">
      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">What Are Cookies?</h2>
        <p class="text-surface-400">Cookies are small text files stored on your device by your web browser. They help websites remember your preferences, understand how you interact with the site, and deliver a better experience.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">How We Use Cookies</h2>
        <p class="text-surface-400">We use essential cookies for cart and session management, analytics cookies to understand site traffic and usage patterns, and marketing cookies (with your consent) to show relevant product recommendations. You can control non-essential cookies at any time using the panel above.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">Third-Party Cookies</h2>
        <p class="text-surface-400">We may use trusted third-party services (such as Google Analytics) that set their own cookies. These services are contractually bound to handle data in accordance with our Privacy Policy.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-surface-50 font-display mb-3">Managing Cookies</h2>
        <p class="text-surface-400">You can manage or disable cookies through your browser settings. Note that disabling essential cookies may affect site functionality. Most browsers allow you to block or delete cookies under Settings &gt; Privacy &amp; Security.</p>
      </section>
    </div>

    <div class="mt-10 pt-6 border-t border-surface-700 text-xs text-surface-600">
      <p>See our <router-link to="/privacy" class="text-electric-500 hover:underline">Privacy Policy</router-link> for more information on how we handle your data.</p>
    </div>
  </div>
</template>
