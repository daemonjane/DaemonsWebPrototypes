<script setup>
import { ref, onMounted } from 'vue'
import { resolveImage } from '../../utils/images'
const items = ref([])
const loading = ref(true)
const uploadUrl = ref('')

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.medias()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load media', e)
  } finally {
    loading.value = false
  }
}

async function upload() {
  if (!uploadUrl.value.trim()) return
  try {
    const api = await getApi()
    await api.osimart.createMedia({ path: uploadUrl.value.trim() })
    uploadUrl.value = ''
    await load()
  } catch (e) {
    alert('Upload failed: ' + e.message)
  }
}

onMounted(load)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-white mb-4">Media Library</h2>
    <form @submit.prevent="upload" class="flex gap-3 mb-6">
      <input v-model="uploadUrl" placeholder="Image URL to upload" class="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">Upload URL</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No media yet.</div>
    <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div v-for="item in items" :key="item.id" class="bg-slate-800/50 rounded-lg border border-slate-800 overflow-hidden group">
        <div class="aspect-square bg-slate-800 overflow-hidden">
          <img :src="resolveImage(item.path || item.image || '')" :alt="item.path || 'Media'" class="w-full h-full object-cover group-hover:scale-105 transition-transform" loading="lazy" />
        </div>
        <div class="p-2">
          <p class="text-[10px] text-slate-500 truncate">{{ item.path?.split('/').pop() || '—' }}</p>
          <p class="text-[10px] text-slate-600">{{ item.size?.kb ? item.size.kb.toFixed(0) + ' KB' : '' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
