import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'techstore_cart'
const cart = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

watch(cart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

export function useCart() {
  const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
  const totalPrice = computed(() => cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0))

  function addItem(product, quantity = 1) {
    const existing = cart.value.find(p => p.id === product.id)
    if (existing) {
      existing.quantity += quantity
    } else {
      cart.value.push({ ...product, quantity })
    }
  }

  function updateQuantity(productId, delta) {
    const item = cart.value.find(p => p.id === productId)
    if (item) {
      item.quantity += delta
      if (item.quantity <= 0) {
        cart.value = cart.value.filter(p => p.id !== productId)
      }
    }
  }

  function removeItem(productId) {
    cart.value = cart.value.filter(p => p.id !== productId)
  }

  function clearCart() {
    cart.value = []
  }

  return { cart, totalItems, totalPrice, addItem, updateQuantity, removeItem, clearCart }
}