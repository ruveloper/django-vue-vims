<script setup>
import { useAppStore } from '../stores/app'
import SearchImageCard from './search/SearchImageCard.vue'

// * Stores
const app = useAppStore()
</script>
<template>
  <div class="min-w-screen min-h-screen pt-20 bg-gray-500">
    <!-- * USER INFORMATION -->
    <div class="w-full h-56 flex flex-col gap-4 justify-center items-center text-white  text-center">
      <div v-if="Object.keys(app.userData).length !== 0">
        <h1 class="font-bold text-3xl">{{app.userData.username}}</h1>
        <hr class="w-80" />
        <div class="flex flex-row justify-center items-center gap-4">
          <div>
            <h2>User Images</h2>
            <p class="font-bold text-xl">{{ app.userData.userdata?.userimage_set.length ?? 0 }}</p>
          </div>
          <div>
            <h2>Favorite Images</h2>
            <p class="font-bold text-xl">
              {{ app.userData.userdata?.userfavoriteimage_set.length ?? 0 }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- * USER FAVORITES GALLERY -->
    <div class="w-full bg-white">
      <div class="container mx-auto py-20">
        <div v-if="Object.keys(app.userData).length !== 0">
          <!-- * IMAGES -->
          <div v-if="app.userData.userdata !== null">
            <div class="gap-5 columns-xs">
              <div
                v-for="image in app.userData.userdata.userfavoriteimage_set"
                :key="image.link"
                class="w-full aspect-auto mb-5"
              >
                <SearchImageCard :image="image" />
              </div>
            </div>
          </div>
          <!-- * NO IMAGES RESULT -->
          <div v-if="app.userData.userdata === null" class="my-20 px-10 text-center">
            <p class="text-purple-600 font-bold text-2xl">Nothing to show</p>
            <p class="text-xl">Start save favorites from search view.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
