<template>
  <nav class="app-nav">
    <router-link class="brand" to="/">
      <span class="brand-mark">B</span>
      <span>Booking Lite</span>
    </router-link>

    <div class="nav-links">
      <router-link class="nav-link" to="/">Overview</router-link>
      <router-link v-if="userStore.isLoggedIn" class="nav-link" to="/admin">Admin</router-link>
      <router-link v-if="userStore.isLoggedIn" class="nav-link" to="/admin/room">Rooms</router-link>
      <router-link v-if="userStore.isLoggedIn" class="nav-link" to="/admin/order">Orders</router-link>
      <router-link v-if="userStore.isLoggedIn" class="nav-link" to="/admin/user">Users</router-link>
    </div>

    <router-link v-if="!userStore.isLoggedIn" class="nav-link active" to="/login">
      Login
    </router-link>

    <button v-else class="button-ghost" @click="handleCheckout">
      Sign out
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";

const userStore = useUserStore();
const router = useRouter();

const handleCheckout = async () => {
  userStore.logout();
  await router.push("/");
};
</script>
