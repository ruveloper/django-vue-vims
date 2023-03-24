<script setup>
import { ref } from 'vue'
import { useAppStore } from '../stores/app'
import { useServiceStore } from '../stores/service'

// * Stores
const service = useServiceStore()
const app = useAppStore()

const form = ref({})
const formErrors = ref({})
const formNonFieldErrors = ref({})
const isFormLoading = ref(false)

async function handleLogInSubmit() {
  isFormLoading.value = true

  // * Get reCaptcha Token
  const reCaptchaToken = await service.getReCaptchaToken('login')
  form.value['g-recaptcha-response'] = reCaptchaToken

  // * Register
  const response = await app.login(form.value)
  // If errors
  if (response.status === 400) {
    formErrors.value = response.data

    // Set non-field errors
    const excludedKeys = ['username', 'password']
    formNonFieldErrors.value = Object.keys(formErrors.value)
      .filter((key) => !excludedKeys.includes(key))
      .reduce((obj, key) => {
        obj[key] = formErrors.value[key]
        return obj
      }, {})

    isFormLoading.value = false
    return
  }
  // If Success, got to search view
  if (response.status === 200 && app.userToken !== '') {
    app.currentView = 'search'
  }

  // * Reset Form
  isFormLoading.value = false
  form.value = {}
}
</script>

<template>
  <div class="min-w-screen min-h-screen pt-20 flex justify-center items-center bg-gray-500">
    <div class="w-96 my-10 flex flex-col max-w-md p-6 rounded-md sm:px-10 bg-gray-50 text-gray-800">
      <div class="mb-8 text-center">
        <h1 class="my-3 text-4xl font-bold">Log In</h1>
        <p class="text-sm text-gray-600">Sign in to access your account and favorites</p>
      </div>

      <form @submit.prevent="handleLogInSubmit" novalidate="true" action="" class="space-y-12">
        <!-- * FORM FIELDS -->
        <div class="space-y-4">
          <div>
            <label for="username" class="block mb-2 text-sm">Username</label>
            <input
              type="username"
              name="username"
              id="username"
              placeholder="yourname"
              v-model="form.username"
              class="w-full px-3 py-2 border rounded-md border-gray-300 bg-gray-50 text-gray-800"
            />
            <div v-if="'username' in formErrors" class="text-red-600 text-end text-sm">
              <p v-for="(error, index) in formErrors.username" :key="'usernameError' + index">
                {{ error }}
              </p>
            </div>
          </div>
          <div>
            <label for="password" class="text-sm">Password</label>
            <input
              type="password"
              name="password"
              id="password"
              placeholder="*****"
              v-model="form.password"
              class="w-full px-3 py-2 border rounded-md border-gray-300 bg-gray-50 text-gray-800"
            />
            <div v-if="'password' in formErrors" class="text-red-600 text-end text-sm">
              <p v-for="(error, index) in formErrors.password" :key="'passwordError' + index">
                {{ error }}
              </p>
            </div>
          </div>
        </div>

        <!-- * NON FIELD ERRORS -->
        <div
          v-for="(error, errorKey, index) in formNonFieldErrors"
          :key="errorKey + index"
          class="text-red-600 text-end text-sm"
        >
          <ul v-if="errorKey === 'non_field_errors'">
            <li v-for="(e, index) in error" :key="errorKey + 'Error' + index">{{ e }}</li>
          </ul>
          <div v-if="errorKey !== 'non_field_errors'">
            <p>{{ errorKey }} : {{ error }}</p>
          </div>
        </div>

        <!-- * SUBMIT -->
        <div class="space-y-2">
          <div>
            <button
              type="submit"
              :class="{ loading: isFormLoading ? true : false }"
              class="w-full btn btn-primary"
            >
              Log In
            </button>
          </div>
          <p class="px-6 text-sm text-center text-gray-600">
            Don't have an account yet?
            <a @click="app.currentView = 'signup'" class="btn btn-link btn-xs">Sign Up</a>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>
