<template>
  <section class="card">
    <p class="eyebrow">Booking Placeholder</p>
    <h2>Booking, check-in, and payment APIs are still pending</h2>
    <p class="muted">{{ info }}</p>
    <p class="note">
      The backend already has an Order model, but it does not expose create-order, list-order, or payment-status routes yet, so this page is intentionally a shell for the next step.
    </p>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { bookingStore } from "@/store/bookingStore"; // 假设你使用了 Pinia

const store = bookingStore;

import { ref, reactive, computed } from "vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";
import { createAdmin, deleteCurrentAdmin, logoutAdmin, updateAdmin } from "@/api/auth";

import type { UserCreatePayload, RoomCreatePayload } from "@/types";

const userStore = useUserStore();
const router = useRouter();
// 反馈信息状态
const sessionFeedback = ref("");
const deleteFeedback = ref("");
const roomFeedback = ref("");

// 表单数据绑定
const deleteForm = reactive({ password: "" });
const userForm = reactive<UserCreatePayload>({ name: "", phone_number: "", identity_number: "", type_: "guest", password: "" });
const roomForm = reactive<RoomCreatePayload>({ room_number: "", type_: "single", price: "" });
const adminUpdateForm = reactive({ name: "", password: "" });
// 处理逻辑

const moveToRoomAdmin = () => {
  router.push("/admin/rooms");
};
const moveToAdmin = () => {
  router.push("/admin");
};
const moveToOrderAdmin = () => {
  router.push("/admin/order");
};
</script>

<style scoped>
/* 可以在这里直接添加你的样式 */
.card { padding: 20px; border: 1px solid #ccc; }
.eyebrow { color: #888; text-transform: uppercase; }
.muted { color: #666; }
.note { font-size: 0.9em; font-style: italic; }
</style>