<script setup>
import { ref, onMounted } from 'vue'
const loading = ref(true)
const saved = ref(false)
const form = ref({ name: '', primary_color: '', secondary_color: '', website: '', google_analytics_id: '' })

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.store()
    form.value = {
      name: data.name || '',
      primary_color: data.primary_color || '',
      secondary_color: data.secondary_color || '',
      website: data.website || '',
      google_analytics_id: data.google_analytics_id || '',
    }
  } catch (e) {
    console.error('Failed to load store', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    await api.osimart.updateStore(form.value)
    saved.value = true
    setTimeout(() => { saved.value = false }, 2000)
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

onMounted(load)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-white mb-4">Store Settings</h2>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <form v-else @submit.prevent="save" class="max-w-xl space-y-4">
      <div>
        <label class="block text-xs text-slate-500 mb-1">Store Name</label>
        <input v-model="form.name" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      </div>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-xs text-slate-500 mb-1">Primary Color</label>
          <div class="flex gap-2">
            <input v-model="form.primary_color" type="color" class="w-10 h-10 rounded bg-slate-900 border border-slate-700 cursor-pointer" />
            <input v-model="form.primary_color" placeholder="#000000" class="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white font-mono" />
          </div>
        </div>
        <div>
          <label class="block text-xs text-slate-500 mb-1">Secondary Color</label>
          <div class="flex gap-2">
            <input v-model="form.secondary_color" type="color" class="w-10 h-10 rounded bg-slate-900 border border-slate-700 cursor-pointer" />
            <input v-model="form.secondary_color" placeholder="#000000" class="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white font-mono" />
          </div>
        </div>
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Website</label>
        <input v-model="form.website" placeholder="https://..." class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      </div>
      <div>
        <label class="block text-xs text-slate-500 mb-1">Google Analytics ID</label>
        <input v-model="form.google_analytics_id" placeholder="G-XXXXXXXXXX" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white font-mono" />
      </div>
      <button type="submit" class="bg-cyan-600 text-white px-6 py-2.5 rounded text-sm font-semibold hover:bg-cyan-500 transition-colors">Save Settings</button>
      <span v-if="saved" class="text-emerald-400 text-sm ml-3">✓ Saved!</span>
    </form>
  </div>
</template>
