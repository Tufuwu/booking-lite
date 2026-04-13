import { renderCalendarPlaceholder } from "../../components/Calendar/index.js";
import { renderRoomCard } from "../../components/RoomCard/index.js";
export function renderHomePage() {
    return `
    <section class="hero card">
      <div>
        <p class="eyebrow">Backend Features Ready</p>
        <h2>Admin login, admin creation, logout, self delete, and room creation</h2>
        <p class="muted">
          This frontend is scoped to the routes the backend already exposes. Booking and order pages are kept as integration placeholders until those APIs are added.
        </p>
      </div>
    </section>

    <section class="grid grid-3">
      ${renderRoomCard({
        title: "Admin session login",
        detail: "Maps to POST /admin/login and sends cookies automatically.",
        highlight: "Auth",
    })}
      ${renderRoomCard({
        title: "Create admin",
        detail: "Maps to POST /admins/ for bootstrapping back-office accounts.",
        highlight: "Admin",
    })}
      ${renderRoomCard({
        title: "Create room",
        detail: "Maps to POST /admins/room/ with single, twin, and family types.",
        highlight: "Room",
    })}
    </section>

    ${renderCalendarPlaceholder()}
  `;
}
//# sourceMappingURL=index.js.map