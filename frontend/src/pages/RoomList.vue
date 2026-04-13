<template>
  <section class="card">
    <p class="eyebrow">Room Page Placeholder</p>
    <h2>Waiting for room query APIs</h2>
    <p class="muted">
      The backend currently exposes room creation only. Room list, room status filters, 
      and room detail endpoints are not available yet, so this page stays as a 
      ready-made integration slot.
    </p>
  </section>
</template>

<style scoped>
/* 将原本 CSS 中的样式直接放在这里。
   scoped 属性确保样式只作用于当前组件，不会污染全局。
*/
.card {
  padding: 1.5rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
}
.eyebrow {
  color: #666;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}
.muted {
  color: #888;
}
</style>