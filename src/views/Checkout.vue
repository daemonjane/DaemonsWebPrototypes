<script setup>
import { ref, reactive, computed } from 'vue'
import { useCart } from '../composables/useCart'
import { useRouter } from 'vue-router'
import { validateForm } from '../utils/validation'
import EmptyState from '../components/EmptyState.vue'
import StepperIndicator from '../components/StepperIndicator.vue'
import { useToast } from '../composables/useToast'
import FreeShippingBar from '../components/FreeShippingBar.vue'

const { cart, totalPrice, clearCart } = useCart()
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

const discountAmount = computed(() => totalPrice.value * (giftCardDiscount.value / 100))
const finalTotal = computed(() => totalPrice.value - discountAmount.value)

const placing = ref(false)

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
  addToast('Gift card applied! 10% discount.', 'success')
}

function nextStep() {
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
  }
  currentStep.value++
}

function prevStep() {
  currentStep.value--
}

async function placeOrder() {
  placing.value = true
  try
  {
    const { api } = await import('../utils/api')
    const result = await api.orders.checkout({
      name: form.name,
      email: form.email,
      address: form.address,
      gift_card_code: giftCardApplied.value ? giftCardCode.value : '',
      gift_card_discount: giftCardApplied.value ? giftCardDiscount.value : null,
    })
    await clearCart()
    addToast('Order placed successfully!', 'success')
    router.push(`/confirmation?id=${result.id}`)
  } catch (e) {
    addToast(e.message || 'Failed to place order', 'error')
  } finally {
    placing.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Checkout</h1>
    <EmptyState v-if="!cart.length" icon="cart" title="Your cart is empty" message="Add some products before checking out." action-label="Browse Shop" action-to="/shop" />

    <template v-else>
      <FreeShippingBar class="mb-4" />
      <StepperIndicator :steps="steps" :current="currentStep" />
      <div class="grid md:grid-cols-2 gap-8">

        <!-- Left: Order Summary -->
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800 h-fit">
          <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
          <ul class="space-y-2">
            <li v-for="item in cart" :key="item.id" class="flex justify-between">
              <span>{{ item.name }} (x{{ item.quantity }})</span>
              <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
            </li>
          </ul>

          <div class="border-t border-slate-700 mt-4 pt-4 space-y-2 text-sm">
            <div class="flex justify-between text-slate-400">
              <span>Subtotal</span>
              <span>${{ cartSubtotal.toFixed(2) }}</span>
            </div>
            <div v-if="upgradesTotal > 0" class="flex justify-between text-slate-400">
              <span>Upgrades</span>
              <span>${{ upgradesTotal.toFixed(2) }}</span>
            </div>
            <div v-if="membershipTotal > 0" class="flex justify-between text-slate-400">
              <span>Membership</span>
              <span>${{ membershipTotal.toFixed(2) }}</span>
            </div>
            <div v-if="giftCardApplied" class="flex justify-between text-emerald-400">
              <span>Gift Card (10% off)</span>
              <span>-${{ discountAmount.toFixed(2) }}</span>
            </div>
          </div>

          <div class="border-t border-slate-700 mt-4 pt-4 text-right">
            <span class="text-lg">Total: </span>
            <span class="text-2xl font-bold text-cyan-400" aria-live="polite">${{ finalTotal.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Right: Step form -->
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <!-- Step 1: Shipping -->
          <div v-if="currentStep === 0">
            <h2 class="text-xl font-semibold mb-4">Shipping Info</h2>
            <form @submit.prevent="nextStep" novalidate>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.name" type="text" placeholder=" " id="ship-name"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.name }"
                    :aria-describedby="errors.name ? 'name-error' : undefined" aria-required="true">
                  <label for="ship-name" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">Full Name</label>
                </div>
                <p v-if="errors.name" id="name-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.name }}</p>
              </div>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.email" type="email" placeholder=" " id="ship-email"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.email }"
                    :aria-describedby="errors.email ? 'email-error' : undefined" aria-required="true">
                  <label for="ship-email" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">Email</label>
                </div>
                <p v-if="errors.email" id="email-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.email }}</p>
              </div>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.address" type="text" placeholder=" " id="ship-addr"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.address }"
                    :aria-describedby="errors.address ? 'address-error' : undefined" aria-required="true">
                  <label for="ship-addr" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">Address</label>
                </div>
                <p v-if="errors.address" id="address-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.address }}</p>
              </div>
              <button type="submit" class="mt-4 w-full bg-cyan-600 py-3 rounded-md font-bold hover:bg-cyan-500 transition active:scale-95">
                Continue to Payment
              </button>
            </form>
          </div>

          <!-- Step 2: Payment -->
          <div v-if="currentStep === 1">
            <h2 class="text-xl font-semibold mb-4">Payment</h2>
            <form @submit.prevent="nextStep" novalidate>
              <div class="mb-3">
                <div class="relative">
                  <input v-model="form.cardNumber" type="text" placeholder=" " id="pay-card"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.cardNumber }"
                    :aria-describedby="errors.cardNumber ? 'card-error' : undefined" aria-required="true">
                  <label for="pay-card" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">Card Number</label>
                </div>
                <p v-if="errors.cardNumber" id="card-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.cardNumber }}</p>
              </div>
              <div class="grid grid-cols-2 gap-3 mb-3">
                <div class="relative">
                  <input v-model="form.expDate" type="text" placeholder=" " id="pay-exp"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.expDate }" aria-required="true"
                    :aria-describedby="errors.expDate ? 'exp-error' : undefined">
                  <label for="pay-exp" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">MM/YY</label>
                </div>
                <div class="relative">
                  <input v-model="form.cvv" type="text" placeholder=" " id="pay-cvv"
                    class="peer w-full bg-slate-800 border border-slate-700 rounded p-2 pt-5 text-sm placeholder-transparent focus:outline-none focus:border-cyan-500 transition-colors"
                    :class="{ 'border-pink-500': errors.cvv }" aria-required="true"
                    :aria-describedby="errors.cvv ? 'cvv-error' : undefined">
                  <label for="pay-cvv" class="absolute left-2 top-1 text-[10px] text-slate-500 peer-placeholder-shown:top-3.5 peer-placeholder-shown:text-xs peer-placeholder-shown:text-slate-500 peer-focus:top-1 peer-focus:text-[10px] peer-focus:text-cyan-400 transition-all duration-200 pointer-events-none">CVV</label>
                </div>
                <p v-if="errors.expDate" id="exp-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.expDate }}</p>
                <p v-if="errors.cvv" id="cvv-error" class="text-pink-400 text-xs mt-1" role="alert">{{ errors.cvv }}</p>
              </div>

              <!-- Gift Card Checker -->
              <div class="mt-6 pt-4 border-t border-slate-700">
                <h3 class="text-sm font-semibold text-slate-300 mb-2">Gift Card</h3>
                <div class="flex gap-2">
                  <input v-model="giftCardCode" type="text" placeholder="Enter code"
                    class="flex-1 bg-slate-800 border border-slate-700 rounded p-2 text-sm"
                    :disabled="giftCardApplied" aria-label="Gift card code">
                  <button v-if="!giftCardApplied" @click.prevent="applyGiftCard"
                    class="bg-emerald-700 hover:bg-emerald-600 text-white text-sm px-4 rounded-md transition active:scale-95">
                    Apply
                  </button>
                  <span v-else class="text-emerald-400 text-sm flex items-center">Applied ✓</span>
                </div>
                <p v-if="giftCardError" class="text-pink-400 text-xs mt-1">{{ giftCardError }}</p>
              </div>

              <div class="flex gap-3 mt-6">
                <button type="button" @click="prevStep"
                  class="flex-1 border border-slate-700 py-3 rounded-md font-semibold hover:bg-slate-800 transition">
                  Back
                </button>
                <button type="submit"
                  class="flex-1 bg-cyan-600 py-3 rounded-md font-bold hover:bg-cyan-500 transition active:scale-95">
                  Review Order
                </button>
              </div>
            </form>
          </div>

          <!-- Step 3: Review -->
          <div v-if="currentStep === 2">
            <h2 class="text-xl font-semibold mb-4">Review & Confirm</h2>
            <div class="space-y-4 text-sm">
              <div class="bg-slate-800 rounded-lg p-3">
                <p class="text-slate-500 text-xs uppercase tracking-wider mb-1">Shipping</p>
                <p class="text-white font-medium">{{ form.name }}</p>
                <p class="text-slate-400">{{ form.email }}</p>
                <p class="text-slate-400">{{ form.address }}</p>
              </div>
              <div class="bg-slate-800 rounded-lg p-3">
                <p class="text-slate-500 text-xs uppercase tracking-wider mb-1">Payment</p>
                <p class="text-slate-400 font-mono">**** **** **** {{ form.cardNumber.slice(-4) }}</p>
              </div>
              <div class="bg-slate-800 rounded-lg p-3">
                <p class="text-slate-500 text-xs uppercase tracking-wider mb-1">Items</p>
                <ul class="space-y-1">
                  <li v-for="item in cart" :key="item.id" class="flex justify-between text-slate-300">
                    <span>{{ item.name }} x{{ item.quantity }}</span>
                    <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
                  </li>
                </ul>
                <div v-if="giftCardApplied" class="border-t border-slate-700 mt-2 pt-2 text-emerald-400 flex justify-between">
                  <span>Gift Card Discount</span>
                  <span>-{{ giftCardDiscount }}%</span>
                </div>
              </div>
            </div>
            <!-- Gift Card on review step -->
            <div class="mt-4 border-t border-slate-700 pt-4">
              <h3 class="text-sm font-semibold text-slate-300 mb-2">Gift Card</h3>
              <div class="flex gap-2">
                <input v-model="giftCardCode" type="text" placeholder="Enter code"
                  class="flex-1 bg-slate-800 border border-slate-700 rounded p-2 text-sm"
                  :disabled="giftCardApplied" aria-label="Gift card code">
                <button v-if="!giftCardApplied" @click.prevent="applyGiftCard"
                  class="bg-emerald-700 hover:bg-emerald-600 text-white text-sm px-4 rounded-md transition active:scale-95">
                  Apply
                </button>
              </div>
              <p v-if="giftCardError" class="text-pink-400 text-xs mt-1">{{ giftCardError }}</p>
              <p v-if="giftCardApplied" class="text-emerald-400 text-xs mt-1">10% discount applied!</p>
              <p v-if="!giftCardApplied && !giftCardError" class="text-slate-500 text-xs mt-1">Try code: SAVE10</p>
            </div>
            <div class="flex gap-3 mt-6">
              <button @click="prevStep"
                class="flex-1 border border-slate-700 py-3 rounded-md font-semibold hover:bg-slate-800 transition">
                Back
              </button>
              <button @click="placeOrder" :disabled="placing"
                class="flex-1 bg-emerald-700 hover:bg-emerald-600 py-3 rounded-md font-bold transition active:scale-95 disabled:opacity-50">
                {{ placing ? 'Placing Order...' : `Place Order — $${finalTotal.toFixed(2)}` }}
              </button>
            </div>
          </div>

        </div>
      </div>
    </template>
  </div>
</template>
