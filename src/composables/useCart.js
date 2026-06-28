import { ref, computed, watch } from 'vue'
import { useToast } from './useToast'

const STORAGE_KEY = 'techstore_cart'
let stored
try { stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') } catch { stored = [] }
const localCart = ref(stored)
const serverCart = ref({ items: [], total_price: 0, total_items: 0 })
let useServer = false

watch(localCart, (newVal) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
}, { deep: true })

function serverToLocal(server) {
  return (server.items || []).map(item => ({
    id: item.product_slug || `item-${item.id}`,
    name: item.name,
    price: item.price,
    quantity: item.quantity,
    image: item.product_image || item.image,
    type: item.item_type,
    _serverId: item.id,
  }))
}

function localToServer(local) {
  return local.map(item => ({
    product_slug: item.type === 'product' ? item.id : undefined,
    name: item.name,
    price: item.price,
    quantity: item.quantity,
    image: item.image || '',
    item_type: item.type || 'product',
  }))
}

export function useCart() {
  const { addToast } = useToast()

  const cart = computed(() => {
    if (useServer) return serverToLocal(serverCart.value)
    return localCart.value
  })

  const totalItems = computed(() => {
    if (useServer) return serverCart.value.total_items || 0
    return localCart.value.reduce((sum, item) => sum + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    if (useServer) return serverCart.value.total_price || 0
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
      const data = await api.cart.get()
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
      serverCart.value = await api.cart.get()
    } catch {
      useServer = false
    }
  }

  async function addItem(product, quantity = 1) {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        serverCart.value = await api.cart.add({
          product_slug: product.id,
          quantity,
          name: product.name,
          price: product.price,
          image: product.image || '',
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
        if (newQty <= 0) {
          const { api } = await import('../utils/api')
          serverCart.value = await api.cart.removeItem(item._serverId)
          addToast('Removed from cart', 3000, 'error')
        } else {
          const { api } = await import('../utils/api')
          serverCart.value = await api.cart.updateItem(item._serverId, { quantity: newQty })
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
        serverCart.value = await api.cart.removeItem(item._serverId)
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
        const { api } = await import('../utils/api')
        serverCart.value = await api.cart.clear()
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    localCart.value = []
    addToast('Cart cleared', 2000, 'error')
  }

  async function addUpgrade(id, name, price) {
    if (useServer) {
      try {
        const { api } = await import('../utils/api')
        serverCart.value = await api.cart.add({ name, price, item_type: 'upgrade', quantity: 1 })
        addToast(`Added ${name}`, 3000, 'success')
      } catch (e) {
        addToast(e.message, 3000, 'error')
      }
      return
    }
    localCart.value = localCart.value.filter(item => item.id !== id)
    localCart.value.push({ id, name, price, quantity: 1, type: 'upgrade' })
    addToast(`Added ${name}`, 3000, 'success')
  }

  async function removeUpgrade(id, name) {
    if (useServer) {
      const item = cart.value.find(p => p.id === id)
      if (item && item._serverId) {
        try {
          const { api } = await import('../utils/api')
          serverCart.value = await api.cart.removeItem(item._serverId)
        } catch {
          // ignore
        }
      }
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
          if (item._serverId) await api.cart.removeItem(item._serverId)
        }
        if (type) {
          serverCart.value = await api.cart.add({ name, price, item_type: 'membership', quantity: 1 })
        } else {
          serverCart.value = await api.cart.get()
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
    if (items.length === 0) return
    try {
      const { api } = await import('../utils/api')
      serverCart.value = await api.cart.merge(items)
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
