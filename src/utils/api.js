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
}
