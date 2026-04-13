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

<script setup>
import { computed } from "vue";
import { bookingStore } from "@/store/bookingStore"; // 假设你使用了 Pinia

const store = bookingStore;

// 使用 computed 保证数据响应性
const info = computed(() => bookingStore.info);
</script>

<style scoped>
/* 可以在这里直接添加你的样式 */
.card { padding: 20px; border: 1px solid #ccc; }
.eyebrow { color: #888; text-transform: uppercase; }
.muted { color: #666; }
.note { font-size: 0.9em; font-style: italic; }
</style>