<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)
const editing = ref(null)
const form = ref({ name: '', on_purchase: false })

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.orderStatusChoices()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load order statuses', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    if (editing.value) {
      await api.osimart.updateOrderStatusChoice(editing.value, form.value)
    } else {
      await api.osimart.createOrderStatusChoice(form.value)
    }
    form.value = { name: '', on_purchase: false }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  form.value = { name: item.name, on_purchase: item.on_purchase }
}

async function remove(id) {
  if (!confirm('Delete this order status?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteOrderStatusChoice(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { name: '', on_purchase: false }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-semibold text-white">Order Statuses</h2>
    </div>
    <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
      <input v-model="form.name" placeholder="Status name" required class="flex-1 min-w-[160px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <label class="flex items-center gap-2 text-sm text-slate-300">
        <input v-model="form.on_purchase" type="checkbox" class="rounded bg-slate-900 border-slate-700 text-cyan-500" />
        Set on purchase
      </label>
      <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">{{ editing ? 'Update' : 'Add' }}</button>
      <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No order statuses yet.</div>
    <div v-else class="grid gap-2">
      <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800 hover:border-slate-700">
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.name }}</p>
        </div>
        <span class="text-xs px-2 py-0.5 rounded-full" :class="item.on_purchase ? 'bg-green-900/50 text-green-400' : 'bg-slate-700/50 text-slate-400'">{{ item.on_purchase ? 'On Purchase' : 'Post Purchase' }}</span>
        <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
    </div>
  </div>
</template>
