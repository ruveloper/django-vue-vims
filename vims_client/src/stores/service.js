import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useServiceStore = defineStore('service', () => {

  const availableServices = ref([])
  // const doubleCount = computed(() => count.value * 2)

  async function getServices() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/services/')
      const data = response.data
      availableServices.value = data['services']
      return availableServices.value
    } catch (error) {
      console.log(error)
    }
  }

  return { availableServices, getServices }
})
