<script setup>
defineProps({
  type: {
    type: String,
    default: 'page',
    validator: v => ['page', 'card', 'detail', 'list', 'banner'].includes(v),
  },
})
</script>

<template>
  <div class="animate-pulse space-y-6" role="status" aria-label="Content loading">
    <!-- Page layout (default) -->
    <div v-if="type === 'page'" class="space-y-6">
      <div class="h-8 skeleton rounded w-1/3"></div>
      <div class="h-4 skeleton rounded w-2/3"></div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 pt-4">
        <div class="h-48 skeleton rounded-xl"></div>
        <div class="h-48 skeleton rounded-xl"></div>
        <div class="h-48 skeleton rounded-xl"></div>
      </div>
      <div class="h-4 skeleton rounded w-full"></div>
      <div class="h-4 skeleton rounded w-5/6"></div>
      <div class="h-4 skeleton rounded w-4/6"></div>
    </div>

    <!-- Card layout -->
    <div v-else-if="type === 'card'" class="space-y-3">
      <div class="h-40 skeleton rounded-xl"></div>
      <div class="h-4 skeleton rounded w-3/4"></div>
      <div class="h-3 skeleton rounded w-1/2"></div>
      <div class="h-8 skeleton rounded w-1/3"></div>
    </div>

    <!-- Product detail layout -->
    <div v-else-if="type === 'detail'" class="grid md:grid-cols-2 gap-8">
      <div class="h-72 sm:h-96 skeleton rounded-xl"></div>
      <div class="space-y-4">
        <div class="h-4 skeleton rounded w-1/4"></div>
        <div class="h-8 skeleton rounded w-3/4"></div>
        <div class="h-6 skeleton rounded w-1/3"></div>
        <div class="h-4 skeleton rounded w-full"></div>
        <div class="h-4 skeleton rounded w-full"></div>
        <div class="h-4 skeleton rounded w-2/3"></div>
        <div class="grid grid-cols-2 gap-2 pt-4">
          <div v-for="i in 4" :key="i" class="h-10 skeleton rounded-lg"></div>
        </div>
        <div class="h-12 skeleton rounded-lg w-40 pt-4"></div>
      </div>
    </div>

    <!-- Banner layout -->
    <div v-else-if="type === 'banner'" class="h-48 sm:h-72 skeleton rounded-xl"></div>

    <!-- List layout -->
    <div v-else-if="type === 'list'" class="space-y-4">
      <div v-for="i in 4" :key="i" class="flex gap-4 items-center">
        <div class="w-16 h-16 skeleton rounded-lg shrink-0"></div>
        <div class="flex-1 space-y-2">
          <div class="h-4 skeleton rounded w-1/2"></div>
          <div class="h-3 skeleton rounded w-1/4"></div>
        </div>
      </div>
    </div>
  </div>
</template>
