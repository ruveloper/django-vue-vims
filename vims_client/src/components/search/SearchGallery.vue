<script setup>
import { capitalize, createApp, h } from 'vue'
import { useSearchStore } from '@/stores/search.js'
import SearchImageCard from './SearchImageCard.vue'

// * Stores
const search = useSearchStore()

async function addImages(service) {
  const newImagesList = await search.addImages()

  const imageSet = document.createElement('div')
  imageSet.classList.add('gap-5', 'columns-xs', 'mt-5')

  for (let index in newImagesList) {
    const newImage = newImagesList[index]
    const newSearchImageCard = createApp({
      setup() {
        return () => h(SearchImageCard, { image: newImage })
      }
    })

    const wrapper = document.createElement('div')
    wrapper.classList.add('w-full', 'aspect-auto', 'mb-5')
    newSearchImageCard.mount(wrapper)
    imageSet.appendChild(wrapper)
  }

  // * Add image set to the service image container
  const imageContainer = document.getElementById(`${service}-image-container`)
  imageContainer.appendChild(imageSet)
}
</script>
<template>
  <div class="container mx-auto">
    <!-- * TABS -->
    <div class="tabs tabs-boxed w-fit mx-auto my-4 bg-white">
      <a
        v-for="(service, index) in search.currentServices"
        :key="index"
        class="tab tab-md mx-2"
        :class="{ 'tab-active': service === search.currentSelectedService }"
        @click="search.currentSelectedService = service"
      >
        {{ capitalize(service) }}
      </a>
    </div>

    <!-- * SERVICE TABS -->
    <div
      v-for="(imageServiceData, service, index) in search.serviceImages"
      :key="index"
      class="w-full"
    >
      <!-- * GALLERY BY SERVICE -->
      <div :class="{ hidden: service !== search.currentSelectedService }">
        <div v-if="imageServiceData.images.length > 0" class="relative">
          <!-- * IMAGES -->
          <div :id="service + '-image-container'">
            <div class="gap-5 columns-xs">
              <div
                v-for="(image, index) in imageServiceData.images"
                :key="index"
                class="w-full aspect-auto mb-5"
              >
                <SearchImageCard :image="image" />
              </div>
            </div>
          </div>

          <!-- * LOAD MORE -->
          <div
            class="h-40 absolute bottom-0 inset-x-0 flex justify-center items-center bg-gradient-to-t from-white to-transparent"
          >
            <button
              @click="addImages(service)"
              class="btn btn-wide btn-primary"
              :class="{ loading: search.isloadingMoreImages }"
            >
              Load more
            </button>
          </div>
        </div>
        <!-- * NO IMAGES RESULT -->
        <div v-if="imageServiceData.images.length === 0" class="my-20 px-10 text-center text-purple-600 font-bold text-2xl">
          <p>Nothing to show from {{ capitalize(service) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
