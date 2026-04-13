interface RoomCardProps {
  title: string;
  detail: string;
  highlight: string;
}

export function renderRoomCard({ title, detail, highlight }: RoomCardProps): string {
  return `
    <article class="card card-room">
      <p class="eyebrow">${highlight}</p>
      <h3>${title}</h3>
      <p class="muted">${detail}</p>
    </article>
  `;
}
