<script setup>
/**
 * Breadcrumb navigation trail.
 * @component
 * @prop {Array<{label: string, to?: string}>} crumbs - Array of breadcrumb segments
 */
defineProps({
  crumbs: { type: Array, required: true }
})
</script>

<template>
  <nav aria-label="Breadcrumb" class="mb-4" vocab="https://schema.org/" typeof="BreadcrumbList">
    <ol class="flex flex-wrap items-center gap-1.5 text-xs sm:text-sm">
      <li property="itemListElement" typeof="ListItem">
        <router-link to="/" property="item" typeof="WebPage" class="text-slate-500 hover:text-cyan-400 transition-colors">Home</router-link>
        <meta property="position" content="1">
      </li>
      <li v-for="(crumb, i) in crumbs" :key="i" class="flex items-center gap-1.5" property="itemListElement" typeof="ListItem">
        <svg class="w-3 h-3 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
        <router-link
          v-if="crumb.to && i < crumbs.length - 1"
          :to="crumb.to"
          property="item"
          typeof="WebPage"
          class="text-slate-500 hover:text-cyan-400 transition-colors"
        >
          {{ crumb.label }}
        </router-link>
        <span v-else class="text-slate-300 font-medium" :aria-current="i === crumbs.length - 1 ? 'page' : undefined" property="name">
          {{ crumb.label }}
        </span>
        <meta :property="'position'" :content="String(i + 2)">
      </li>
    </ol>
  </nav>
</template>
