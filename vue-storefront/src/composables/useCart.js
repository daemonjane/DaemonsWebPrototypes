import { ref, computed, watch } from 'vue'
import { useToast } from './useToast'

const STORAGE_KEY = 'techstore_cart'
const cart = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

watch(cart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

export function useCart() {
  const { addToast } = useToast()

  const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
  const totalPrice = computed(() => cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0))

  function addItem(product, quantity = 1) {
    const existing = cart.value.find(p => p.id === product.id)
    if (existing) {
      existing.quantity += quantity
      addToast(`Updated quantity of ${product.name} (${existing.quantity})`)
    } else {
      cart.value.push({ ...product, quantity })
      addToast(`Added ${product.name} to cart`)
    }
  }

  function updateQuantity(productId, delta) {
    const item = cart.value.find(p => p.id === productId)
    if (!item) return
    const oldQuantity = item.quantity
    item.quantity += delta
    if (item.quantity <= 0) {
      cart.value = cart.value.filter(p => p.id !== productId)
      addToast(`Removed ${item.name} from cart`)
    } else {
      addToast(`Updated ${item.name} (${oldQuantity} → ${item.quantity})`)
    }
  }

  function removeItem(productId) {
    const item = cart.value.find(p => p.id === productId)
    if (item) {
      cart.value = cart.value.filter(p => p.id !== productId)
      addToast(`Removed ${item.name} from cart`)
    }
  }

  function clearCart() {
    cart.value = []
    addToast('Cart cleared')
  }

  return { cart, totalItems, totalPrice, addItem, updateQuantity, removeItem, clearCart }
}