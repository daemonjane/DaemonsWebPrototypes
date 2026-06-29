<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)
const editing = ref(null)
const form = ref({ text: '', link: '', active: true })

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.announcementBars()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load announcement bars', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    if (editing.value) {
      await api.osimart.updateAnnouncementBar(editing.value, form.value)
    } else {
      await api.osimart.createAnnouncementBar(form.value)
    }
    form.value = { text: '', link: '', active: true }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  form.value = { text: item.text || '', link: item.link || '', active: item.active !== false }
}

async function remove(id) {
  if (!confirm('Delete this announcement?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteAnnouncementBar(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { text: '', link: '', active: true }
}

onMounted(load)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-white mb-4">Announcement Bars</h2>
    <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
      <input v-model="form.text" placeholder="Announcement text" required class="flex-1 min-w-[200px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.link" placeholder="Link URL (optional)" class="flex-1 min-w-[180px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <label class="flex items-center gap-2 text-sm text-slate-300">
        <input v-model="form.active" type="checkbox" class="rounded border-slate-700 bg-slate-800 text-cyan-500" />
        Active
      </label>
      <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">{{ editing ? 'Update' : 'Add' }}</button>
      <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No announcement bars yet.</div>
    <div v-else class="grid gap-2">
      <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800">
        <span class="text-xs px-2 py-0.5 rounded-full" :class="item.active !== false ? 'bg-emerald-900/30 text-emerald-400' : 'bg-slate-700 text-slate-500'">{{ item.active !== false ? 'Active' : 'Inactive' }}</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.text }}</p>
          <p v-if="item.link" class="text-xs text-cyan-600 truncate">{{ item.link }}</p>
        </div>
        <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
    </div>
  </div>
</template>
