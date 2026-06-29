const OSIMART_BASE = 'https://api.osimart.com'

export function resolveImage(mainImage) {
  if (!mainImage) return '/assets/placeholder.svg'
  if (typeof mainImage === 'string') {
    if (mainImage.startsWith('http')) return mainImage
    return `${OSIMART_BASE}/${mainImage.replace(/^\//, '')}`
  }
  const path = mainImage.path || mainImage.url
  if (!path) return '/assets/placeholder.svg'
  if (path.startsWith('http')) return path
  return `${OSIMART_BASE}/${path.replace(/^\//, '')}`
}
