<script setup>
defineProps({
  icon: { type: String, default: 'search' },
  title: { type: String, required: true },
  message: { type: String, default: '' },
  actionLabel: { type: String, default: '' },
  actionTo: { type: String, default: '' },
})

const emit = defineEmits(['action'])


const icons = {
  cart: `<svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>`,
  heart: `<svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>`,
  search: `<svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>`,
  box: `<svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/></svg>`,
}
</script>

<template>
  <div class="flex flex-col items-center justify-center py-16 sm:py-20 text-center space-y-4" role="status" aria-live="polite">
    <div class="text-slate-600" v-html="icons[icon] || icons.search"></div>
    <h3 class="text-xl font-bold text-white">{{ title }}</h3>
    <p v-if="message" class="text-slate-400 text-sm max-w-md">{{ message }}</p>
    <router-link
      v-if="actionLabel && actionTo"
      :to="actionTo"
      class="inline-block mt-2 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold px-6 py-2.5 rounded-md transition-all active:scale-95"
    >
      {{ actionLabel }}
    </router-link>
    <button
      v-else-if="actionLabel"
      @click="emit('action')"
      class="inline-block mt-2 bg-cyan-600 hover:bg-cyan-500 text-white font-semibold px-6 py-2.5 rounded-md transition-all active:scale-95"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>
