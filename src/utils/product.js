import { resolveImage } from './images'

export function stripHtml(html) {
  const d = document.createElement('div')
  d.innerHTML = html
  return d.textContent || d.innerText || ''
}

export function pick(arr) {
  return Array.isArray(arr) ? arr : (arr?.results || [])
}

export function normalizeProduct(p) {
  return {
    id: p.slugified_name || p.id,
    uuid: p.id,
    variantId: p.variants?.[0]?.id || null,
    name: p.name,
    category: p.categories?.[0]?.category?.slugified_name || 'uncategorized',
    categoryName: p.categories?.[0]?.category?.name || 'Uncategorized',
    brand: p.brand || null,
    collection: p.collections?.[0]?.slugified_name || p.collections?.[0]?.name || null,
    collections: Array.isArray(p.collections) ? p.collections : [],
    price: parseFloat(p.price_range || '0'),
    image: resolveImage(p.main_image),
    description: stripHtml(p.description || ''),
    createdAt: p.created_at || p.date_created || null,
    rating: 4.5,
    stock: Math.max(0, Number(p.remaining_stock ?? p.stock ?? p.quantity ?? 0) || 0),
    specs: (p.sections || []).flatMap(s => (s.items || []).map(i => `${i.name}: ${i.value}`)),
    badge: null,
    badgeColor: null,
  }
}

export function normalizeProductDetail(p) {
  const images = []
  if (p.main_image) images.push(p.main_image)
  if (p.images) {
    for (const img of (Array.isArray(p.images) ? p.images : [])) {
      if (img !== p.main_image) images.push(img)
    }
  }
  if (p.gallery) {
    for (const img of (Array.isArray(p.gallery) ? p.gallery : [])) {
      if (!images.includes(img)) images.push(img)
    }
  }
  return {
    ...normalizeProduct(p),
    images,
    categoryName: p.categories?.[0]?.category?.name || 'Uncategorized',
    sections: Array.isArray(p.sections) ? p.sections : [],
    variants: Array.isArray(p.variants) ? p.variants : [],
  }
}
