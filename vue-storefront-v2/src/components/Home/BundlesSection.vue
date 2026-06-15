<script setup>
import { useCart } from '../../composables/useCart'
const { addItem } = useCart()

const bundles = [
  { id: 'bundle-silent', name: 'Silent Operator Bundle', description: 'Vanguard Desktop + Cyber‑Pro Keyboard + Desk Mat', price: 2596, saved: 152, oldPrice: 2748 },
  { id: 'bundle-immersive', name: 'Immersive Vision Bundle', description: '34" QD‑OLED Monitor + VESA Arm + Bias Lighting Kit', price: 1299, saved: 93, oldPrice: 1392 }
]

function addBundleToCart(bundle) {
  addItem({ id: bundle.id, name: bundle.name, price: bundle.price })
}
</script>

<template>
  <section id="bundles" class="space-y-10 sm:space-y-12">
    ... (the two bundle cards using @click="addBundleToCart(bundles[0])" etc.)
  </section>
</template>