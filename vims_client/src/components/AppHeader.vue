<script setup>
import IconMenu from './icons/IconMenu.vue'
</script>
<template>
  <header class="container mx-auto navbar py-2 bg-base-100 rounded-lg shadow-lg z-10">
    <div class="flex-1">
      <a class="btn btn-ghost normal-case text-xl">VIMSearch</a>
    </div>
    <div class="flex-none">
      <!-- * NAVBAR ACTIONS -->
      <ul class="menu menu-horizontal px-1">
        <li><a>Search</a></li>
        <li><a>My Images</a></li>
        <!-- Authentication -->
        <li><a>Log In</a></li>
        <li><a class="font-bold text-purple-700">Sign Up</a></li>
      </ul>

      <!-- * PROFILE -->
      <div class="dropdown dropdown-end">
        <label tabindex="0" class="btn btn-ghost">
          <h2>Ruben Caballero</h2>
        </label>
        <ul
          tabindex="0"
          class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
        >
          <li><a>Log Out</a></li>
        </ul>
      </div>


      <!-- * MOBILE LAYOUT -->
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-circle">
            <IconMenu />
          </label>
          <ul
            tabindex="0"
            class="menu menu-compact dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52"
          >
            <li><a>Search</a></li>
            <li><a>My Images</a></li>
            <!-- Authentication -->
            <li><a>Log In</a></li>
            <li><a class="font-bold text-purple-700">Sign Up</a></li>
            <li><a class="font-bold text-purple-700">Log Out</a></li>
          </ul>
        </div>
    </div>
  </header>
</template>
