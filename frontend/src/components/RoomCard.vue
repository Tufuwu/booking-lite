<template>
  <div class="room-card">
    <span class="highlight">{{ highlight }}</span>
    <h3>{{ title }}</h3>
    <p>{{ detail }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  detail: String,
  highlight: String
});
</script>