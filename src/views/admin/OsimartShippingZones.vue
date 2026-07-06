<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)
const editing = ref(null)
const form = ref({ name: '', shipment_price: '' })

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.shippingZones()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load shipping zones', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    const payload = {
      name: form.value.name,
      shipment_price: parseFloat(form.value.shipment_price) || 0,
    }
    if (editing.value) {
      await api.osimart.updateShippingZone(editing.value, payload)
    } else {
      await api.osimart.createShippingZone(payload)
    }
    form.value = { name: '', shipment_price: '' }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  form.value = { name: item.name, shipment_price: String(item.shipment_price ?? '') }
}

async function remove(id) {
  if (!confirm('Delete this shipping zone?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteShippingZone(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { name: '', shipment_price: '' }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-lg font-semibold text-white">Shipping Zones</h2>
    </div>
    <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
      <input v-model="form.name" placeholder="Zone name" required class="flex-1 min-w-[160px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <input v-model="form.shipment_price" type="number" step="0.01" min="0" placeholder="Price" required class="w-28 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">{{ editing ? 'Update' : 'Add' }}</button>
      <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
    </form>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No shipping zones yet.</div>
    <div v-else class="grid gap-2">
      <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800 hover:border-slate-700">
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.name }}</p>
        </div>
        <span class="text-sm text-cyan-400 font-semibold">${{ Number(item.shipment_price).toFixed(2) }}</span>
        <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
    </div>
  </div>
</template>
