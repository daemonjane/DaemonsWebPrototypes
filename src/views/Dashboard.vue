<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'
import { useRecentlyViewed } from '../composables/useRecentlyViewed'
import EmptyState from '../components/EmptyState.vue'

const router = useRouter()
const { user, isAuthenticated, isStaff, refresh } = useUser()
const { items: recentlyViewed } = useRecentlyViewed()

const orders = ref([])
const favorites = ref([])
const pending = ref(true)

onMounted(async () => {
  await refresh()
  if (!user.value) { router.push('/login'); return }
  try {
    const { api } = await import('../utils/api')
    const [ordRes, favRes] = await Promise.allSettled([
      api.orders.list(),
      api.wishlist.get(),
    ])
    if (ordRes.status === 'fulfilled') orders.value = (ordRes.value || []).slice(0, 3)
    if (favRes.status === 'fulfilled') favorites.value = (favRes.value?.products || []).slice(0, 4)
  } catch (e) {
    console.error('Dashboard fetch error', e)
  } finally {
    pending.value = false
  }
})
</script>

<template>
  <div class="space-y-8">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-white">Welcome back, {{ user?.username || 'Guest' }}</h1>
        <p class="text-slate-400 text-sm mt-1">Here's your account overview.</p>
      </div>
      <div class="flex gap-2">
        <router-link to="/profile" class="text-xs bg-slate-800 text-slate-300 px-4 py-2 rounded-md hover:bg-slate-700 transition-colors">Edit Profile</router-link>
        <router-link v-if="isStaff()" to="/admin/osimart" class="text-xs bg-cyan-800 text-cyan-200 px-4 py-2 rounded-md hover:bg-cyan-700 transition-colors">Admin</router-link>
      </div>
    </div>

    <div v-if="pending" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-slate-500 text-sm mt-3">Loading dashboard...</p>
    </div>

    <template v-else>
      <!-- Quick Stats -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Orders</p>
          <p class="text-2xl font-bold text-white mt-1">{{ orders.length > 2 ? orders.length + '+' : orders.length || 0 }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Favorites</p>
          <p class="text-2xl font-bold text-white mt-1">{{ favorites.length || 0 }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Recently Viewed</p>
          <p class="text-2xl font-bold text-white mt-1">{{ recentlyViewed.length || 0 }}</p>
        </div>
        <div class="bg-slate-900 rounded-xl p-4 border border-slate-800">
          <p class="text-xs text-slate-500 uppercase tracking-wider">Account</p>
          <p class="text-2xl font-bold text-white mt-1 capitalize">{{ user?.profile?.membership_tier || 'Free' }}</p>
        </div>
      </div>

      <!-- Recent Orders -->
      <section class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">Recent Orders</h2>
          <router-link to="/orders" class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors">View all →</router-link>
        </div>
        <div v-if="orders.length" class="space-y-3">
          <router-link v-for="o in orders" :key="o.id" :to="`/orders`" class="block bg-slate-900 rounded-xl p-4 border border-slate-800 hover:border-slate-700 transition-all duration-200">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm text-white font-medium">Order #{{ o.id }}</p>
                <p class="text-xs text-slate-500">{{ new Date(o.created_at).toLocaleDateString() }}</p>
              </div>
              <span class="text-xs px-2.5 py-1 rounded-full font-medium"
                :class="o.status === 'delivered' ? 'bg-emerald-900/40 text-emerald-300' : o.status === 'shipped' ? 'bg-cyan-900/40 text-cyan-300' : 'bg-slate-800 text-slate-400'">
                {{ (o.status || 'pending').replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) }}
              </span>
            </div>
          </router-link>
        </div>
        <EmptyState v-else icon="package" title="No orders yet" message="Start shopping to see your orders here." action-label="Browse Shop" @action="router.push('/shop')" />
      </section>

      <!-- Favorites -->
      <section class="space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">Favorite Products</h2>
          <router-link to="/favorites" class="text-xs text-cyan-400 hover:text-cyan-300 transition-colors">View all →</router-link>
        </div>
        <div v-if="favorites.length" class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <router-link v-for="p in favorites" :key="p.id" :to="`/product/${p.slug || p.id}`" class="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden hover:border-cyan-700 transition-all duration-200 group">
            <div class="h-20 bg-slate-800 overflow-hidden">
              <img :src="p.image || '/assets/placeholder.svg'" :alt="p.name" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            </div>
            <div class="p-2">
              <p class="text-xs text-slate-200 truncate">{{ p.name }}</p>
              <p class="text-cyan-400 text-xs font-mono mt-0.5">${{ parseFloat(p.price || 0).toFixed(2) }}</p>
            </div>
          </router-link>
        </div>
        <p v-else class="text-sm text-slate-500">No favorites yet. Browse the shop and save your favorites!</p>
      </section>

      <!-- Recently Viewed -->
      <section v-if="recentlyViewed.length" class="space-y-4">
        <h2 class="text-lg font-semibold text-white">Recently Viewed</h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <router-link v-for="item in recentlyViewed.slice(0, 4)" :key="item.id" :to="`/product/${item.id}`" class="bg-slate-900 rounded-lg border border-slate-800 overflow-hidden hover:border-cyan-700 transition-all duration-200 group">
            <div class="h-20 bg-slate-800 overflow-hidden">
              <img :src="item.image" :alt="item.name" loading="lazy" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500">
            </div>
            <div class="p-2">
              <p class="text-xs text-slate-200 truncate">{{ item.name }}</p>
              <p class="text-cyan-400 text-xs font-mono mt-0.5">${{ parseFloat(item.price || 0).toFixed(2) }}</p>
            </div>
          </router-link>
        </div>
      </section>
    </template>
  </div>
</template>
