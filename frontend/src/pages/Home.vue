<template>
  <div class="home-page">
    <section class="hero">
      <p class="eyebrow">Hotel operations</p>
      <h1>Booking Lite</h1>
      <p>
        A focused workspace for front desk teams to manage rooms, guests, and orders with a cleaner daily flow.
      </p>
      <div class="button-row">
        <router-link class="nav-link active" :to="userStore.isLoggedIn ? '/admin' : '/login'">
          {{ userStore.isLoggedIn ? "Open Console" : "Staff Login" }}
        </router-link>
      </div>
    </section>

    <section class="metric-row">
      <article class="metric-card">
        <span class="muted">Room workflow</span>
        <strong>Fast</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Role access</span>
        <strong>Clear</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Order desk</span>
        <strong>Ready</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Guest records</span>
        <strong>Organized</strong>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/store/user";

const userStore = useUserStore();
</script>
