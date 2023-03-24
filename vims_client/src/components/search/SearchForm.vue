<script setup>
import { ref, onMounted, capitalize } from 'vue'
import { useServiceStore } from '@/stores/service.js'
import { useSearchStore } from '@/stores/search.js'

// * Stores
const service = useServiceStore()
const search = useSearchStore()

// * References
const selectedServices = ref([])
const searchQuery = ref('')
const searchBackgroundStyle = ref({backgroundImage: ''})

function _getRandomItem(arr) {
  const randomIndex = Math.floor(Math.random() * arr.length)
  const item = arr[randomIndex]
  return item
}

async function initSearchForm() {
  // Get available services from api
  selectedServices.value = await service.getServices()
  // Get list of backgrounds and choice a random one
  const searchBackgrounds = await search.getSearchBackgrounds(selectedServices.value)
  const randomSearchBackground = _getRandomItem(searchBackgrounds)
  searchBackgroundStyle.value = {
    backgroundImage: `url(${randomSearchBackground.original_url})`
  }
}

onMounted(() => {
  initSearchForm()
})
</script>

<template>
  <!-- class=" h-full pt-20 bg-gradient-to-tr from-indigo-700 to-purple-300" -->
  <div :style="searchBackgroundStyle" class="search-background h-full pt-20">
    <div class="container h-full mx-auto flex flex-col justify-center items-center">
      <p
        class="max-w-md my-3 text-center text-lg md:text-2xl text-white font-semibold drop-shadow-lg shadow-black"
      >
        The best image vault and search aggregator, upload youserself or explore images and save as
        favorites.
      </p>

      <!-- * SEARCH FORM -->
      <div>
        <input
          type="text"
          placeholder="Search"
          class="block input input-bordered input-primary w-full max-w-xs"
          v-model="searchQuery"
          @keyup.enter="search.searchImages(selectedServices, searchQuery)"
        />
        <div
          v-for="(service, index) in service.availableServices"
          :key="index"
          class="inline-flex m-2 items-center"
        >
          <input
            type="checkbox"
            checked="true"
            class="checkbox checkbox-sm checkbox-primary"
            :id="'service-' + index"
            :value="service"
            v-model="selectedServices"
            @keyup.enter="search.searchImages(selectedServices, searchQuery)"
          />
          <label
            :for="'service-' + index"
            class="ml-2 text-white font-semibold drop-shadow-lg shadow-black"
            >{{ capitalize(service) }}</label
          >
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-background {
  background-color: #6b7280;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  position: relative;
  transition: background-image 0.5s ease-in-out;
}
</style>
