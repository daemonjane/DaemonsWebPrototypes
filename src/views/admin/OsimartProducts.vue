<script setup>
import { ref, computed, onMounted } from 'vue'

const items = ref([])
const categories = ref([])
const brands = ref([])
const collections = ref([])
const loading = ref(true)
const saving = ref(false)
const showForm = ref(false)
const editing = ref(null)
const form = ref(emptyForm())
const search = ref('')
const filterCategory = ref('')
const filterBrand = ref('')

function emptyForm() {
  return {
    name: '', slug: '', description: '', price: '', compare_at_price: '',
    stock: '', main_image: '', images: '', category_id: '', brand_id: '',
    collection_ids: [], status: 'active', featured: false,
    variants: [],
  }
}

function resetForm() {
  form.value = emptyForm()
  editing.value = null
  showForm.value = false
}

async function getApi() {
  const m = await import('../../utils/api')
  return m.api
}

async function load() {
  loading.value = true
  try {
    const api = await getApi()
    const [prodData, catData, brandData, collData] = await Promise.all([
      api.osimart.products({ limit: 200 }),
      api.osimart.categories(),
      api.osimart.brands(),
      api.osimart.collections(),
    ])
    items.value = prodData.results || prodData || []
    categories.value = catData.results || catData || []
    brands.value = brandData.results || brandData || []
    collections.value = collData.results || collData || []
  } catch (e) {
    console.error('Failed to load products', e)
  } finally {
    loading.value = false
  }
}

const filtered = computed(() => {
  let list = items.value
  if (search.value) {
    const q = search.value.toLowerCase()
    list = list.filter(p => p.name?.toLowerCase().includes(q) || p.slugified_name?.toLowerCase().includes(q))
  }
  if (filterCategory.value) {
    list = list.filter(p => p.categories?.some(c => c.category?.id === filterCategory.value || c.category?.slugified_name === filterCategory.value))
  }
  if (filterBrand.value) {
    list = list.filter(p => p.brand?.id === filterBrand.value || p.brand?.slugified_name === filterBrand.value)
  }
  return list
})

function getCategoryName(p) {
  return p.categories?.[0]?.category?.name || 'Uncategorized'
}

function getBrandName(p) {
  return p.brand?.name || '-'
}

function openCreate() {
  editing.value = null
  form.value = emptyForm()
  showForm.value = true
}

function openEdit(item) {
  editing.value = item.id
  form.value = {
    name: item.name || '',
    slug: item.slugified_name || '',
    description: item.description || '',
    price: item.price_range || '',
    compare_at_price: item.compare_at_price || '',
    stock: item.remaining_stock ?? item.stock ?? '',
    main_image: item.main_image || '',
    images: Array.isArray(item.images) ? item.images.join('\n') : '',
    category_id: item.categories?.[0]?.category?.id || '',
    brand_id: item.brand?.id || '',
    collection_ids: (item.collections || []).map(c => c.id || c.collection?.id).filter(Boolean),
    status: item.status || 'active',
    featured: item.featured || false,
    variants: Array.isArray(item.variants) ? item.variants.map(v => ({ ...v })) : [],
  }
  showForm.value = true
}

async function save() {
  saving.value = true
  try {
    const api = await getApi()
    const images = form.value.images
      ? form.value.images.split('\n').map(s => s.trim()).filter(Boolean)
      : []
    const variants = form.value.variants.length
      ? form.value.variants.map(v => {
          const vp = { name: v.name, price: v.price }
          if (v.remaining_stock != null) vp.remaining_stock = Number(v.remaining_stock)
          else if (v.stock != null) vp.remaining_stock = Number(v.stock)
          if (v.values?.length) vp.values = v.values
          if (v.id) vp.id = v.id
          return vp
        })
      : undefined
    const payload = {
      name: form.value.name || undefined,
      description: form.value.description || undefined,
      price_range: form.value.price || undefined,
      compare_at_price: form.value.compare_at_price || undefined,
      remaining_stock: form.value.stock ? Number(form.value.stock) : undefined,
      main_image: form.value.main_image || undefined,
      images: images.length ? images : undefined,
      category_id: form.value.category_id || undefined,
      brand_id: form.value.brand_id || undefined,
      collection_ids: form.value.collection_ids.length ? form.value.collection_ids : undefined,
      status: form.value.status || undefined,
      featured: form.value.featured ? 1 : 0,
      variants,
    }
    Object.keys(payload).forEach(k => { if (payload[k] === undefined) delete payload[k] })

    if (editing.value) {
      await api.osimart.updateProduct(editing.value, payload)
    } else {
      await api.osimart.createProduct(payload)
    }
    resetForm()
    await load()
  } catch (e) {
    alert('Save failed: ' + e.message)
  } finally {
    saving.value = false
  }
}

async function remove(id) {
  if (!confirm('Delete this product?')) return
  try {
    const api = await getApi()
    await api.osimart.deleteProduct(id)
    await load()
  } catch (e) {
    alert('Delete failed: ' + e.message)
  }
}

function addVariant() {
  form.value.variants.push({ name: '', price: '', remaining_stock: '', values: [] })
}

function removeVariant(idx) {
  form.value.variants.splice(idx, 1)
}

function productImage(p) {
  if (p.main_image) return p.main_image
  if (p.images?.length) return p.images[0]
  return null
}

onMounted(load)
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-semibold text-white">Products</h2>
      <button @click="openCreate" class="bg-cyan-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-cyan-500">+ New Product</button>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-3 mb-4 p-3 bg-slate-800/30 rounded-lg border border-slate-800">
      <input v-model="search" placeholder="Search name or slug..." class="flex-1 min-w-[160px] bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
      <select v-model="filterCategory" class="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white">
        <option value="">All categories</option>
        <option v-for="c in categories" :key="c.id" :value="c.id || c.slugified_name">{{ c.name }}</option>
      </select>
      <select v-model="filterBrand" class="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white">
        <option value="">All brands</option>
        <option v-for="b in brands" :key="b.id" :value="b.id || b.slugified_name">{{ b.name }}</option>
      </select>
    </div>

    <!-- Product form modal -->
    <div v-if="showForm" class="fixed inset-0 z-50 flex items-start justify-center pt-8 pb-8 overflow-y-auto bg-black/60" @click.self="resetForm">
      <div class="bg-slate-900 rounded-xl border border-slate-700 w-full max-w-3xl mx-4 shadow-2xl">
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-800">
          <h3 class="text-lg font-semibold text-white">{{ editing ? 'Edit Product' : 'New Product' }}</h3>
          <button @click="resetForm" class="text-slate-500 hover:text-white text-xl leading-none">&times;</button>
        </div>
        <form @submit.prevent="save" class="p-6 space-y-5 max-h-[70vh] overflow-y-auto">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="text-xs text-slate-500 font-medium block mb-1">Name *</label>
              <input v-model="form.name" required class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Slug</label>
              <input v-model="form.slug" placeholder="Auto-generated from name" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Status</label>
              <select v-model="form.status" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white">
                <option value="active">Active</option>
                <option value="draft">Draft</option>
                <option value="archived">Archived</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="text-xs text-slate-500 font-medium block mb-1">Description</label>
              <textarea v-model="form.description" rows="3" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white"></textarea>
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Price *</label>
              <input v-model="form.price" required placeholder="0.00" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Compare at Price</label>
              <input v-model="form.compare_at_price" placeholder="0.00" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Stock</label>
              <input v-model="form.stock" type="number" min="0" placeholder="0" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Category</label>
              <select v-model="form.category_id" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white">
                <option value="">None</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Brand</label>
              <select v-model="form.brand_id" class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white">
                <option value="">None</option>
                <option v-for="b in brands" :key="b.id" :value="b.id">{{ b.name }}</option>
              </select>
            </div>
            <div>
              <label class="text-xs text-slate-500 font-medium block mb-1">Collections</label>
              <select v-model="form.collection_ids" multiple class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white h-20">
                <option v-for="c in collections" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
            </div>
            <div class="md:col-span-2">
              <label class="text-xs text-slate-500 font-medium block mb-1">Main Image URL</label>
              <input v-model="form.main_image" placeholder="https://..." class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white" />
            </div>
            <div class="md:col-span-2">
              <label class="text-xs text-slate-500 font-medium block mb-1">Additional Images (one URL per line)</label>
              <textarea v-model="form.images" rows="3" placeholder="https://..." class="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 text-sm text-white"></textarea>
            </div>
            <div class="md:col-span-2 flex items-center gap-2">
              <input v-model="form.featured" type="checkbox" id="featured-check" class="rounded border-slate-700 bg-slate-800 text-cyan-500 accent-cyan-500" />
              <label for="featured-check" class="text-sm text-white">Featured product</label>
            </div>
          </div>

          <!-- Variants section -->
          <div class="border-t border-slate-800 pt-4">
            <div class="flex items-center justify-between mb-3">
              <h4 class="text-sm font-semibold text-white">Variants</h4>
              <button type="button" @click="addVariant" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1 border border-cyan-800/50 rounded">+ Add variant</button>
            </div>
            <div v-if="!form.variants.length" class="text-xs text-slate-500 py-2">No variants defined.</div>
            <div v-for="(v, i) in form.variants" :key="i" class="flex flex-wrap items-center gap-2 mb-2 bg-slate-800/30 rounded-lg p-3 border border-slate-800">
              <input v-model="v.name" placeholder="Name (e.g. Black / Large)" class="flex-1 min-w-[120px] bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-xs text-white" />
              <input v-model="v.price" placeholder="Price" class="w-20 bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-xs text-white" />
              <input v-model="v.remaining_stock" type="number" min="0" placeholder="Stock" class="w-16 bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-xs text-white" />
              <button type="button" @click="removeVariant(i)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Remove</button>
            </div>
          </div>

          <div class="flex items-center gap-3 pt-2 border-t border-slate-800">
            <button type="submit" :disabled="saving" class="bg-cyan-600 text-white px-6 py-2 rounded text-sm font-semibold hover:bg-cyan-500 disabled:opacity-50">
              {{ saving ? 'Saving...' : (editing ? 'Update' : 'Create') }}
            </button>
            <button type="button" @click="resetForm" class="bg-slate-700 text-slate-300 px-4 py-2 rounded text-sm hover:bg-slate-600">Cancel</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Product list -->
    <div v-if="loading" class="text-slate-500 text-sm py-8 text-center">Loading...</div>
    <div v-else-if="!items.length" class="text-slate-500 text-sm py-8 text-center">No products yet.</div>
    <div v-else class="space-y-2">
      <div v-for="item in filtered" :key="item.id" class="flex items-center gap-3 bg-slate-800/30 rounded-lg px-4 py-3 border border-slate-800 hover:border-slate-700">
        <div class="w-10 h-10 rounded-lg bg-slate-800 overflow-hidden shrink-0 flex items-center justify-center">
          <img v-if="productImage(item)" :src="productImage(item)" :alt="item.name" class="w-full h-full object-cover" />
          <span v-else class="text-slate-600 text-lg">📦</span>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-white font-medium truncate">{{ item.name }}</p>
          <p class="text-xs text-slate-500 truncate">
            <span class="text-cyan-400 font-mono">${{ item.price_range || '0' }}</span>
            <span class="mx-1.5">·</span>
            {{ getCategoryName(item) }}
            <span class="mx-1.5">·</span>
            {{ getBrandName(item) }}
            <span class="mx-1.5">·</span>
            <span class="text-slate-500">Stock: {{ item.remaining_stock ?? item.stock ?? 0 }}</span>
          </p>
        </div>
        <span class="text-[10px] uppercase px-2 py-0.5 rounded-full font-medium" :class="item.status === 'active' ? 'bg-emerald-900/40 text-emerald-300' : 'bg-slate-700 text-slate-400'">{{ item.status || 'draft' }}</span>
        <button @click="openEdit(item)" class="text-xs text-cyan-400 hover:text-cyan-300 px-2 py-1">Edit</button>
        <button @click="remove(item.id)" class="text-xs text-red-400 hover:text-red-300 px-2 py-1">Delete</button>
      </div>
      <p v-if="filtered.length !== items.length" class="text-xs text-slate-500 pt-2 text-center">{{ filtered.length }} of {{ items.length }} products</p>
    </div>
  </div>
</template>
