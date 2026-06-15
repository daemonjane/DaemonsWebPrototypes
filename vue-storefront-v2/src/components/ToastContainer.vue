<script setup>
/**
 * Renders global toast notifications in a fixed bottom-right container.
 * Uses `role="status"` and `aria-live="polite"` for screen reader announcements.
 * @component
 */
import { useToast } from '../composables/useToast'
const { toasts } = useToast()
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50 space-y-2 pointer-events-none">
      <!-- Accessibility: live region so screen readers announce new toasts -->
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="[
        'px-4 py-2.5 rounded-md shadow-lg text-sm pointer-events-auto flex items-center gap-2 transition-all',
        toast.type === 'error' ? 'bg-pink-800 text-white' :
        toast.type === 'success' ? 'bg-emerald-800 text-white' :
        'bg-cyan-800 text-white'
      ]"
      role="status"
      aria-live="polite"
    >
      <span v-if="toast.type === 'error'" class="text-pink-200 text-xs font-bold">✕</span>
      <span v-else-if="toast.type === 'success'" class="text-emerald-200 text-xs font-bold">✓</span>
      <span v-else class="text-cyan-200 text-xs font-bold">i</span>
      {{ toast.message }}
    </div>
  </div>
</template>