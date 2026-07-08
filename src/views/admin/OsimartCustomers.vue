<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.customers(page.value)
    items.value = data.results || data || []
    totalPages.value = data.total_pages || Math.ceil((data.count || 0) / 20) || 1
  } catch (e) {
    console.error('Failed to load customers', e)
  } finally {
    loading.value = false
  }
}

function prevPage() {
  if (page.value > 1) { page.value--; load() }
}

function nextPage() {
  if (page.value < totalPages.value) { page.value++; load() }
}

async function remove(id) {
  if (!confirm('Delete this customer?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteCustomer(id)
    items.value = items.value.filter(c => c.id !== id)
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-white">Customers</h2>
      <div v-if="!loading && items.length" class="flex items-center gap-2 text-sm">
        <button @click="prevPage" :disabled="page <= 1" class="px-3 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors">Prev</button>
        <span class="text-slate-500">Page {{ page }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="page >= totalPages" class="px-3 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors">Next</button>
      </div>
    </div>
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No customers yet.</div>
    <div v-else class="overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left text-slate-500 border-b border-slate-800">
            <th class="pb-3 pr-4 font-medium">Name</th>
            <th class="pb-3 pr-4 font-medium">Email</th>
            <th class="pb-3 pr-4 font-medium">Orders</th>
            <th class="pb-3 font-medium">Joined</th>
            <th class="pb-3 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in items" :key="c.id" class="border-b border-slate-800/50 text-slate-300">
            <td class="py-3 pr-4">{{ c.name || c.username || '\u2014' }}</td>
            <td class="py-3 pr-4 text-cyan-600">{{ c.email || '\u2014' }}</td>
            <td class="py-3 pr-4">{{ c.orders_count || c.order_count || 0 }}</td>
            <td class="py-3 pr-4">{{ c.created_at ? new Date(c.created_at).toLocaleDateString() : '\u2014' }}</td>
            <td class="py-3"><button @click="remove(c.id)" class="text-xs text-red-400 hover:text-red-300">Delete</button></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
