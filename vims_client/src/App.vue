<script setup>
import AppHeader from './components/AppHeader.vue';
import SearchView from './components/SearchView.vue';
</script>

<template>
  <div class="relative">
    <div class="fixed inset-x-0 top-3 z-10">
      <AppHeader/>
    </div>
  </div>

  <main class="z-0">
    <!-- <Search View /> -->
    <SearchView/>
  </main>
</template>

<style scoped></style>
