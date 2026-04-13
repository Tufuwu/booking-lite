export function renderCalendarPlaceholder() {
    const today = new Date();
    const days = Array.from({ length: 7 }, (_, index) => {
        const value = new Date(today);
        value.setDate(today.getDate() + index);
        return `<li>${value.toLocaleDateString("zh-CN", { month: "numeric", day: "numeric" })}</li>`;
    }).join("");
    return `
    <section class="card">
      <p class="eyebrow">预订日历占位</p>
      <h3>等待订单接口开放</h3>
      <ul class="calendar-strip">${days}</ul>
    </section>
  `;
}
//# sourceMappingURL=index.js.map