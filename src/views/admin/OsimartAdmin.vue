<script setup>
import { ref } from 'vue'
import OsimartProducts from './OsimartProducts.vue'
import OsimartCategories from './OsimartCategories.vue'
import OsimartBrands from './OsimartBrands.vue'
import OsimartCollections from './OsimartCollections.vue'
import OsimartVariantTypes from './OsimartVariantTypes.vue'
import OsimartBanners from './OsimartBanners.vue'
import OsimartAnnouncements from './OsimartAnnouncements.vue'
import OsimartCustomers from './OsimartCustomers.vue'
import OsimartMedia from './OsimartMedia.vue'
import OsimartStore from './OsimartStore.vue'
import OsimartShippingZones from './OsimartShippingZones.vue'
import OsimartOrderStatuses from './OsimartOrderStatuses.vue'
import OsimartOrders from './OsimartOrders.vue'

const tabs = [
  { id: 'orders', label: 'Orders', icon: '📋' },
  { id: 'products', label: 'Products', icon: '📦' },
  { id: 'categories', label: 'Categories', icon: '📁' },
  { id: 'brands', label: 'Brands', icon: '🏷️' },
  { id: 'collections', label: 'Collections', icon: '📚' },
  { id: 'variant-types', label: 'Variant Types', icon: '🧩' },
  { id: 'banners', label: 'Banners', icon: '🖼️' },
  { id: 'announcements', label: 'Announcements', icon: '📢' },
  { id: 'customers', label: 'Customers', icon: '👥' },
  { id: 'media', label: 'Media', icon: '🎨' },
  { id: 'shipping-zones', label: 'Shipping Zones', icon: '🚚' },
  { id: 'order-statuses', label: 'Order Statuses', icon: '🔄' },
  { id: 'store', label: 'Store Settings', icon: '⚙️' },
]
const activeTab = ref('products')
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-white mb-6">Osimart Management</h1>
    <div class="flex gap-1 flex-wrap border-b border-slate-800 pb-1 mb-8 overflow-x-auto">
      <button v-for="t in tabs" :key="t.id" @click="activeTab = t.id" class="px-4 py-2 text-sm rounded-t-md transition-colors whitespace-nowrap" :class="activeTab === t.id ? 'bg-slate-800 text-cyan-400 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'">{{ t.icon }} {{ t.label }}</button>
    </div>
    <div class="bg-slate-900/50 rounded-xl p-4 sm:p-6 border border-slate-800 min-h-[60vh]">
      <OsimartOrders v-if="activeTab === 'orders'" />
      <OsimartProducts v-else-if="activeTab === 'products'" />
      <OsimartCategories v-else-if="activeTab === 'categories'" />
      <OsimartBrands v-else-if="activeTab === 'brands'" />
      <OsimartCollections v-else-if="activeTab === 'collections'" />
      <OsimartVariantTypes v-else-if="activeTab === 'variant-types'" />
      <OsimartBanners v-else-if="activeTab === 'banners'" />
      <OsimartAnnouncements v-else-if="activeTab === 'announcements'" />
      <OsimartCustomers v-else-if="activeTab === 'customers'" />
      <OsimartMedia v-else-if="activeTab === 'media'" />
      <OsimartShippingZones v-else-if="activeTab === 'shipping-zones'" />
      <OsimartOrderStatuses v-else-if="activeTab === 'order-statuses'" />
      <OsimartStore v-else-if="activeTab === 'store'" />
    </div>
  </div>
</template>
