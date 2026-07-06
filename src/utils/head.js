export function useHead({ title, meta }) {
  if (title) {
    document.title = title
  }

  if (meta) {
    const existing = document.querySelectorAll('[data-head]')
    existing.forEach(el => el.remove())

    meta.forEach(({ name, property, content }) => {
      if (!content) return
      const el = document.createElement('meta')
      el.setAttribute('data-head', '')
      if (name) el.setAttribute('name', name)
      if (property) el.setAttribute('property', property)
      el.setAttribute('content', content)
      document.head.appendChild(el)
    })
  }
}
