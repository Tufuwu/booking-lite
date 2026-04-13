<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" />
      
      <input v-model="password" type="password" placeholder="Password" />
      
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";

const username = ref("");
const password = ref(""); // 新增变量
const userStore = useUserStore();
const router = useRouter();

async function handleLogin() {
  const success = await userStore.login(
    username.value,
    password.value
  );

  if (success) {
    console.log("登录成功:");
    router.push("/admin"); // ✅ 登录成功跳转
  }
}
</script>