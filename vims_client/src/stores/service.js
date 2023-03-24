import { ref, watch } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAppStore } from './app'

export const useServiceStore = defineStore('service', () => {
  // * stores
  const app = useAppStore()
  watch(app, showReCaptchaBadge)

  // * Image Services
  const availableServices = ref([])

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

  // * Google reCaptcha
  const reCaptchaKey = ref('DEBUGKey')
  const reCaptchaDebug = ref(true)
  const reCaptchaReady = ref(false)
  const showBadgeOnViews = ['login', 'signup']

  async function _getReCaptchaPublicKey() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/recaptcha/')
      const data = response.data
      reCaptchaKey.value = data['key']
      return reCaptchaKey.value
    } catch (error) {
      console.log(error)
    }
  }

  async function initReCatpcha() {
    const publicKey = await _getReCaptchaPublicKey()
    // If the response from the server is the Debug Key
    if (publicKey === 'MyPublicReCaptchaKey') {
      reCaptchaDebug.value = true
      reCaptchaReady.value = true
      console.log('WARNING: Using reCaptcha Development Mode')
      return publicKey
    }
    // Else, init reCaptcha
    let recaptchaScript = document.createElement('script')
    recaptchaScript.setAttribute(
      'src',
      `https://www.google.com/recaptcha/api.js?render=${publicKey}`
    )
    document.head.appendChild(recaptchaScript)
    reCaptchaDebug.value = false
    reCaptchaReady.value = true
    return publicKey
  }

  async function getReCaptchaToken(action) {
    let token = 'AnyReCaptchaToken'

    if (reCaptchaDebug.value) {
      return token
    }

    try {
      // eslint-disable-next-line no-undef
      await grecaptcha.ready(async function () {
        // eslint-disable-next-line no-undef
        token = await grecaptcha.execute(reCaptchaKey.value, { action: action })
      })
    } catch (error) {
      console.error(error)
    }
    return token
  }

  // * Show recaptcha badge on selected Views
  function showReCaptchaBadge() {
    const elements = document.getElementsByClassName('grecaptcha-badge')
    if (elements.length > 0) {
      const reCaptchaBadgeEl = elements[0]
      if (showBadgeOnViews.includes(app.currentView)) {
        reCaptchaBadgeEl.style.visibility = 'visible'
      } else {
        reCaptchaBadgeEl.style.visibility = 'hidden'
      }
    }
  }

  return {
    availableServices,
    getServices,
    reCaptchaReady,
    reCaptchaDebug,
    initReCatpcha,
    getReCaptchaToken
  }
})