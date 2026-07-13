export const vSpotlight = {
  mounted(el) {
    el.classList.add('spotlight-card')
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top
      el.style.setProperty('--mouse-x', `${x}px`)
      el.style.setProperty('--mouse-y', `${y}px`)
    })
  },
}

export const vMagnetic = {
  mounted(el) {
    el.classList.add('magnetic-btn')
    const strength = 0.3
    el.addEventListener('mousemove', (e) => {
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left - rect.width / 2
      const y = e.clientY - rect.top - rect.height / 2
      el.style.setProperty('--mx', `${x * strength}px`)
      el.style.setProperty('--my', `${y * strength}px`)
    })
    el.addEventListener('mouseleave', () => {
      el.style.setProperty('--mx', '0px')
      el.style.setProperty('--my', '0px')
    })
  },
}
