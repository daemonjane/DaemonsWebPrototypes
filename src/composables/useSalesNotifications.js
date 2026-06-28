import { onMounted, onUnmounted } from 'vue'
import { useToast } from './useToast'
import { products } from '../data/products'

let interval = null

export function useSalesNotifications() {
  const { addToast } = useToast()

  function triggerRandomSale() {
    const pool = products.filter(p => p.stock === undefined || p.stock > 0)
    const product = pool[Math.floor(Math.random() * pool.length)]
    const names = ['Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Sam', 'Quinn', 'Taylor', 'Avery', 'Drew']
    const name = names[Math.floor(Math.random() * names.length)]
    addToast(`${name} just purchased ${product.name}`, 3000, 'default')
  }

  function start() {
    if (interval) return
    triggerRandomSale()
    interval = setInterval(triggerRandomSale, 30000)
  }

  function stop() {
    if (interval) {
      clearInterval(interval)
      interval = null
    }
  }

  onMounted(start)
  onUnmounted(stop)

  return { start, stop }
}
