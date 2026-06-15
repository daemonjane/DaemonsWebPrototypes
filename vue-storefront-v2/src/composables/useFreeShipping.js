import { computed } from 'vue'
import { useCart } from './useCart'

const FREE_SHIPPING_THRESHOLD = 150

export function useFreeShipping() {
  const { totalPrice } = useCart()

  const remaining = computed(() => Math.max(0, FREE_SHIPPING_THRESHOLD - totalPrice.value))
  const progress = computed(() => Math.min(100, (totalPrice.value / FREE_SHIPPING_THRESHOLD) * 100))
  const qualifies = computed(() => totalPrice.value >= FREE_SHIPPING_THRESHOLD)

  return { remaining, progress, qualifies, threshold: FREE_SHIPPING_THRESHOLD }
}
