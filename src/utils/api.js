const BASE = ''

function getCSRFToken() {
  const name = 'csrftoken'
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
  return match ? decodeURIComponent(match[2]) : ''
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const unsafe = ['POST', 'PUT', 'PATCH', 'DELETE']
  if (unsafe.includes(method)) {
    const token = getCSRFToken()
    if (token) headers['X-CSRFToken'] = token
  }
  const opts = {
    method,
    headers,
    credentials: 'same-origin',
  }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${BASE}${path}`, opts)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`)
  return data
}

export async function ensureCSRF() {
  if (!getCSRFToken()) {
    await fetch(`${BASE}/api/auth/csrf/`, { credentials: 'same-origin' })
  }
}

export const api = {
  register: (username, email, password) => request('POST', '/api/auth/register/', { username, email, password }),
  login: (username, password) => request('POST', '/api/auth/login/', { username, password }),
  logout: () => request('POST', '/api/auth/logout/'),
  profile: {
    get: () => request('GET', '/api/auth/profile/'),
    update: (data) => request('PATCH', '/api/auth/profile/', data),
  },
  cart: {
    get: () => request('GET', '/api/cart/'),
    add: (data) => request('POST', '/api/cart/add/', data),
    updateItem: (itemId, data) => request('PATCH', `/api/cart/item/${itemId}/`, data),
    removeItem: (itemId) => request('DELETE', `/api/cart/item/${itemId}/`),
    clear: () => request('POST', '/api/cart/clear/'),
    merge: (items) => request('POST', '/api/cart/merge/', { items }),
  },
  wishlist: {
    get: () => request('GET', '/api/wishlist/'),
    toggle: (slug) => request('POST', '/api/wishlist/toggle/', { slug }),
    check: (slug) => request('GET', `/api/wishlist/check/${slug}/`),
  },
  orders: {
    list: () => request('GET', '/api/orders/'),
    detail: (id) => request('GET', `/api/orders/${id}/`),
    tracking: (id) => request('GET', `/api/orders/${id}/tracking/`),
    checkout: (data) => request('POST', '/api/orders/checkout/', data),
  },
  addons: {
    list: (slug) => request('GET', `/api/products/${slug}/addons/`),
  },
  osimart: {
    banners: () => request('GET', '/api/osimart/banners/'),
    products: (params = {}) => {
      const qs = new URLSearchParams(params).toString()
      return request('GET', `/api/osimart/products/${qs ? '?' + qs : ''}`)
    },
    productDetail: (id) => request('GET', `/api/osimart/products/${id}/`),
    categories: () => request('GET', '/api/osimart/categories/'),
    store: () => request('GET', '/api/osimart/store/'),
    home: () => request('GET', '/api/osimart/home/'),
  },
  search: (query, category = '') => {
    const params = new URLSearchParams()
    if (query) params.set('q', query)
    if (category) params.set('category', category)
    return request('GET', `/api/products/search/?${params}`)
  },
}
