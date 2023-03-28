<script setup>
import { ref, onBeforeMount, watch } from 'vue'
import { useAppStore } from '../../stores/app'
import IconHeart from '../icons/IconHeart.vue'
import IconHeartRed from '../icons/IconHeartRed.vue'
import SearchImageModal from './SearchImageModal.vue'

const props = defineProps({ image: Object })

// * stores
const app = useAppStore()

// * references
const imageData = ref({})
const isFavorite = ref(false)
const showModal = ref(false)

async function toggleFavorite() {
  if (!isFavorite.value) {
    const response = await app.addFavoriteImage(imageData.value)
    // Update image data with new ID
    imageData.value = response.data
  } else {
    await app.removeFavoriteImage(imageData.value)
  }
  // Update favorite state
  isFavorite.value = checkFavorite()
}

function checkFavorite() {
  if (Object.keys(app.userData).length === 0 || app.userData.userdata === null) {
    return false
  }
  const favoriteImages = app.userData.userdata.userfavoriteimage_set
  for (const index in favoriteImages) {
    const img = favoriteImages[index]
    if (imageData.value.link === img.link) {
      // Update image data
      imageData.value = img
      return true
    }
  }
  return false
}

// * Watch if image is remove from favorites on userData updates
watch(app, () => {
  isFavorite.value = checkFavorite()
})

onBeforeMount(() => {
  // Asing props to a ref in order to allow mutations
  imageData.value = props.image
  isFavorite.value = checkFavorite()
})
</script>
<template>
  <div @click="showModal = true" class="rounded-lg overflow-hidden relative group cursor-pointer">
    <img class="w-full object-cover" :src="imageData.preview_url" :alt="imageData.name" />

    <button
      v-if="Object.keys(app.userData).length > 0"
      @click.stop="toggleFavorite"
      class="btn btn-sm btn-square btn-outline btn-primary absolute top-3 right-3 cursor-default bg-white/60 border-white lg:btn-md lg:hidden lg:group-hover:flex"
    >
      <IconHeart v-if="!isFavorite" />
      <IconHeartRed v-if="isFavorite" />
    </button>
  </div>

  <!-- * SEARCH IMAGE MODAL -->
  <Teleport to="body">
    <SearchImageModal :show="showModal" :image="imageData" @close="showModal = false" />
  </Teleport>
</template>
