<template>
  <div class="login-page">
    <section class="hero">
      <p class="eyebrow">Staff access</p>
      <h1>Welcome back</h1>
      <p>Sign in to continue managing rooms, staff accounts, and operational tasks.</p>
    </section>

    <section class="card login-card">
      <p class="eyebrow">Secure login</p>
      <h2>Console access</h2>
      <form class="form-stack" @submit.prevent="handleLogin">
        <label>
          <span>Username</span>
          <input v-model="loginForm.username" autocomplete="username" placeholder="Enter username" required />
        </label>

        <label>
          <span>Password</span>
          <input
            v-model="loginForm.password"
            autocomplete="current-password"
            type="password"
            placeholder="Enter password"
            required
          />
        </label>

        <button type="submit">Login</button>
        <p class="feedback">{{ feedback }}</p>
      </form>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";
import type { LoginPayload } from "@/types";

const userStore = useUserStore();
const router = useRouter();
const feedback = ref("");

const loginForm = ref<LoginPayload>({
  username: "",
  password: "",
});

const roleHomeMap: Record<string, string> = {
  admin: "/admin",
  staff: "/admin/order",
  guest: "/guest",
};

async function handleLogin() {
  feedback.value = "";

  const success = await userStore.login(
    loginForm.value.username,
    loginForm.value.password,
  );

  if (success) {
    const role = userStore.roles[0] ?? userStore.role;
    await router.push(roleHomeMap[role] ?? "/");
    return;
  }

  feedback.value = "Login failed. Please check the username and password.";
}
</script>
