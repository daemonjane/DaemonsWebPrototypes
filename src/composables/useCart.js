import { ref, computed, watch } from 'vue'
import { useToast } from './useToast'

const STORAGE_KEY = 'techstore_cart'
let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const localCart = ref(stored)
const serverCart = ref(null)
let useServer = false

watch(localCart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

function osimartItemToLocal(item) {
  return {
    id: item.item_id || item.product_id || item.id || `item-${Date.now()}`,
    _serverId: item.id,
    name: item.name || item.product_name || '',
    price: parseFloat(item.price || item.unit_price || 0),
    quantity: item.quantity || 1,
    image: item.image || item.product_image || '',
    type: item.item_type || item.type || 'product',
  }
}

export function useCart() {
  const { addToast } = useToast()

  const cart = computed(() => {
    if (useServer && serverCart.value) {
      const raw = serverCart.value.cart || serverCart.value.items || serverCart.value.products || serverCart.value || {}
      if (Array.isArray(raw)) return raw.map(osimartItemToLocal)
      if (raw && typeof raw === 'object') return Object.values(raw).map(osimartItemToLocal)
      return []
    }
    return localCart.value
  })

  const totalItems = computed(() => {
    if (useServer && serverCart.value) {
      const raw = serverCart.value.cart || {}
      if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
        return Object.values(raw).reduce((s, i) => s + (i.quantity || 1), 0)
      }
      return serverCart.value.total_items ?? serverCart.value.total_quantity ?? cart.value.reduce((s, i) => s + i.quantity, 0)
    }
    return localCart.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    if (useServer && serverCart.value) {
      return parseFloat(serverCart.value.total_price ?? serverCart.value.total ?? 0)
    }
    return localCart.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
  })

  async function init() {
    try {
      const { useUser } = await import('./useUser')
      const { user } = useUser()
      if (!user.value) {
        useServer = false
        return
      }
      const { api } = await import('../utils/api')
      const data = await api.osimartCart.view()
      serverCart.value = data
      useServer = true
    } catch {
      useServer = false
    }
  }

  async function refresh() {
    if (!useServer) return
    try {
      const { api } = await import('../utils/api')
      serverCart.value = await api.osimartCart.view()
    } catch {
      useServer = false
    }
  }

  async function addItem(product, quantity = 1) {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        serverCart.value = await api.osimartCart.updateItem({
          item_id: product.variantId || product.uuid || product.id,
          action: 'add',
          quantity,
          name: product.name,
          price: product.price,
          image: product.image || '',
          item_type: product.type || 'product',
        })
        addToast(`Added ${product.name} to cart`, 3000, 'success')
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    const existing = localCart.value.find(p => p.id === product.id)
    if (existing) {
      existing.quantity += quantity
      addToast(`Updated quantity of ${product.name} (${existing.quantity})`, 3000, 'success')
    } else {
      localCart.value.push({ ...product, quantity })
      addToast(`Added ${product.name} to cart`, 3000, 'success')
    }
  }

  async function updateQuantity(productId, delta) {
    if (useServer) {
      try {
        const item = cart.value.find(p => p.id === productId)
        if (!item) return
        const newQty = item.quantity + delta
        const { api } = await import('../utils/api')
        if (newQty <= 0) {
          serverCart.value = await api.osimartCart.updateItem({
            item_id: item._serverId || productId,
            action: 'remove',
          })
          addToast('Removed from cart', 3000, 'error')
        } else {
          serverCart.value = await api.osimartCart.updateItem({
            item_id: item._serverId || productId,
            action: 'update_quantity',
            quantity: newQty,
          })
          addToast(`Updated quantity (${newQty})`, 3000, 'success')
        }
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    const item = localCart.value.find(p => p.id === productId)
    if (!item) return
    item.quantity += delta
    if (item.quantity <= 0) {
      localCart.value = localCart.value.filter(p => p.id !== productId)
      addToast('Removed from cart', 3000, 'error')
    } else {
      addToast(`Updated quantity (${item.quantity})`, 3000, 'success')
    }
  }

  async function removeItem(productId) {
    if (useServer) {
      try {
        const item = cart.value.find(p => p.id === productId)
        if (!item) return
        const { api } = await import('../utils/api')
        serverCart.value = await api.osimartCart.updateItem({
          item_id: item._serverId || productId,
          action: 'remove',
        })
        addToast('Removed from cart', 3000, 'error')
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    localCart.value = localCart.value.filter(p => p.id !== productId)
    addToast('Removed from cart', 3000, 'error')
  }

  async function clearCart() {
    if (useServer) {
      try {
        const items = cart.value
        const { api } = await import('../utils/api')
        for (const item of items) {
          await api.osimartCart.updateItem({
            item_id: item._serverId || item.id,
            action: 'remove',
          })
        }
        serverCart.value = await api.osimartCart.view()
        addToast('Cart cleared', 2000, 'success')
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    localCart.value = []
    addToast('Cart cleared', 2000, 'error')
  }

  async function addUpgrade(id, name, price) {
    const item = { id, name, price, quantity: 1, type: 'upgrade' }
    await addItem(item)
  }

  async function removeUpgrade(id, name) {
    if (useServer) {
      const item = cart.value.find(p => p.id === id)
      if (!item) return
      await removeItem(item._serverId || id)
      return
    }
    localCart.value = localCart.value.filter(item => item.id !== id)
    addToast(`Removed ${name}`, 3000, 'error')
  }

  async function setMembership(type, name, price) {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        const itemsToRemove = cart.value.filter(i => i.type === 'membership')
        for (const item of itemsToRemove) {
          await api.osimartCart.updateItem({
            item_id: item._serverId || item.id,
            action: 'remove',
          })
        }
        if (type) {
          serverCart.value = await api.osimartCart.updateItem({
            item_id: `membership-${type}`,
            action: 'add',
            name,
            price,
            quantity: 1,
            item_type: 'membership',
          })
        } else {
          serverCart.value = await api.osimartCart.view()
        }
        addToast(type ? `Selected ${name}` : 'Membership removed', 3000, 'success')
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    localCart.value = localCart.value.filter(item => item.type !== 'membership')
    if (type) {
      localCart.value.push({ id: `membership-${type}`, name, price, quantity: 1, type: 'membership' })
      addToast(`Selected ${name}`, 3000, 'success')
    }
  }

  async function mergeLocalIntoServer() {
    const items = localCart.value
    if (items.length === 0) {
      useServer = true
      return
    }
    try {
      const { api } = await import('../utils/api')
      for (const item of items) {
        await api.osimartCart.updateItem({
          item_id: item.id,
          action: 'add',
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          image: item.image || '',
          item_type: item.type || 'product',
        })
      }
      serverCart.value = await api.osimartCart.view()
      localCart.value = []
      useServer = true
    } catch {
      useServer = false
    }
  }

  return {
    cart, totalItems, totalPrice,
    init, refresh, mergeLocalIntoServer,
    addItem, updateQuantity, removeItem, clearCart, addUpgrade, removeUpgrade, setMembership,
  }
}
