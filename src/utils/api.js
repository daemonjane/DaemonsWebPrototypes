function getAuthToken() {
  return localStorage.getItem('gg-token')
}

async function request(method, path, body) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getAuthToken()
  if (token) headers['Authorization'] = `Bearer ${token}`
  const opts = { method, headers }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${path}`, opts)
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || data.error || `Request failed (${res.status})`)
  return data
}

export const api = {
  osimartCart: {
    view: () => request('GET', '/api/osimart/cart/view/'),
    updateItem: (data) => request('POST', '/api/osimart/cart/update-item/', data),
  },
  wishlist: {
    get: () => request('GET', '/api/wishlist/'),
    toggle: (slug) => request('POST', '/api/wishlist/toggle/', { slug }),
    check: (slug) => request('GET', `/api/wishlist/check/${slug}/`),
  },
  newsletter: {
    subscribe: (email) => request('POST', '/api/newsletter/subscribe/', { email }),
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
    createBanner: (data) => request('POST', '/api/osimart/banners/', data),
    banner: (id) => request('GET', `/api/osimart/banners/${id}/`),
    updateBanner: (id, data) => request('PUT', `/api/osimart/banners/${id}/`, data),
    deleteBanner: (id) => request('DELETE', `/api/osimart/banners/${id}/`),
    products: (params = {}) => {
      const qs = new URLSearchParams(params).toString()
      return request('GET', `/api/osimart/products/${qs ? '?' + qs : ''}`)
    },
    productDetail: (id) => request('GET', `/api/osimart/products/${id}/`),
    createProduct: (data) => request('POST', '/api/osimart/products/', data),
    updateProduct: (id, data) => request('PUT', `/api/osimart/products/${id}/`, data),
    deleteProduct: (id) => request('DELETE', `/api/osimart/products/${id}/`),
    categories: () => request('GET', '/api/osimart/categories/'),
    createCategory: (data) => request('POST', '/api/osimart/categories/', data),
    category: (id) => request('GET', `/api/osimart/categories/${id}/`),
    updateCategory: (id, data) => request('PUT', `/api/osimart/categories/${id}/`, data),
    deleteCategory: (id) => request('DELETE', `/api/osimart/categories/${id}/`),
    store: () => request('GET', '/api/osimart/store/'),
    updateStore: (data) => request('PUT', '/api/osimart/store/', data),
    home: () => request('GET', '/api/osimart/home/'),
    brands: () => request('GET', '/api/osimart/brands/'),
    createBrand: (data) => request('POST', '/api/osimart/brands/', data),
    brand: (id) => request('GET', `/api/osimart/brands/${id}/`),
    updateBrand: (id, data) => request('PUT', `/api/osimart/brands/${id}/`, data),
    deleteBrand: (id) => request('DELETE', `/api/osimart/brands/${id}/`),
    collections: () => request('GET', '/api/osimart/collections/'),
    createCollection: (data) => request('POST', '/api/osimart/collections/', data),
    collection: (id) => request('GET', `/api/osimart/collections/${id}/`),
    updateCollection: (id, data) => request('PUT', `/api/osimart/collections/${id}/`, data),
    deleteCollection: (id) => request('DELETE', `/api/osimart/collections/${id}/`),
    quantityUnits: () => request('GET', '/api/osimart/quantity-units/'),
    variantTypes: () => request('GET', '/api/osimart/variant-types/'),
    createVariantType: (data) => request('POST', '/api/osimart/variant-types/', data),
    variantType: (id) => request('GET', `/api/osimart/variant-types/${id}/`),
    updateVariantType: (id, data) => request('PUT', `/api/osimart/variant-types/${id}/`, data),
    deleteVariantType: (id) => request('DELETE', `/api/osimart/variant-types/${id}/`),
    announcementBars: () => request('GET', '/api/osimart/announcement-bars/'),
    createAnnouncementBar: (data) => request('POST', '/api/osimart/announcement-bars/', data),
    announcementBar: (id) => request('GET', `/api/osimart/announcement-bars/${id}/`),
    updateAnnouncementBar: (id, data) => request('PUT', `/api/osimart/announcement-bars/${id}/`, data),
    deleteAnnouncementBar: (id) => request('DELETE', `/api/osimart/announcement-bars/${id}/`),
    customers: (page) => request('GET', page ? `/api/osimart/customers/?page=${page}` : '/api/osimart/customers/'),
    createCustomer: (data) => request('POST', '/api/osimart/customers/', data),
    updateCustomer: (id, data) => request('PUT', `/api/osimart/customers/${id}/`, data),
    deleteCustomer: (id) => request('DELETE', `/api/osimart/customers/${id}/`),
    medias: () => request('GET', '/api/osimart/medias/'),
    createMedia: (data) => request('POST', '/api/osimart/medias/', data),
    deleteMedia: (id) => request('DELETE', `/api/osimart/medias/${id}/`),
    shippingZones: () => request('GET', '/api/osimart/shipping-zones/'),
    createShippingZone: (data) => request('POST', '/api/osimart/shipping-zones/', data),
    updateShippingZone: (id, data) => request('PUT', `/api/osimart/shipping-zones/${id}/`, data),
    deleteShippingZone: (id) => request('DELETE', `/api/osimart/shipping-zones/${id}/`),
    orderStatusChoices: () => request('GET', '/api/osimart/order-status-choices/'),
    createOrderStatusChoice: (data) => request('POST', '/api/osimart/order-status-choices/', data),
    updateOrderStatusChoice: (id, data) => request('PUT', `/api/osimart/order-status-choices/${id}/`, data),
    deleteOrderStatusChoice: (id) => request('DELETE', `/api/osimart/order-status-choices/${id}/`),
    orders: () => request('GET', '/api/admin/orders/'),
    updateOrderStatus: (id, status) => request('PATCH', `/api/admin/orders/${id}/status/`, { status }),
    updateProfile: (data) => request('PUT', '/api/osimart/customers/profile/', data),
  },
  search: (query, category = '') => {
    const params = { search: query, limit: 50 }
    if (category) params.category = category
    return request('GET', `/api/osimart/products/?${new URLSearchParams(params)}`)
  },
  payments: {
    config: () => request('GET', '/api/payments/config/'),
    createIntent: (amount) => request('POST', '/api/payments/create-intent/', { amount }),
    confirm: (paymentIntentId) => request('POST', '/api/payments/confirm/', { payment_intent_id: paymentIntentId }),
  },
  backInStock: {
    subscribe: (data) => request('POST', '/api/back-in-stock/', data),
  },
}
