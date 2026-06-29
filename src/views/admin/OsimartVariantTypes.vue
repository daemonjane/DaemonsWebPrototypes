<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const qunits = ref([])
const loading = ref(true)
const editing = ref(null)
const form = ref({ name: '', values: '' })

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const [vtData, quData] = await Promise.all([
      api.osimart.variantTypes(),
      api.osimart.quantityUnits(),
    ])
    items.value = vtData.results || vtData || []
    qunits.value = quData.results || quData || []
  } catch (e) {
    console.error('Failed to load variant types', e)
  } finally {
    loading.value = false
  }
}

async function save() {
  try {
    const api = await getApi()
    const payload = { name: form.value.name }
    const vals = form.value.values.split(',').map(s => s.trim()).filter(Boolean)
    if (vals.length) payload.values = vals

    if (editing.value) {
      await api.osimart.updateVariantType(editing.value, payload)
    } else {
      await api.osimart.createVariantType(payload)
    }
    form.value = { name: '', values: '' }
    editing.value = null
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  }
}

function edit(item) {
  editing.value = item.id
  const vals = (item.possible_values || []).join(', ')
  form.value = { name: item.name, values: vals }
}

async function remove(id) {
  if (!confirm('Delete this variant type?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteVariantType(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function cancel() {
  editing.value = null
  form.value = { name: '', values: '' }
}

onMounted(load)
</script>

<template>
  <div class="space-y-10">
    <div>
      <h2 class="text-lg font-semibold text-white mb-4">Variant Types</h2>
      <form @submit.prevent="save" class="flex flex-wrap gap-3 mb-4 p-4 bg-slate-800/50 rounded-lg border border-slate-700">
        <input v-model="form.name" placeholder="Name (e.g. Color)" required class="flex-1 min-w-[140px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
        <input v-model="form.values" placeholder="Possible values (comma-separated)" class="flex-[2] min-w-[200px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
        <button type="submit" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">{{ editing ? 'Update' : 'Add' }}</button>
        <button v-if="editing" type="button" @click="cancel" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
      </form>
      <div v-if="loading" class="text-slate-500 text-sm py-4 text-center">Loading...</div>
      <div v-else-if="!items.length" class="text-slate-500 text-sm py-4 text-center">No variant types yet.</div>
      <div v-else class="grid gap-2">
        <div v-for="item in items" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800">
          <p class="text-sm text-white font-medium flex-1">{{ item.name }}</p>
          <div class="flex gap-1 flex-wrap">
            <span v-for="v in (item.possible_values || []).slice(0, 5)" :key="v" class="text-[10px] bg-slate-700 text-slate-300 px-2 py-0.5 rounded-full">{{ v }}</span>
            <span v-if="(item.possible_values || []).length > 5" class="text-[10px] text-slate-500">+{{ (item.possible_values || []).length - 5 }}</span>
          </div>
          <button @click="edit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
          <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
        </div>
      </div>
    </div>
    <div>
      <h2 class="text-lg font-semibold text-white mb-4">Quantity Units</h2>
      <div v-if="loading" class="text-slate-500 text-sm py-4 text-center">Loading...</div>
      <div v-else-if="!qunits.length" class="text-slate-500 text-sm py-4 text-center">No quantity units yet.</div>
      <div v-else class="grid gap-2">
        <div v-for="item in qunits" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800">
          <p class="text-sm text-white font-medium">{{ item.name }}</p>
          <span class="text-xs text-slate-500">{{ item.unit || item.symbol || '-' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
