<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">Order management</p>
      <h1>Orders workspace</h1>
      <p class="muted">Booking, check-in, and payment endpoints can plug into this workspace next.</p>
    </section>

    <section class="metric-row">
      <article class="metric-card">
        <span class="muted">Today</span>
        <strong>--</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Pending</span>
        <strong>--</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Checked in</span>
        <strong>--</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Revenue</span>
        <strong>--</strong>
      </article>
    </section>

    <section class="card empty-panel">
      <p class="eyebrow">API pending</p>
      <h2>Order table</h2>
      <p class="muted">Once the backend exposes order routes, this area can become a searchable booking table.</p>
    </section>
  </div>
</template>

<script setup lang="ts"></script>
