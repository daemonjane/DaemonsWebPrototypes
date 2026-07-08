<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)
const form = ref({ title: '', link: '', image: '' })
const editing = ref(null)

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.banners()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load banners', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    if (editing.value) {
      await api.osimart.updateBanner(editing.value, form.value)
    } else {
      await api.osimart.createBanner(form.value)
    }
    form.value = { title: '', link: '', image: '' }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  form.value = {
    title: item.title || '',
    link: item.link || '',
    image: typeof item.image === 'object' ? (item.image.path || item.image.image || item.image.id || '') : (item.image || ''),
  }
}

async function remove(id) {
  if (!confirm('Delete this banner?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteBanner(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { title: '', link: '', image: '' }
}

onMounted(load)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-white mb-4">Banners</h2>
    <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
      <input v-model="form.title" placeholder="Title" class="flex-1 min-w-[140px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.link" placeholder="Link URL" class="flex-1 min-w-[180px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.image" placeholder="Image path" class="flex-1 min-w-[180px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <button v-if="editing" type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">Update</button>
      <button v-else type="submit" class="bg-emerald-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-emerald-500">Create</button>
      <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No banners yet.</div>
    <div v-else class="grid gap-2">
      <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800">
        <div class="w-16 h-10 rounded bg-slate-800 overflow-hidden shrink-0">
          <img v-if="item.image" :src="typeof item.image === 'object' ? item.image.path || item.image.image || '' : item.image" alt="" class="w-full h-full object-cover" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.title || 'Untitled' }}</p>
          <p v-if="item.link" class="text-xs text-cyan-600 truncate">{{ item.link }}</p>
        </div>
        <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
    </div>
  </div>
</template>
