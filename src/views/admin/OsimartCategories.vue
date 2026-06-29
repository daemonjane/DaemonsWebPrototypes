<script setup>
import { ref, onMounted } from 'vue'
const { api } = await import('../../utils/api')
const items = ref([])
const loading = ref(true)
const editing = ref(null)
const form = ref({ name: '', icon: '', description: '' })

async function load() {
  loading.value = true
  try {
    const data = await api.osimart.categories()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load categories', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    if (editing.value) {
      await api.osimart.updateCategory(editing.value, form.value)
    } else {
      await api.osimart.createCategory(form.value)
    }
    form.value = { name: '', icon: '', description: '' }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  form.value = { name: item.name, icon: item.icon || '', description: item.description || '' }
}

async function remove(id) {
  if (!confirm('Delete this category?')) return
  try {
    await api.osimart.deleteCategory(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { name: '', icon: '', description: '' }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-semibold text-white">Categories</h2>
    </div>
    <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
      <input v-model="form.name" placeholder="Name" required class="flex-1 min-w-[140px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.icon" placeholder="Icon (emoji)" class="w-20 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.description" placeholder="Description" class="flex-1 min-w-[200px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">{{ editing ? 'Update' : 'Add' }}</button>
      <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No categories yet.</div>
    <div v-else class="grid gap-2">
      <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800 hover:border-slate-700">
        <span class="text-lg">{{ item.icon || '📁' }}</span>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.name }}</p>
          <p class="text-xs text-slate-500 truncate">{{ item.description || item.slugified_name || '-' }}</p>
        </div>
        <span class="text-xs text-slate-600">{{ item.product_count || item.products_count || 0 }} products</span>
        <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
    </div>
  </div>
</template>
