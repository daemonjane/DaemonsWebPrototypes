import { onMounted, onUnmounted } from 'vue'
import { useToast } from './useToast'

let interval = null

const productNames = [
  'Vanguard Desktop',
  '34" QD‑OLED Monitor',
  'Cyber‑Pro Keyboard',
  'Gaming Mouse',
  'Wireless Headset',
  'NVMe SSD 2TB',
  'Stream Deck',
  'Gaming Chair',
  'CPU Cooler',
  'Sleeved Cables',
  'Microphone',
  'Ultrawide Monitor',
]

export function useSalesNotifications() {
  const { addToast } = useToast()

  function triggerRandomSale() {
    const name = productNames[Math.floor(Math.random() * productNames.length)]
    const names = ['Alex', 'Jordan', 'Casey', 'Morgan', 'Riley', 'Sam', 'Quinn', 'Taylor', 'Avery', 'Drew']
    const person = names[Math.floor(Math.random() * names.length)]
    addToast(`${person} just purchased ${name}`, 3000, 'default')
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
