const STORE_ID = '17781c3f-b746-4897-be7d-15d1ff48589e'
const BASE_URL = 'https://api.osimart.com'

function getDeviceId() {
  let deviceId = localStorage.getItem('gg-device-id')
  if (!deviceId) {
    deviceId = crypto.randomUUID()
    localStorage.setItem('gg-device-id', deviceId)
  }
  return deviceId
}

export async function login({ email, password }) {
  const url = `${BASE_URL}/auth/login/?store=${STORE_ID}`

  const payload = {
    email,
    password,
    store_id: STORE_ID,
    device_name: navigator.userAgent || 'web-client',
    device_id: getDeviceId(),
    login_as: 'customer'
  }

  console.log('[osimart] login request ->', url, payload)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  } catch (networkErr) {
    console.error('[osimart] login network error:', networkErr)
    throw new Error('Could not reach the server. Check your connection and try again.')
  }

  let data = null
  try {
    data = await res.json()
  } catch {
    console.warn('[osimart] login response had no JSON body')
  }

  console.log('[osimart] login response <-', res.status, data)

  if (!res.ok) {
    const message =
      data?.non_field_errors?.[0] ||
      data?.verified?.[0] ||
      data?.detail ||
      data?.message ||
      data?.email?.[0] ||
      data?.password?.[0] ||
      (data ? JSON.stringify(data) : `Login failed (${res.status})`)
    console.error('[osimart] login failed:', res.status, message, data)
    throw new Error(message)
  }

  return data
}

export async function signup({ name, email, password, phone }) {
  const url = `${BASE_URL}/auth/register/?store=${STORE_ID}`

  const trimmedName = (name || '').trim()
  const nameParts = trimmedName.split(/\s+/).filter(Boolean)
  const first_name = nameParts[0] || ''
  const last_name = nameParts.slice(1).join(' ') || ''

  const payload = {
    name: trimmedName,
    first_name,
    last_name,
    email,
    password,
    mobile: phone || '',
    store_id: STORE_ID,
    device_name: navigator.userAgent || 'web-client',
    device_id: getDeviceId(),
    register_as: 'customer'
  }

  console.log('[osimart] signup request ->', url, payload)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  } catch (networkErr) {
    console.error('[osimart] signup network error:', networkErr)
    throw new Error('Could not reach the server. Check your connection and try again.')
  }

  let data = null
  try {
    data = await res.json()
  } catch {
    console.warn('[osimart] signup response had no JSON body')
  }

  console.log('[osimart] signup response <-', res.status, data)

  if (!res.ok) {
    const message =
      data?.detail ||
      data?.message ||
      data?.non_field_errors?.[0] ||
      (data ? JSON.stringify(data) : `Signup failed (${res.status})`)
    console.error('[osimart] signup failed:', res.status, message, data)
    throw new Error(message)
  }

  return data
}

export async function verifyEmail({ email, code }) {
  const url = `${BASE_URL}/auth/verify/?store=${STORE_ID}`

  const payload = {
    email,
    code,
    store_id: STORE_ID,
    verify_as: 'customer'
  }

  console.log('[osimart] verification request ->', url, payload)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  } catch (networkErr) {
    console.error('[osimart] verification network error:', networkErr)
    throw new Error('Could not reach the server. Check your connection.')
  }

  let data = null
  try {
    data = await res.json()
  } catch {}

  console.log('[osimart] verification response <-', res.status, JSON.stringify(data))

  if (!res.ok) {
    const message = data?.detail || data?.message || data?.code?.[0] || 'Verification failed.'
    throw new Error(message)
  }

  return data
}

export async function resendVerificationCode({ email }) {
  const url = `${BASE_URL}/auth/regen/?store=${STORE_ID}`

  const payload = {
    email,
    store_id: STORE_ID,
    verify_as: 'customer'
  }

  console.log('[osimart] resend code request ->', url, payload)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
  } catch (networkErr) {
    console.error('[osimart] resend code network error:', networkErr)
    throw new Error('Could not reach the server. Check your connection.')
  }

  let data = null
  try {
    data = await res.json()
  } catch {}

  console.log('[osimart] resend code response <-', res.status, JSON.stringify(data))

  if (!res.ok) {
    const message = data?.detail || data?.message || data?.email?.[0] || 'Could not resend code.'
    throw new Error(message)
  }

  return data
}

export function saveAuthSession(data) {
  const accessToken = data?.access_token || data?.token || data?.access
  const refreshToken = data?.refresh_token || data?.refresh

  if (accessToken) localStorage.setItem('gg-token', accessToken)
  if (refreshToken) localStorage.setItem('gg-refresh', refreshToken)

  const userObj =
    data?.user ||
    (data?.user_id
      ? { id: data.user_id, session_id: data.session_id }
      : (data?.id ? data : null))

  if (userObj) localStorage.setItem('gg-user', JSON.stringify(userObj))

  console.log('[osimart] auth session saved:', {
    token: getAuthToken(),
    user: userObj
  })
}

export function getAuthToken() {
  return localStorage.getItem('gg-token')
}

export function getRefreshToken() {
  return localStorage.getItem('gg-refresh')
}

export function logoutAuth() {
  localStorage.removeItem('gg-token')
  localStorage.removeItem('gg-refresh')
  localStorage.removeItem('gg-user')
}

export async function refreshToken() {
  const refresh = getRefreshToken()
  if (!refresh) throw new Error('No refresh token available')

  const url = `${BASE_URL}/auth/refresh/?store=${STORE_ID}`
  const payload = { refresh, store_id: STORE_ID }

  console.log('[osimart] refresh token request ->', url)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (networkErr) {
    console.error('[osimart] refresh network error:', networkErr)
    throw new Error('Could not reach the server.')
  }

  let data = null
  try { data = await res.json() } catch {}

  console.log('[osimart] refresh response <-', res.status, data)

  if (!res.ok) {
    const msg = data?.detail || data?.message || 'Token refresh failed'
    throw new Error(msg)
  }

  saveAuthSession(data)
  return data
}

export async function changePassword({ old_password, new_password }) {
  const token = getAuthToken()
  const url = `${BASE_URL}/auth/change-password/?store=${STORE_ID}`
  const payload = { old_password, new_password, store_id: STORE_ID }

  console.log('[osimart] change password request ->', url)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    })
  } catch (networkErr) {
    console.error('[osimart] change password network error:', networkErr)
    throw new Error('Could not reach the server.')
  }

  let data = null
  try { data = await res.json() } catch {}

  console.log('[osimart] change password response <-', res.status, data)

  if (!res.ok) {
    const msg = data?.detail || data?.message || data?.old_password?.[0] || 'Change password failed'
    throw new Error(msg)
  }

  return data
}

export async function resetPassword({ email, code, new_password }) {
  const url = `${BASE_URL}/auth/reset_password/?store=${STORE_ID}`
  const payload = {
    email,
    code,
    new_password: new_password,
    store_id: STORE_ID,
    reset_as: 'customer',
  }

  console.log('[osimart] reset password request ->', url)

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (networkErr) {
    console.error('[osimart] reset password network error:', networkErr)
    throw new Error('Could not reach the server.')
  }

  let data = null
  try { data = await res.json() } catch {}

  console.log('[osimart] reset password response <-', res.status, data)

  if (!res.ok) {
    const msg = data?.detail || data?.message || data?.email?.[0] || 'Reset password failed'
    throw new Error(msg)
  }

  return data
}

export async function sendPasswordResetCode({ email }) {
  const url = `${BASE_URL}/auth/regen/?store=${STORE_ID}`
  const payload = { email, store_id: STORE_ID, verify_as: 'customer' }

  let res
  try {
    res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (networkErr) {
    throw new Error('Could not reach the server.')
  }

  let data = null
  try { data = await res.json() } catch {}

  if (!res.ok) {
    const msg = data?.detail || data?.message || data?.email?.[0] || 'Failed to send code'
    throw new Error(msg)
  }

  return data
}
