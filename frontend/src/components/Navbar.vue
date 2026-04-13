<template>
  <nav>
    <router-link to="/">Home</router-link>

    <router-link v-if="!userStore.isLoggedIn" to="/login">
      Login
    </router-link>

    <button v-else @click="handleCheckout">
      Checkout
    </button>
  </nav>
</template>

<script setup>
import { useUserStore } from "@/store/user";
import { logoutAdmin } from "@/api/auth.ts";
import { useRouter } from "vue-router";
const userStore = useUserStore();
const router = useRouter();

const handleCheckout = async () => {
  // 这里写你的 checkout 逻辑
  try {
    await logoutAdmin();

    userStore.logout();

    router.push("/");
  } catch (e) { sessionFeedback.value = e.message; }
  // await userStore.fetchMe(); // ⭐同步状态
};
</script>