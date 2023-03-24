import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import axios from 'axios'

import './assets/css/main.css'

// * BACKEND_API_BASE_URL
// Config base api url for axios requests
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/'
axios.defaults.baseURL = API_BASE_URL
console.log(`BASE API URL: ${axios.defaults.baseURL}`)

const app = createApp(App)

app.use(createPinia())

app.mount('#app')
