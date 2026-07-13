import { ref, onMounted, watch } from 'vue'

export function useCountUp(target, duration = 1200) {
  const current = ref(0)
  const prefix = ref('')
  const suffix = ref('')
  let observer = null
  let el = ref(null)

  function parseTarget(val) {
    const str = String(val)
    const match = str.match(/^([^0-9]*)([0-9]+)(.*)$/)
    if (match) {
      prefix.value = match[1]
      return { num: parseInt(match[2], 10), suffix: match[3] }
    }
    return { num: 0, suffix: '' }
  }

  function animate(targetEl) {
    const { num, suffix: sfx } = parseTarget(target.value)
    suffix.value = sfx
    if (num === 0) { current.value = 0; return }

    const start = performance.now()
    const step = (now) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      current.value = Math.round(eased * num)
      if (progress < 1) requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  }

  onMounted(() => {
    if (!el.value) return
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animate(entry.target)
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.3 }
    )
    observer.observe(el.value)
  })

  return { current, prefix, suffix, el }
}
