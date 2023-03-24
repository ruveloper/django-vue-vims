<script setup>
import { ref } from 'vue'
import { useAppStore } from '../stores/app'
import { useServiceStore } from '../stores/service'
import DefaultModal from './common/DefaultModal.vue'

// * Stores
const service = useServiceStore()
const app = useAppStore()

const form = ref({})
const formErrors = ref({})
const formNonFieldErrors = ref({})
const isFormLoading = ref(false)

const showModal = ref(false)

async function handleSignUpSubmit() {
  isFormLoading.value = true

  // * Get reCaptcha Token
  const reCaptchaToken = await service.getReCaptchaToken('signup')
  form.value['g-recaptcha-response'] = reCaptchaToken

  // * Register
  const response = await app.signup(form.value)
  // If errors
  if (response.status === 400) {
    formErrors.value = response.data

    // Set non-field errors
    const excludedKeys = ['email', 'username', 'password', 'password2']
    formNonFieldErrors.value = Object.keys(formErrors.value)
      .filter((key) => !excludedKeys.includes(key))
      .reduce((obj, key) => {
        obj[key] = formErrors.value[key]
        return obj
      }, {})

    isFormLoading.value = false
    return
  }
  // If Success
  if (response.status === 200 && app.userToken !== '') {
    showModal.value = true
  }

  // * Reset Form
  isFormLoading.value = false
  form.value = {}
}

function closeModal() {
  showModal.value = false
  app.currentView = 'search'
}
</script>

<template>
  <div class="min-w-screen min-h-screen pt-20 flex justify-center items-center bg-gray-500">
    <div class="w-96 my-10 flex flex-col max-w-md p-6 rounded-md sm:px-10 bg-gray-50 text-gray-800">
      <div class="mb-8 text-center">
        <h1 class="my-3 text-4xl font-bold">Sign Up</h1>
        <p class="text-sm text-gray-600">Create an account to store your favorites images</p>
      </div>

      <form @submit.prevent="handleSignUpSubmit" novalidate="true" action="" class="space-y-12">
        <!-- * FORM FIELDS -->
        <div class="space-y-4">
          <div>
            <label for="email" class="block mb-2 text-sm">Email address</label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder="your.name@mail.com"
              v-model.trim="form.email"
              class="w-full px-3 py-2 border rounded-md border-gray-300 bg-gray-50 text-gray-800"
            />
            <div v-if="'email' in formErrors" class="text-red-600 text-end text-sm">
              <p v-for="(error, index) in formErrors.email" :key="'emailError' + index">
                {{ error }}
              </p>
            </div>
          </div>
          <div>
            <label for="username" class="block mb-2 text-sm">Username</label>
            <input
              type="username"
              name="username"
              id="username"
              placeholder="yourname"
              v-model.trim="form.username"
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
              v-model.trim="form.password"
              class="w-full px-3 py-2 border rounded-md border-gray-300 bg-gray-50 text-gray-800"
            />
            <div v-if="'password' in formErrors" class="text-red-600 text-end text-sm">
              <p v-for="(error, index) in formErrors.password" :key="'passwordError' + index">
                {{ error }}
              </p>
            </div>
          </div>
          <div>
            <label for="password2" class="text-sm">Confirm Password</label>
            <input
              type="password"
              name="password2"
              id="password2"
              placeholder="*****"
              v-model.trim="form.password2"
              class="w-full px-3 py-2 border rounded-md border-gray-300 bg-gray-50 text-gray-800"
            />
            <div v-if="'password2' in formErrors" class="text-red-600 text-end text-sm">
              <p v-for="(error, index) in formErrors.password2" :key="'password2Error' + index">
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
              Sign Up
            </button>
          </div>
          <p class="px-6 text-sm text-center text-gray-600">
            You have an account?
            <a @click="app.currentView = 'login'" class="btn btn-link btn-xs">Log In</a>
          </p>
        </div>
      </form>
    </div>
  </div>

  <!-- * SUCCESS REGISTER MODAL -->
  <Teleport to="body">
    <DefaultModal :show="showModal" @close="closeModal">
      <template #header>
        <h3>Success!</h3>
      </template>
      <template #body>
        <p>Your account has been created.</p>
      </template>
    </DefaultModal>
  </Teleport>
</template>
