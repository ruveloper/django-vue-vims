<script setup>
import { onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import SearchView from './components/SearchView.vue'
import LoginView from './components/LoginView.vue'
import SignupView from './components/SignupView.vue'
import ProfileView from './components/ProfileView.vue'
import { useAppStore } from './stores/app'
import { useServiceStore } from './stores/service'

// * Stores
const app = useAppStore()
const service = useServiceStore()

onMounted(() => {
  app.getTokenFromCookies()
  service.initReCatpcha()
})
</script>

<template>
  <div class="relative">
    <div class="fixed inset-x-0 top-3 z-10">
      <AppHeader />
    </div>
  </div>

  <main class="z-0">
    <!-- * VIEWS -->
    <!-- The search view should live forever, as mounting it is a high-cost process,
          so it only hides when the view changes. -->
    <SearchView :class="{ hidden: app.currentView !== 'search' }" />
    <LoginView v-if="app.currentView === 'login' && app.userToken === ''" />
    <SignupView v-if="app.currentView === 'signup' && app.userToken === ''" />
    <ProfileView v-if="app.currentView === 'profile' && app.userToken !== ''" />
  </main>
</template>

<style scoped></style>
