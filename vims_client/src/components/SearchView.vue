<script setup>
import SearchForm from './search/SearchForm.vue'
import SearchGallery from './search/SearchGallery.vue'

import { useSearchStore } from '@/stores/search.js'

// * Stores
const search = useSearchStore()
</script>
<template>
  <div>
    <!-- * SEARCH FORM -->
    <div
      class="transition-all duration-700"
      :class="{
        'h-screen': Object.keys(search.serviceImages).length === 0,
        'h-96': Object.keys(search.serviceImages).length > 0
      }"
    >
      <SearchForm />
    </div>

    <!-- * SEARCH GALLERY -->
    <div v-if="Object.keys(search.serviceImages).length > 0">
      <SearchGallery />
    </div>
  </div>
</template>
