<script setup>
import { useAppStore } from '../stores/app'
import IconMenu from './icons/IconMenu.vue'

// * Stores
const app = useAppStore()
</script>
<template>
  <header class="container h-10 mx-auto navbar py-2 bg-base-100 rounded-lg shadow-lg z-10">
    <div class="flex-1">
      <a @click="app.currentView = 'search'" class="h-10 cursor-pointer">
        <img class="h-full" src="@/assets/img/logo_name_xs.jpg" alt="vims logo" />
      </a>
    </div>
    <div class="flex-none">
      <!-- * ----------------------- DESKTOP NAVBAR LAYOUT ----------------------- -->
      <div class="hidden md:block">
        <!-- * NAVBAR ACTIONS -->
        <ul class="menu menu-horizontal px-1">
          <li><a @click="app.currentView = 'search'">Search</a></li>
          <div v-if="app.userToken === ''" class="flex flex-row">
            <li><a @click="app.currentView = 'login'">Log In</a></li>
            <li>
              <a
                @click="app.currentView = 'signup'"
                class="font-bold text-purple-700 active:text-white"
                >Sign Up</a
              >
            </li>
          </div>
        </ul>

        <!-- * PROFILE -->
        <div v-if="app.userToken !== ''" class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost">
            <h2>{{ app.userData.username }}</h2>
          </label>
          <ul
            tabindex="0"
            class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
          >
            <li><a @click="app.currentView = 'profile'">My Images</a></li>
            <li><a @click="app.logout">Log Out</a></li>
          </ul>
        </div>
      </div>

      <!-- * ----------------------- MOBILE NAVBAR LAYOUT ----------------------- -->
      <div class="dropdown dropdown-end md:hidden">
        <label tabindex="0" class="btn btn-ghost btn-circle">
          <IconMenu />
        </label>
        <ul
          tabindex="0"
          class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
        >
          <li><a @click="app.currentView = 'search'">Search</a></li>
          <!-- Authentication -->
          <div v-if="app.userToken === ''">
            <li><a @click="app.currentView = 'login'">Log In</a></li>
            <li>
              <a
                @click="app.currentView = 'signup'"
                class="font-bold text-purple-700 active:text-white"
                >Sign Up</a
              >
            </li>
          </div>
          <div v-if="app.userToken !== ''" class="mt-3">
            <h2 class="text-center">{{ app.userData.username }}</h2>
            <hr />
            <li><a @click="app.currentView = 'profile'">My Images</a></li>
            <li><a @click="app.logout">Log Out</a></li>
          </div>
        </ul>
      </div>
    </div>
  </header>
</template>
