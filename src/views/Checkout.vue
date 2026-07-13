<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useOsimartCart } from '../composables/useOsimartCart'
import { useRouter } from 'vue-router'
import { validateForm } from '../utils/validation'
import EmptyState from '../components/EmptyState.vue'
import StepperIndicator from '../components/StepperIndicator.vue'
import { useToast } from '../composables/useToast'
import FreeShippingBar from '../components/FreeShippingBar.vue'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const { cart, totalPrice, clearCart } = useOsimartCart()
const router = useRouter()
const { addToast } = useToast()

const steps = ['Shipping', 'Payment', 'Review']
const currentStep = ref(0)

const form = reactive({
  name: '',
  email: '',
  address: '',
  cardNumber: '',
  expDate: '',
  cvv: '',
})
const errors = reactive({})

const giftCardCode = ref('')
const giftCardDiscount = ref(0)
const giftCardApplied = ref(false)
const giftCardError = ref('')

const pubKey = ref('')
const paymentMode = ref('demo')
const stripeLoaded = ref(false)
const cardElement = ref(null)

const cartSubtotal = computed(() =>
  cart.value
    .filter(item => item.type !== 'upgrade' && item.type !== 'membership')
    .reduce((sum, item) => sum + item.price * item.quantity, 0)
)
const upgradesTotal = computed(() =>
  cart.value.filter(item => item.type === 'upgrade').reduce((sum, item) => sum + item.price, 0)
)
const membershipTotal = computed(() =>
  cart.value.filter(item => item.type === 'membership').reduce((sum, item) => sum + item.price, 0)
)

const discountAmount = computed(() => (totalPrice?.value ?? 0) * (giftCardDiscount.value / 100))
const finalTotal = computed(() => (totalPrice?.value ?? 0) - discountAmount.value)

const placing = ref(false)

let api = null
try {
  const mod = await import('../utils/api')
  api = mod.api
} catch {
  // api stays null, demo mode will be used
}

onMounted(async () => {
  if (!api) { paymentMode.value = 'demo'; return }
  try {
    const cfg = await api.payments.config()
    pubKey.value = cfg.publishable_key || ''
    paymentMode.value = cfg.mode || 'demo'
    if (pubKey.value) {
      try {
        const stripe = await import('@stripe/stripe-js')
        const stripeInstance = await stripe.loadStripe(pubKey.value)
        if (stripeInstance) {
          stripeLoaded.value = true
        }
      } catch { /* stripe not available */ }
    }
  } catch {
    paymentMode.value = 'demo'
  }
})

function applyGiftCard() {
  giftCardError.value = ''
  if (!giftCardCode.value.trim()) {
    giftCardError.value = 'Enter a code'
    return
  }
  if (giftCardCode.value.trim().length < 6) {
    giftCardError.value = 'Invalid code'
    return
  }
  giftCardDiscount.value = 10
  giftCardApplied.value = true
  addToast('Gift card applied! 10% discount.', 3000, 'success')
}

function isValidCardNumber(n) {
  const digits = n.replace(/\D/g, '')
  if (digits.length < 13 || digits.length > 19) return false
  let sum = 0
  let alt = false
  for (let i = digits.length - 1; i >= 0; i--) {
    let d = parseInt(digits[i], 10)
    if (alt) { d *= 2; if (d > 9) d -= 9 }
    sum += d; alt = !alt
  }
  return sum % 10 === 0
}

async function nextStep() {
  Object.keys(errors).forEach(key => delete errors[key])
  if (currentStep.value === 0) {
    const validationErrors = validateForm(form, {
      name: ['required'],
      email: ['required', 'email'],
      address: ['required'],
    })
    if (Object.keys(validationErrors).length > 0) {
      Object.assign(errors, validationErrors)
      return
    }
  }
  if (currentStep.value === 1) {
    const validationErrors = validateForm(form, {
      cardNumber: ['required'],
      expDate: ['required'],
      cvv: ['required'],
    })
    if (Object.keys(validationErrors).length > 0) {
      Object.assign(errors, validationErrors)
      return
    }
    if (!isValidCardNumber(form.cardNumber)) {
      errors.cardNumber = 'Invalid card number'
      return
    }
  }
  currentStep.value++
}

function prevStep() {
  currentStep.value--
}

async function placeOrder() {
  placing.value = true
  try {
    if (api) {
      let paymentIntentId = ''
      if (paymentMode.value === 'live' && stripeLoaded.value) {
        const { createPaymentIntent, confirmCardPayment } = await import('../utils/payment')
        const clientSecret = await createPaymentIntent(api, finalTotal.value)
        paymentIntentId = await confirmCardPayment(clientSecret, cardElement.value, {
          name: form.name,
          email: form.email,
        })
      } else {
        paymentIntentId = `demo_pi_${Date.now()}`
      }

      const result = await api.orders.checkout({
        name: form.name,
        email: form.email,
        address: form.address,
        gift_card_code: giftCardApplied.value ? giftCardCode.value : '',
        gift_card_discount: giftCardApplied.value ? giftCardDiscount.value : null,
        payment_intent_id: paymentIntentId,
        items: cart.value.map(i => ({
          name: i.name,
          price: i.price,
          quantity: i.quantity,
          item_type: i.type || 'product',
        })),
      })
      await clearCart()
      addToast('Order placed successfully!', 3000, 'success')
      const orderId = result?.id
      if (!orderId) throw new Error('No order ID returned')
      router.push(`/confirmation?id=${orderId}`)
    } else {
      const demoOrderId = `demo-${Date.now()}`
      const demoOrder = {
        id: demoOrderId,
        name: form.name,
        email: form.email,
        address: form.address,
        items: cart.value.map(i => ({
          name: i.name,
          price: i.price,
          quantity: i.quantity,
          item_type: i.type || 'product',
        })),
        total: finalTotal.value,
        payment_mode: 'demo',
        status: 'placed',
        created_at: new Date().toISOString(),
      }
      const orders = JSON.parse(localStorage.getItem('vertex_orders') || '[]')
      orders.push(demoOrder)
      localStorage.setItem('vertex_orders', JSON.stringify(orders))
      await clearCart()
      addToast('Order placed (demo mode)!', 3000, 'success')
      router.push(`/confirmation?id=${demoOrderId}`)
    }
  } catch (e) {
    addToast(e.message || 'Failed to place order', 3000, 'error')
  } finally {
    placing.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <Breadcrumbs :crumbs="[{ label: 'Checkout' }]" />
    <h1 class="text-3xl font-display font-bold text-surface-50 mb-6">Checkout</h1>
    <EmptyState v-if="!cart.length" icon="cart" title="Your cart is empty" message="Add some products before checking out." action-label="Browse Shop" action-to="/shop" />

    <template v-else>
      <FreeShippingBar class="mb-4" />
      <StepperIndicator :steps="steps" :current="currentStep" />
      <div class="grid md:grid-cols-2 gap-8">

        <!-- Left: Order Summary -->
        <div class="bg-surface-800/60 p-6 rounded-xl border border-surface-700 h-fit">
          <h2 class="text-xl font-display font-semibold mb-4">Order Summary</h2>
          <ul class="space-y-2">
            <li v-for="item in cart" :key="item.id" class="flex justify-between">
              <span>{{ item.name }} (x{{ item.quantity }})</span>
              <span>${{ (Number(item.price || 0) * (item.quantity || 0)).toFixed(2) }}</span>
            </li>
          </ul>

          <div class="border-t border-surface-600 mt-4 pt-4 space-y-2 text-sm">
            <div class="flex justify-between text-surface-400">
              <span>Subtotal</span>
              <span>${{ Number(cartSubtotal || 0).toFixed(2) }}</span>
            </div>
            <div v-if="upgradesTotal > 0" class="flex justify-between text-surface-400">
              <span>Upgrades</span>
              <span>${{ Number(upgradesTotal || 0).toFixed(2) }}</span>
            </div>
            <div v-if="membershipTotal > 0" class="flex justify-between text-surface-400">
              <span>Membership</span>
              <span>${{ Number(membershipTotal || 0).toFixed(2) }}</span>
            </div>
            <div v-if="giftCardApplied" class="flex justify-between text-success-400">
              <span>Gift Card (10% off)</span>
              <span>-${{ Number(discountAmount || 0).toFixed(2) }}</span>
            </div>
          </div>

          <div class="border-t border-surface-600 mt-4 pt-4 text-right">
            <span class="text-lg">Total: </span>
            <span class="text-2xl font-bold text-electric-500 price-glow" aria-live="polite">${{ Number(finalTotal || 0).toFixed(2) }}</span>
          </div>

          <div class="mt-4 pt-4 border-t border-surface-600 text-xs text-surface-500">
            <p v-if="paymentMode === 'demo'">
              Payment is simulated. No real charge will be made.
            </p>
            <p v-else-if="stripeLoaded">
              Secured by Stripe
            </p>
          </div>
        </div>

        <!-- Right: Step form -->
        <div class="bg-surface-800/60 p-6 rounded-xl border border-surface-700">
          <!-- Step 1: Shipping -->
          <div v-if="currentStep === 0">
            <h2 class="text-xl font-display font-semibold mb-4">Shipping Info</h2>
            <form @submit.prevent="nextStep" novalidate>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.name" type="text" placeholder=" " id="ship-name"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.name }"
                    :aria-describedby="errors.name ? 'name-error' : undefined" aria-required="true">
                  <label for="ship-name" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">Full Name</label>
                </div>
                <p v-if="errors.name" id="name-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.name }}</p>
              </div>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.email" type="email" placeholder=" " id="ship-email"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.email }"
                    :aria-describedby="errors.email ? 'email-error' : undefined" aria-required="true">
                  <label for="ship-email" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">Email</label>
                </div>
                <p v-if="errors.email" id="email-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
              </div>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.address" type="text" placeholder=" " id="ship-addr"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.address }"
                    :aria-describedby="errors.address ? 'address-error' : undefined" aria-required="true">
                  <label for="ship-addr" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">Address</label>
                </div>
                <p v-if="errors.address" id="address-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.address }}</p>
              </div>
              <button type="submit" class="mt-4 w-full bg-electric-500 py-3 rounded-md font-bold hover:bg-electric-400 transition active:scale-95">
                Continue to Payment
              </button>
            </form>
          </div>

          <!-- Step 2: Payment -->
          <div v-if="currentStep === 1">
            <h2 class="text-xl font-display font-semibold mb-4">Payment</h2>
            <form @submit.prevent="nextStep" novalidate>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.cardNumber" type="text" placeholder=" " id="pay-card"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.cardNumber }"
                    :aria-describedby="errors.cardNumber ? 'card-error' : undefined" aria-required="true">
                  <label for="pay-card" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">Card Number</label>
                </div>
                <p v-if="errors.cardNumber" id="card-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.cardNumber }}</p>
              </div>
              <div class="grid grid-cols-2 gap-3 mb-3">
                <div class="relative">
                  <input v-model="form.expDate" type="text" placeholder=" " id="pay-exp"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.expDate }" aria-required="true"
                    :aria-describedby="errors.expDate ? 'exp-error' : undefined">
                  <label for="pay-exp" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">MM/YY</label>
                </div>
                <div class="relative">
                  <input v-model="form.cvv" type="text" placeholder=" " id="pay-cvv"
                    class="peer w-full bg-surface-700 border border-surface-600 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-electric-500 transition-colors"
                    :class="{ 'border-danger-500': errors.cvv }" aria-required="true"
                    :aria-describedby="errors.cvv ? 'cvv-error' : undefined">
                  <label for="pay-cvv" class="absolute left-2 top-1 text-[10px] text-surface-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-surface-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-electric-500 transition-all duration-200 pointer-events-none">CVV</label>
                </div>
                <p v-if="errors.expDate" id="exp-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.expDate }}</p>
                <p v-if="errors.cvv" id="cvv-error" class="text-danger-400 text-xs mt-1" role="alert">{{ errors.cvv }}</p>
              </div>

              <div v-if="paymentMode === 'demo'" class="bg-surface-700/50 rounded p-3 mb-3 text-xs text-surface-400">
                Demo mode — enter any valid-looking card number (e.g. 4242 4242 4242 4242).
                No real charge will be made.
              </div>

              <!-- Gift Card Checker -->
              <div class="mt-6 pt-4 border-t border-surface-600">
                <h3 class="text-sm font-semibold text-surface-300 mb-2">Gift Card</h3>
                <div class="flex gap-2">
                  <input v-model="giftCardCode" type="text" placeholder="Enter code"
                    class="flex-1 bg-surface-700 border border-surface-600 rounded p-2 text-sm"
                    :disabled="giftCardApplied" aria-label="Gift card code">
                  <button v-if="!giftCardApplied" @click.prevent="applyGiftCard"
                    class="bg-success-600 hover:bg-success-500 text-surface-50 text-sm px-4 rounded-md transition active:scale-95">
                    Apply
                  </button>
                  <span v-else class="text-success-400 text-sm flex items-center">Applied ✓</span>
                </div>
                <p v-if="giftCardError" class="text-danger-400 text-xs mt-1">{{ giftCardError }}</p>
              </div>

              <div class="flex gap-3 mt-6">
                <button type="button" @click="prevStep"
                  class="flex-1 border border-surface-600 py-3 rounded-md font-semibold hover:bg-surface-700 transition">
                  Back
                </button>
                <button type="submit"
                  class="flex-1 bg-electric-500 py-3 rounded-md font-bold hover:bg-electric-400 transition active:scale-95">
                  Review Order
                </button>
              </div>
            </form>
          </div>

          <!-- Step 3: Review -->
          <div v-if="currentStep === 2">
            <h2 class="text-xl font-display font-semibold mb-4">Review & Confirm</h2>
            <div class="space-y-4 text-sm">
              <div class="bg-surface-700 rounded-lg p-3">
                <p class="text-surface-500 text-xs uppercase tracking-wider mb-1">Shipping</p>
                <p class="text-surface-50 font-medium">{{ form.name }}</p>
                <p class="text-surface-400">{{ form.email }}</p>
                <p class="text-surface-400">{{ form.address }}</p>
              </div>
              <div class="bg-surface-700 rounded-lg p-3">
                <p class="text-surface-500 text-xs uppercase tracking-wider mb-1">Payment</p>
                <p class="text-surface-400 font-mono">**** **** **** {{ form.cardNumber.slice(-4) }}</p>
                <p v-if="paymentMode === 'demo'" class="text-electric-500 text-xs mt-1">Demo payment — no charge</p>
              </div>
              <div class="bg-surface-700 rounded-lg p-3">
                <p class="text-surface-500 text-xs uppercase tracking-wider mb-1">Items</p>
                <ul class="space-y-1">
                  <li v-for="item in cart" :key="item.id" class="flex justify-between text-surface-300">
                    <span>{{ item.name }} x{{ item.quantity }}</span>
                    <span>${{ (Number(item.price || 0) * (item.quantity || 0)).toFixed(2) }}</span>
                  </li>
                </ul>
                <div v-if="giftCardApplied" class="border-t border-surface-600 mt-2 pt-2 text-success-400 flex justify-between">
                  <span>Gift Card Discount</span>
                  <span>-{{ giftCardDiscount }}%</span>
                </div>
              </div>
            </div>
            <!-- Gift Card on review step -->
            <div class="mt-4 border-t border-surface-600 pt-4">
              <h3 class="text-sm font-semibold text-surface-300 mb-2">Gift Card</h3>
              <div class="flex gap-2">
                <input v-model="giftCardCode" type="text" placeholder="Enter code"
                  class="flex-1 bg-surface-700 border border-surface-600 rounded p-2 text-sm"
                  :disabled="giftCardApplied" aria-label="Gift card code">
                <button v-if="!giftCardApplied" @click.prevent="applyGiftCard"
                  class="bg-success-600 hover:bg-success-500 text-surface-50 text-sm px-4 rounded-md transition active:scale-95">
                  Apply
                </button>
              </div>
              <p v-if="giftCardError" class="text-danger-400 text-xs mt-1">{{ giftCardError }}</p>
              <p v-if="giftCardApplied" class="text-success-400 text-xs mt-1">10% discount applied!</p>
              <p v-if="!giftCardApplied && !giftCardError" class="text-surface-500 text-xs mt-1">Try code: SAVE10</p>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="prevStep"
                class="flex-1 border border-surface-600 py-3 rounded-md font-semibold hover:bg-surface-700 transition">
                Back
              </button>
              <button @click="placeOrder" :disabled="placing"
                class="flex-1 bg-success-600 hover:bg-success-500 py-3 rounded-md font-bold transition active:scale-95 disabled:opacity-50">
                {{ placing ? 'Placing Order...' : `Place Order — $${finalTotal.toFixed(2)}` }}
              </button>
            </div>
          </div>

        </div>
      </div>
    </template>
  </div>
</template>
