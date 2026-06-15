<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { products } from '../data/products'
import { useCart } from '../composables/useCart'

const route = useRoute()
const productId = route.params.id
const product = computed(() => products.find(p => p.id === productId))

const { addItem } = useCart()
</script>

<template>
  <div v-if="product" class="max-w-7xl mx-auto px-4 py-12">
    <div class="grid md:grid-cols-2 gap-8">
      <img :src="product.image" :alt="product.name" class="w-full rounded-xl object-cover h-96" />
      <div>
        <h1 class="text-4xl font-bold text-white">{{ product.name }}</h1>
        <p class="text-2xl text-cyan-400 mt-4">${{ product.price.toFixed(2) }}</p>
        <p class="text-slate-400 mt-4">{{ product.description }}</p>
        <div class="mt-4">
          <h3 class="text-white font-semibold mb-2">Technical Specs</h3>
          <ul class="list-disc list-inside text-slate-300">
            <li v-for="spec in product.specs" :key="spec">{{ spec }}</li>
          </ul>
        </div>
        <button @click="addItem({ id: product.id, name: product.name, price: product.price })" 
                class="mt-8 bg-cyan-500 hover:bg-cyan-600 text-black font-semibold py-3 px-8 rounded-full transition">
          Add to Cart
        </button>
      </div>
    </div>
  </div>
  <div v-else class="text-center py-20 text-slate-400">
    Product not found.
  </div>
</template>