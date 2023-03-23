<script setup>
import { ref } from 'vue'
import IconHeart from '../icons/IconHeart.vue'
import IconHeartRed from '../icons/IconHeartRed.vue'
import SearchImageModal from './SearchImageModal.vue'

const props = defineProps({ image: Object })

const showModal = ref(false)

function print(msg) {
  console.log(msg)
}
</script>
<template>
  <div @click="showModal = true" class="rounded-lg overflow-hidden relative group cursor-pointer">
    <img class="w-full object-cover" :src="props.image.preview_url" :alt="props.image.name" />

    <button
      @click.stop="print('Add to favorite')"
      class="hidden group-hover:flex btn btn-md btn-square btn-outline btn-primary absolute top-3 right-3 cursor-default bg-white/70 border-white"
    >
      <IconHeart />
      <!-- <IconHeartRed /> -->
    </button>
  </div>

  <!-- * SEARCH IMAGE MODAL -->
  <Teleport to="body">
    <SearchImageModal :show="showModal" :image="props.image" @close="showModal = false" />
  </Teleport>
</template>
