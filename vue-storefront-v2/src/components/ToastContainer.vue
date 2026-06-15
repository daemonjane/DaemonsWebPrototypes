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
      class="bg-cyan-800 text-white px-4 py-2 rounded-md shadow-lg text-sm pointer-events-auto"
      role="status"
      aria-live="polite"
    >
      {{ toast.message }}
    </div>
  </div>
</template>