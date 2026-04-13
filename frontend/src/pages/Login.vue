<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "../store/user";

const username = ref("");
const userStore = useUserStore();

function handleLogin() {
  userStore.login(username.value);
}
</script>