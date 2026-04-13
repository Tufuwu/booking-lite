<div class="shell">
  navbar
  <main>page</main>
</div>


<template>
  <div class="shell">
    <Navbar />
    <main class="page">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Navbar from "./components/Navbar.vue";
</script>