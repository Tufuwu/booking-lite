<template>
  <section class="card">
    <p class="eyebrow">预订日历占位</p>
    <h3>等待订单接口开放</h3>
    <ul class="calendar-strip">
      <li v-for="(day, index) in nextSevenDays" :key="index">
        {{ day }}
      </li>
    </ul>
  </section>
</template>

<script setup>
import { computed } from "vue";

// 计算未来 7 天的日期字符串
const nextSevenDays = computed(() => {
  const today = new Date();
  return Array.from({ length: 7 }, (_, index) => {
    const value = new Date(today);
    value.setDate(today.getDate() + index);
    return value.toLocaleDateString("zh-CN", { 
      month: "numeric", 
      day: "numeric" 
    });
  });
});
</script>

<style scoped>
.calendar-strip {
  display: flex;
  list-style: none;
  padding: 0;
  gap: 10px;
}
.calendar-strip li {
  padding: 8px;
  background: #f4f4f4;
  border-radius: 4px;
}
</style>