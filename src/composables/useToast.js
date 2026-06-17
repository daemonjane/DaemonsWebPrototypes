import { ref } from 'vue'

/**
 * @typedef {Object} Toast
 * @property {number} id
 * @property {string} message
 * @property {'default'|'success'|'error'} [type]
 */

const toasts = ref([])
let nextId = 0

/**
 * Composable for global toast notifications.
 * Toasts auto-dismiss after a configurable duration.
 *
 * @returns {{
 *   toasts: import('vue').Ref<Toast[]>,
 *   addToast: (message: string, duration?: number, type?: 'default'|'success'|'error') => void
 * }}
 */
export function useToast() {
  function addToast(message, duration = 3000, type = 'default') {
    const id = nextId++
    toasts.value.push({ id, message, type })
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== id)
    }, duration)
  }

  return { toasts, addToast }
}