<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="loginForm.username" placeholder="Username" />
      
      <input v-model="loginForm.password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";
import type { LoginPayload } from "@/types";


const userStore = useUserStore();
const router = useRouter();

const loginForm = ref<LoginPayload>({
  username: "",
  password: ""
});

async function handleLogin() {


  const success = await userStore.login(
    loginForm.value.username,
    loginForm.value.password
  );

  if (success) {
    router.push("/admin");
  }
}
</script>