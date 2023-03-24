import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useSearchStore = defineStore('search', () => {
  // * Search State
  const isloadingMoreImages = ref(false)

  // * Search Backgrounds
  // List of backgrounds images for the searchview
  // [{...ImageData1}, ...]
  const searchBackgrounds = ref([])

  // * Current Search Params
  const currentServices = ref([])
  const currentSelectedService = ref('')
  const currentSearchQuery = ref('')

  // * Service Images
  // List of images for each service
  // {pexels:{perPage: 15, currentPage: 1, images: [{...ImageData1}, ...]}, unsplash:{...}, ...}
  const serviceImages = ref({})

  function _formatURLQuery(serviceList, searchQuery, page, perPage) {
    const selectedServiceParams = serviceList.map((service) => `service=${service}`).join('&')
    const searchQueryParam = encodeURIComponent(searchQuery)
    const queryParams = `${selectedServiceParams}&query=${searchQueryParam}&page=${page}&per_page=${perPage}`
    return queryParams
  }

  async function _getSearch(queryParams) {
    try {
      const response = await axios.get(`/api/search/?${queryParams}`)
      const data = response.data
      const results = data.results
      return results
    } catch (error) {
      console.log(error)
    }
  }

  async function getSearchBackgrounds(availableServices) {
    if (availableServices.length === 0) {
      return
    }
    const service = availableServices.includes('pixabay') ? 'pixabay' : availableServices[0]

    // * Format URL Query Params
    const queryParams = _formatURLQuery([service], "Nature Forest", 1, 30)

    // * Make request
    const results = await _getSearch(queryParams)

    // * Add images to Search Backgrounds
    searchBackgrounds.value = results[0].images

    return searchBackgrounds.value
  }

  async function searchImages(selectedServices, searchQuery, page = 1, perPage = 15) {
    // Validate not empty
    if (!selectedServices.length || searchQuery === '') {
      return
    }

    // Clean images since is a new search and then set the current search params
    serviceImages.value = {}
    currentServices.value = selectedServices
    currentSelectedService.value = selectedServices[0]
    currentSearchQuery.value = searchQuery

    // * Format URL Query Params
    const queryParams = _formatURLQuery(
      currentServices.value,
      currentSearchQuery.value,
      page,
      perPage
    )

    // * Make request
    const results = await _getSearch(queryParams)

    // * Add images by service
    for (let index in results) {
      const resulService = results[index].service
      serviceImages.value[resulService] = {}
      serviceImages.value[resulService]['currentPage'] = page
      serviceImages.value[resulService]['perPage'] = perPage
      serviceImages.value[resulService]['images'] = results[index].images
    }
  }

  async function addImages() {
    isloadingMoreImages.value = true
    let newImagesList = []
    // Get current search params
    const service = currentSelectedService.value
    const searchQuery = currentSearchQuery.value
    const goToPage = serviceImages.value[service]['currentPage'] + 1
    const perPage = serviceImages.value[service]['perPage']

    // * Format URL Query Params
    const queryParams = _formatURLQuery([service], searchQuery, goToPage, perPage)

    // * Make request
    const results = await _getSearch(queryParams)

    // * Add images to service
    for (let index in results) {
      const resulService = results[index].service
      if (resulService !== service) {
        break
      }
      newImagesList = results[index].images
      // serviceImages.value[service]['images'] = [
      //   ...serviceImages.value[service]['images'],
      //   ...newImagesList
      // ]
    }

    // * Update current page
    serviceImages.value[service]['currentPage'] = goToPage
    isloadingMoreImages.value = false

    return newImagesList
  }

  return {
    isloadingMoreImages,
    searchBackgrounds,
    currentServices,
    currentSelectedService,
    currentSearchQuery,
    serviceImages,
    getSearchBackgrounds,
    searchImages,
    addImages
  }
})
