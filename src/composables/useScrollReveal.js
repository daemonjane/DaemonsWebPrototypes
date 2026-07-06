import { onMounted, onUnmounted } from 'vue'

export function useScrollReveal(threshold = 0.08) {
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          const el = entry.target
          const delay = Number(el.dataset.revealDelay) || 0
          const stagger = Number(el.dataset.revealStagger) || 0
          if (stagger) {
            const children = el.children
            for (let i = 0; i < children.length; i++) {
              const child = children[i]
              const d = delay + i * stagger
              child.style.transitionDelay = `${d}ms`
              child.classList.add('revealed')
            }
          } else {
            setTimeout(() => el.classList.add('revealed'), delay)
          }
          observer.unobserve(el)
        }
      }
    },
    { threshold }
  )

  const observe = (el) => {
    if (el && el.nodeType === 1) observer.observe(el)
  }

  onUnmounted(() => observer.disconnect())

  return { observe }
}
