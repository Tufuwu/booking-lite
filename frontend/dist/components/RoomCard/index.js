export function renderRoomCard({ title, detail, highlight }) {
    return `
    <article class="card card-room">
      <p class="eyebrow">${highlight}</p>
      <h3>${title}</h3>
      <p class="muted">${detail}</p>
    </article>
  `;
}
//# sourceMappingURL=index.js.map