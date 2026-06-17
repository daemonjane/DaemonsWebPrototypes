import { ref, computed, watch } from 'vue'
import { useToast } from './useToast'

const STORAGE_KEY = 'techstore_cart'

const cart = ref(JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'))

watch(cart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

/**
 * @typedef {Object} CartItem
 * @property {string} id
 * @property {string} name
 * @property {number} price
 * @property {number} quantity
 * @property {'product'|'upgrade'|'membership'} [type]
 */

/**
 * Composable for managing the shopping cart.
 * Persists cart state to localStorage automatically.
 *
 * @returns {{
 *   cart: import('vue').Ref<CartItem[]>,
 *   totalItems: import('vue').ComputedRef<number>,
 *   totalPrice: import('vue').ComputedRef<number>,
 *   addItem: (product: { id: string, name: string, price: number }, quantity?: number) => void,
 *   updateQuantity: (productId: string, delta: number) => void,
 *   removeItem: (productId: string) => void,
 *   clearCart: () => void,
 *   addUpgrade: (id: string, name: string, price: number) => void,
 *   removeUpgrade: (id: string, name: string) => void,
 *   setMembership: (type: string|null, name: string, price: number) => void
 * }}
 */
export function useCart() {
  const { addToast } = useToast()

  const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0))
  const totalPrice = computed(() => cart.value.reduce((sum, item) => sum + item.price * item.quantity, 0))

  function addItem(product, quantity = 1) {
    const existing = cart.value.find(p => p.id === product.id)
    if (existing) {
      existing.quantity += quantity
      addToast(`Updated quantity of ${product.name} (${existing.quantity})`, 3000, 'success')
    } else {
      cart.value.push({ ...product, quantity })
      addToast(`Added ${product.name} to cart`, 3000, 'success')
    }
  }

  function updateQuantity(productId, delta) {
    const item = cart.value.find(p => p.id === productId)
    if (!item) return
    const oldQuantity = item.quantity
    item.quantity += delta
    if (item.quantity <= 0) {
      cart.value = cart.value.filter(p => p.id !== productId)
      addToast(`Removed ${item.name} from cart`, 3000, 'error')
    } else {
      addToast(`Updated ${item.name} (${oldQuantity} → ${item.quantity})`, 3000, 'success')
    }
  }

  function removeItem(productId) {
    const item = cart.value.find(p => p.id === productId)
    if (item) {
      cart.value = cart.value.filter(p => p.id !== productId)
      addToast(`Removed ${item.name} from cart`, 3000, 'error')
    }
  }

  function clearCart() {
    cart.value = []
    addToast('Cart cleared', 2000, 'error')
  }

  function addUpgrade(id, name, price) {
    // Remove any existing upgrade with the same id
    cart.value = cart.value.filter(item => item.id !== id)
    cart.value.push({ id, name, price, quantity: 1, type: 'upgrade' })
    addToast(`Added ${name}`, 3000, 'success')
  }

  function removeUpgrade(id, name) {
    cart.value = cart.value.filter(item => item.id !== id)
    addToast(`Removed ${name}`, 3000, 'error')
  }

  function setMembership(type, name, price) {
    cart.value = cart.value.filter(item => item.type !== 'membership')
    if (type) {
      cart.value.push({ id: `membership-${type}`, name, price, quantity: 1, type: 'membership' })
      addToast(`Selected ${name}`, 3000, 'success')
    }
  }

  return { cart, totalItems, totalPrice, addItem, updateQuantity, removeItem, clearCart, addUpgrade, removeUpgrade, setMembership }
}