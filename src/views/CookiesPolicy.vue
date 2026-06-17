<script setup>
import { ref, computed } from 'vue'
import { useToast } from '../composables/useToast'

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
  addToast('Cookie preferences saved.', 'success')
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
    <div class="mb-10">
      <span class="text-xs font-mono text-cyan-500 uppercase tracking-wider bg-cyan-950/30 px-2 py-1 rounded">Legal</span>
      <h1 class="text-3xl sm:text-4xl font-bold text-white mt-3">Cookie Policy</h1>
      <p class="text-slate-400 mt-2 text-sm">Last updated: {{ lastUpdated }}</p>
    </div>

    <!-- Cookie preference panel -->
    <div class="bg-slate-900 rounded-xl border border-slate-800 p-6 mb-8 space-y-5">
      <h2 class="text-lg font-semibold text-white">Manage Cookie Preferences</h2>

      <div class="space-y-4">
        <!-- Essential -->
        <div class="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg">
          <div class="flex-1">
            <p class="text-white text-sm font-medium">Essential <span class="text-xs text-slate-500 ml-1">(Always active)</span></p>
            <p class="text-xs text-slate-400 mt-0.5">Required for cart, checkout, and basic site functionality.</p>
          </div>
          <div class="w-10 h-6 bg-emerald-600 rounded-full flex items-center px-1 justify-end opacity-50 cursor-not-allowed">
            <div class="w-4 h-4 bg-white rounded-full shadow"></div>
          </div>
        </div>

        <!-- Analytics -->
        <label class="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg cursor-pointer hover:bg-slate-800 transition-colors">
          <div class="flex-1">
            <p class="text-white text-sm font-medium">Analytics</p>
            <p class="text-xs text-slate-400 mt-0.5">Help us improve by tracking page visits and usage patterns.</p>
          </div>
          <input type="checkbox" v-model="preferences.analytics" class="sr-only">
          <div class="w-10 h-6 rounded-full flex items-center px-1 transition-colors duration-200"
            :class="preferences.analytics ? 'bg-cyan-600 justify-end' : 'bg-slate-700 justify-start'">
            <div class="w-4 h-4 bg-white rounded-full shadow"></div>
          </div>
        </label>

        <!-- Marketing -->
        <label class="flex items-center justify-between p-4 bg-slate-800/50 rounded-lg cursor-pointer hover:bg-slate-800 transition-colors">
          <div class="flex-1">
            <p class="text-white text-sm font-medium">Marketing</p>
            <p class="text-xs text-slate-400 mt-0.5">Enable personalized product recommendations and offers.</p>
          </div>
          <input type="checkbox" v-model="preferences.marketing" class="sr-only">
          <div class="w-10 h-6 rounded-full flex items-center px-1 transition-colors duration-200"
            :class="preferences.marketing ? 'bg-cyan-600 justify-end' : 'bg-slate-700 justify-start'">
            <div class="w-4 h-4 bg-white rounded-full shadow"></div>
          </div>
        </label>
      </div>

      <div class="flex flex-wrap gap-3 pt-2">
        <button @click="savePreferences"
          class="bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Save Preferences
        </button>
        <button @click="acceptAll"
          class="bg-emerald-700 hover:bg-emerald-600 text-white text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Accept All
        </button>
        <button @click="rejectAll"
          class="border border-slate-700 text-slate-400 hover:text-white text-sm font-semibold px-5 py-2 rounded-md transition active:scale-95">
          Reject All
        </button>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-8 text-sm leading-relaxed">
      <section>
        <h2 class="text-xl font-semibold text-white mb-3">What Are Cookies?</h2>
        <p class="text-slate-400">Cookies are small text files stored on your device by your web browser. They help websites remember your preferences, understand how you interact with the site, and deliver a better experience.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-white mb-3">How We Use Cookies</h2>
        <p class="text-slate-400">We use essential cookies for cart and session management, analytics cookies to understand site traffic and usage patterns, and marketing cookies (with your consent) to show relevant product recommendations. You can control non-essential cookies at any time using the panel above.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-white mb-3">Third-Party Cookies</h2>
        <p class="text-slate-400">We may use trusted third-party services (such as Google Analytics) that set their own cookies. These services are contractually bound to handle data in accordance with our Privacy Policy.</p>
      </section>

      <section>
        <h2 class="text-xl font-semibold text-white mb-3">Managing Cookies</h2>
        <p class="text-slate-400">You can manage or disable cookies through your browser settings. Note that disabling essential cookies may affect site functionality. Most browsers allow you to block or delete cookies under Settings &gt; Privacy &amp; Security.</p>
      </section>
    </div>

    <div class="mt-10 pt-6 border-t border-slate-800 text-xs text-slate-600">
      <p>See our <router-link to="/privacy" class="text-cyan-400 hover:underline">Privacy Policy</router-link> for more information on how we handle your data.</p>
    </div>
  </div>
</template>
