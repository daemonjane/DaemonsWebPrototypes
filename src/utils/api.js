const BASE = ''

async function request(method, path, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
    credentials: 'same-origin',
  }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${BASE}${path}`, opts)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`)
  return data
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
    checkout: (data) => request('POST', '/api/orders/checkout/', data),
  },
  search: (query, category = '') => {
    const params = new URLSearchParams()
    if (query) params.set('q', query)
    if (category) params.set('category', category)
    return request('GET', `/api/products/search/?${params}`)
  },
}
