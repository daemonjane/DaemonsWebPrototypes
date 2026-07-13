<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUser } from '../composables/useUser'
import Breadcrumbs from '../components/Breadcrumbs.vue'

const router = useRouter()
const { user, isAuthenticated, refresh } = useUser()
const editing = ref(false)
const pending = ref(false)
const saved = ref(false)
const form = reactive({ username: '', email: '', bio: '', location: '', phone: '' })
const errors = reactive({})

onMounted(async () => {
  await refresh()
  if (!user.value) { router.push('/login'); return }
  resetForm()
})

function resetForm() {
  if (!user.value) return
  form.username = user.value.username || ''
  form.email = user.value.email || ''
  form.bio = user.value.profile?.bio || ''
  form.location = user.value.profile?.location || ''
  form.phone = user.value.profile?.phone || ''
}

async function save() {
  Object.keys(errors).forEach(k => delete errors[k])
  saved.value = false
  pending.value = true
  try {
    const { api } = await import('../utils/api')
    const userData = JSON.parse(localStorage.getItem('gg-user') || '{}')
    const customerId = userData?.id || userData?.customer_id
    if (customerId) {
      await api.osimart.updateCustomer(customerId, { ...form })
    } else {
      await api.osimart.updateProfile({ ...form })
    }
    await refresh()
    saved.value = true
    editing.value = false
    setTimeout(() => { saved.value = false }, 3000)
  } catch (e) {
    errors.save = e.message || 'Failed to save'
  } finally {
    pending.value = false
  }
}

function cancel() {
  resetForm()
  editing.value = false
  Object.keys(errors).forEach(k => delete errors[k])
}
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <Breadcrumbs :crumbs="[{ label: 'Profile' }]" />
    <div class="bg-surface-900 border border-surface-700 rounded-xl p-6 sm:p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold font-display text-surface-50">My Profile</h1>
        <button v-if="!editing" @click="editing = true" class="text-sm text-electric-500 hover:text-electric-400 flex items-center gap-1">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          Edit
        </button>
      </div>

      <p v-if="saved" class="mb-4 p-3 rounded-lg bg-emerald-950/30 border border-emerald-700/50 text-emerald-300 text-sm" role="alert">Profile saved!</p>
      <p v-if="errors.save" class="mb-4 p-3 rounded-lg bg-pink-950/30 border border-pink-700/50 text-pink-300 text-sm" role="alert">{{ errors.save }}</p>

      <div v-if="!editing" class="space-y-4">
        <div class="pb-4 border-b border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Username</p>
          <p class="text-surface-100 mt-1">{{ user?.username }}</p>
        </div>
        <div class="pb-4 border-b border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Email</p>
          <p class="text-surface-100 mt-1">{{ user?.email }}</p>
        </div>
        <div class="pb-4 border-b border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Bio</p>
          <p class="text-surface-100 mt-1">{{ user?.profile?.bio || '—' }}</p>
        </div>
        <div class="pb-4 border-b border-surface-700">
          <p class="text-xs text-surface-500 uppercase tracking-wider">Location</p>
          <p class="text-surface-100 mt-1">{{ user?.profile?.location || '—' }}</p>
        </div>
        <div>
          <p class="text-xs text-surface-500 uppercase tracking-wider">Phone</p>
          <p class="text-surface-100 mt-1">{{ user?.profile?.phone || '—' }}</p>
        </div>
        <div v-if="user?.is_staff || user?.is_superuser" class="pt-4 border-t border-surface-700">
          <router-link to="/dashboard/" class="inline-flex items-center gap-2 bg-surface-800 hover:bg-surface-600 border border-surface-700 text-surface-200 text-sm font-semibold py-2 px-4 rounded-lg transition-colors">
            Dashboard
          </router-link>
        </div>
      </div>

      <form v-else @submit.prevent="save" class="space-y-4">
        <div>
          <label class="block text-sm text-surface-400 mb-1">Username</label>
          <input v-model="form.username" class="w-full bg-surface-800 border border-surface-700 rounded p-3 text-sm focus:outline-none focus:ring-2 focus:ring-electric-500/50">
        </div>
        <div>
          <label class="block text-sm text-surface-400 mb-1">Email</label>
          <input v-model="form.email" type="email" class="w-full bg-surface-800 border border-surface-700 rounded p-3 text-sm focus:outline-none focus:ring-2 focus:ring-electric-500/50">
        </div>
        <div>
          <label class="block text-sm text-surface-400 mb-1">Bio</label>
          <textarea v-model="form.bio" rows="3" class="w-full bg-surface-800 border border-surface-700 rounded p-3 text-sm focus:outline-none focus:ring-2 focus:ring-electric-500/50"></textarea>
        </div>
        <div>
          <label class="block text-sm text-surface-400 mb-1">Location</label>
          <input v-model="form.location" class="w-full bg-surface-800 border border-surface-700 rounded p-3 text-sm focus:outline-none focus:ring-2 focus:ring-electric-500/50">
        </div>
        <div>
          <label class="block text-sm text-surface-400 mb-1">Phone</label>
          <input v-model="form.phone" class="w-full bg-surface-800 border border-surface-700 rounded p-3 text-sm focus:outline-none focus:ring-2 focus:ring-electric-500/50">
        </div>
        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="pending" class="bg-electric-500 hover:bg-electric-400 text-surface-50 font-semibold py-2 px-6 rounded-lg transition-colors disabled:opacity-50">
            {{ pending ? 'Saving...' : 'Save' }}
          </button>
          <button type="button" @click="cancel" class="bg-surface-800 hover:bg-surface-600 text-surface-200 py-2 px-6 rounded-lg transition-colors">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>
