<script setup>
import { capitalize } from 'vue'
import IconClose from '../icons/IconClose.vue'
import IconUserAvatar from '../icons/IconUserAvatar.vue'
import IconDownload from '../icons/IconDownload.vue'
import IconLinkTo from '../icons/IconLinkTo.vue'

const props = defineProps({
  show: Boolean,
  image: Object
})
</script>

<template>
  <Transition name="modal">
    <div v-if="show" @click.self="$emit('close')" class="modal-mask pt-10 pb-20 flex flex-col">
      <div class="flex w-8 mx-auto h-8 m-2 text-white font-bol">
        <IconClose />
      </div>

      <div class="modal-container container mx-auto h-full p-5 flex flex-col md:flex-row overflow-hidden rounded-xl bg-white">
        <!-- * IMAGE -->
        <div class="w-full h-3/4 md:h-full">
          <img
            class="w-full h-full object-contain"
            :src="props.image.original_url"
            :alt="props.image.name"
          />
        </div>

        <!-- * IMAGE INFORMATION -->
        <div class="pt-3 px-3 w-full h-1/4 md:w-2/6 md:min-w-fit md:h-full md:flex md:flex-col md:justify-center md:items-center">
          <h2 class="font-bold text-center text-2xl">
            {{ capitalize(props.image.service) }}
          </h2>
          <div class="w-full flex justify-center items-center text-xl">
            <IconUserAvatar />
            <p>{{ props.image.author }}</p>
          </div>
          <div class="pt-3 w-full flex flex-row md:flex-col justify-center items-center gap-5">
            <a :href="props.image.original_url" target="_blank" class="w-fit flex flex-row btn btn-md gap-2">
              <IconDownload />
              <p class="max-[400px]:hidden">DOWNLOAD</p>
            </a>
            <a :href="props.image.link" target="_blank" class="w-fit btn btn-md gap-2">
              <IconLinkTo />
              <p class="max-[400px]:hidden">ORIGINAL</p>
            </a>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  transition: opacity 0.3s ease;
}

/*
 * MODAL TRANSITION STYLES
 */

.modal-enter-from {
  opacity: 0;
}

.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
