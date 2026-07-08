export async function createPaymentIntent(api, amount) {
  const result = await api.payments.createIntent(amount)
  if (result.mode === 'demo' || !result.client_secret) {
    return `demo_pi_${Date.now()}`
  }
  if (!result.client_secret) {
    throw new Error('Failed to create payment')
  }
  return result.client_secret
}

export async function confirmCardPayment(clientSecret, cardElement, billingDetails) {
  const { loadStripe } = await import('@stripe/stripe-js')
  const pubKey = await getPubKey()
  const stripe = await loadStripe(pubKey)
  if (!stripe) throw new Error('Failed to load Stripe')
  const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
    payment_method: { card: cardElement, billing_details: billingDetails },
  })
  if (error) throw new Error(error.message)
  return paymentIntent.id
}

let cachedPubKey = ''

async function getPubKey() {
  if (cachedPubKey) return cachedPubKey
  const { api } = await import('./api')
  const cfg = await api.payments.config()
  cachedPubKey = cfg.publishable_key || ''
  return cachedPubKey
}
