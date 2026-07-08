<script setup>
import { ref, onMounted } from 'vue'
const items = ref([])
const loading = ref(true)

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const data = await api.osimart.customers()
    items.value = data.results || data || []
  } catch (e) {
    console.error('Failed to load customers', e)
  } finally {
    loading.value = false
  }
}

async function remove(id) {
  const api = await getApi()
  await api.osimart.deleteCustomer(id)
  items.value = items.value.filter(c => c.id !== id)
}

onMounted(load)
</script>

<template>
  <div>
    <h2 class="text-lg font-semibold text-white mb-4">Customers</h2>
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
