<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'

const router = useRouter()
const { user, refresh } = useUser()

const stats = ref({ products: 0, categories: 0, brands: 0, collections: 0, orders: 0, banners: 0 })
const recentOrders = ref([])
const pending = ref(true)

onMounted(async () => {
  await refresh()
  if (!user.value?.is_staff) { router.push('/login'); return }
  try {
    const { api } = await import('../utils/api')
    const [prodRes, catRes, brandRes, collRes, ordRes, banRes] = await Promise.allSettled([
      api.osimart.products({ limit: 1 }),
      api.osimart.categories(),
      api.osimart.brands(),
      api.osimart.collections(),
      api.orders.list(),
      api.osimart.banners(),
    ])
    if (prodRes.status === 'fulfilled') stats.value.products = prodRes.value?.count || (prodRes.value?.results || []).length || 0
    if (catRes.status === 'fulfilled') stats.value.categories = (Array.isArray(catRes.value) ? catRes.value : catRes.value?.results || []).length
    if (brandRes.status === 'fulfilled') stats.value.brands = (Array.isArray(brandRes.value) ? brandRes.value : brandRes.value?.results || []).length
    if (collRes.status === 'fulfilled') stats.value.collections = (Array.isArray(collRes.value) ? collRes.value : collRes.value?.results || []).length
    if (ordRes.status === 'fulfilled') {
      const ords = ordRes.value || []
      stats.value.orders = ords.length
      recentOrders.value = ords.slice(0, 5)
    }
    if (banRes.status === 'fulfilled') stats.value.banners = (Array.isArray(banRes.value) ? banRes.value : banRes.value?.results || []).length
  } catch (e) {
    console.error('Admin dashboard error', e)
  } finally {
    pending.value = false
  }
})

</script>

<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-white">Admin Dashboard</h1>
        <p class="text-slate-400 text-sm mt-1">Manage your store from one place.</p>
      </div>
      <div class="flex gap-2">
        <router-link to="/admin/osimart" class="text-xs bg-cyan-600 text-white px-4 py-2 rounded-md hover:bg-cyan-500 transition-colors inline-flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
          Osimart Admin
        </router-link>
      </div>
    </div>

    <div v-if="pending" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-slate-500 text-sm mt-3">Loading admin data...</p>
    </div>

    <template v-else>
      <!-- Store Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Products</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.products }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Categories</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.categories }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Brands</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.brands }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Collections</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.collections }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Orders</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.orders }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-colors">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Banners</p>
          <p class="text-2xl font-bold text-white mt-1">{{ stats.banners }}</p>
        </div>
      </div>

      <!-- Quick Links -->
      <section class="space-y-4">
        <h2 class="text-lg font-semibold text-white">Quick Actions</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
          <router-link to="/admin/osimart/products" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">📦</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Products</span>
          </router-link>
          <router-link to="/admin/osimart/orders" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">📋</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Orders</span>
          </router-link>
          <router-link to="/admin/osimart/categories" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">🏷️</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Categories</span>
          </router-link>
          <router-link to="/admin/osimart/customers" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">👥</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Customers</span>
          </router-link>
          <router-link to="/admin/osimart/banners" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">🖼️</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Banners</span>
          </router-link>
          <router-link to="/admin/osimart/brands" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">🏢</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Brands</span>
          </router-link>
          <router-link to="/admin/analytics" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">📊</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Analytics</span>
          </router-link>
          <router-link to="/admin/osimart/store" class="bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-cyan-700 transition-all duration-200 text-center group">
            <span class="text-2xl block mb-1">⚙️</span>
            <span class="text-xs text-slate-400 group-hover:text-white">Store Settings</span>
          </router-link>
        </div>
      </section>

      <!-- Recent Orders -->
      <section v-if="recentOrders.length" class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">Recent Orders</h2>
          <router-link to="/admin/osimart/orders" class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors">View all →</router-link>
        </div>
        <div class="space-y-2">
          <div v-for="o in recentOrders" :key="o.id" class="bg-slate-900 rounded-xl p-3.5 border border-slate-800 hover:border-slate-700 transition-all duration-200 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div>
                <p class="text-sm text-white font-medium">Order #{{ o.id }}</p>
                <p class="text-xs text-slate-500">{{ o.name || o.email }} · {{ new Date(o.created_at).toLocaleDateString() }}</p>
              </div>
            </div>
            <span class="text-xs px-2.5 py-1 rounded-full font-medium"
              :class="o.status === 'delivered' ? 'bg-emerald-900/40 text-emerald-300' : o.status === 'shipped' ? 'bg-cyan-900/40 text-cyan-300' : 'bg-slate-800 text-slate-400'">
              {{ (o.status || 'pending').replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
            </span>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>
