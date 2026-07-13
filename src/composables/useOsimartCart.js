import { ref, computed, watch } from 'vue'
import { useToast } from './useToast'

const STORAGE_KEY = 'vertex_cart'
let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const localCart = ref(stored)
const userEmail = ref('')

watch(localCart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

export function useOsimartCart() {
  const { addToast } = useToast()

  const cart = computed(() => localCart.value)

  const totalItems = computed(() =>
    localCart.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  const totalPrice = computed(() =>
    localCart.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  )

  function isInCart(productId) {
    return localCart.value.some(item => item.id === productId)
  }

  async function _getCurrentUser() {
    const { useUser } = await import('./useUser')
    return useUser().user.value
  }

  async function _syncToOsimart(items) {
    try {
      const user = await _getCurrentUser()
      const osimartId = user?.profile?.osimart_customer_id
      if (!osimartId) return
      const { api } = await import('../utils/api')
      for (const item of items) {
        await api.osimartCart.updateItem({
          customer_id: osimartId,
          item_id: item.variantId || item.uuid || item.id,
          action: 'add',
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          image: item.image || '',
          item_type: item.type || 'product',
        })
      }
    } catch {
      // osimart sync is best-effort
    }
  }

  async function init() {
    const user = await _getCurrentUser()
    if (!user) return
    if (localCart.value.length > 0) {
      await _syncToOsimart(localCart.value)
    }
  }

  async function addItem(product, quantity = 1) {
    const existing = localCart.value.find(p => p.id === product.id)
    if (existing) {
      existing.quantity += quantity
      addToast(`Updated quantity of ${product.name} (${existing.quantity})`, 3000, 'success')
    } else {
      localCart.value.push({ ...product, quantity })
      addToast(`Added ${product.name} to cart`, 3000, 'success')
    }
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function updateQuantity(productId, delta) {
    const item = localCart.value.find(p => p.id === productId)
    if (!item) return
    item.quantity += delta
    if (item.quantity <= 0) {
      localCart.value = localCart.value.filter(p => p.id !== productId)
      addToast('Removed from cart', 3000, 'error')
    } else {
      addToast(`Updated quantity (${item.quantity})`, 3000, 'success')
    }
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function removeItem(productId) {
    localCart.value = localCart.value.filter(p => p.id !== productId)
    addToast('Removed from cart', 3000, 'error')
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function clearCart() {
    localCart.value = []
    addToast('Cart cleared', 2000, 'error')
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function addUpgrade(id, name, price) {
    await addItem({ id, name, price, quantity: 1, type: 'upgrade' })
  }

  async function removeUpgrade(id, name) {
    localCart.value = localCart.value.filter(item => item.id !== id)
    addToast(`Removed ${name}`, 3000, 'error')
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function setMembership(type, name, price) {
    localCart.value = localCart.value.filter(item => item.type !== 'membership')
    if (type) {
      localCart.value.push({ id: `membership-${type}`, name, price, quantity: 1, type: 'membership' })
      addToast(`Selected ${name}`, 3000, 'success')
    }
    if (await _getCurrentUser()) _syncToOsimart(localCart.value)
  }

  async function mergeLocalIntoServer() {
    if (await _getCurrentUser() && localCart.value.length > 0) {
      await _syncToOsimart(localCart.value)
    }
  }

  function setUser(email) {
    userEmail.value = email
  }

  return {
    cart, totalItems, totalPrice, isInCart,
    init, mergeLocalIntoServer, setUser,
    addItem, updateQuantity, removeItem, clearCart,
    addUpgrade, removeUpgrade, setMembership,
  }
}
