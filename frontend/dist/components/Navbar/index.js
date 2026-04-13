import { userStore } from "../../store/userStore.js";
const links = [
    { route: "home", label: "首页" },
    { route: "login", label: "登录" },
    { route: "rooms", label: "房态接入位" },
    { route: "booking", label: "订单接入位" },
    { route: "admin", label: "管理后台" },
];
export function renderNavbar(activeRoute) {
    const session = userStore.getState();
    return `
    <header class="topbar">
      <div>
        <p class="eyebrow">Booking Lite</p>
        <h1>酒店管理前端</h1>
      </div>
      <nav class="nav">
        ${links
        .map((link) => `
              <a class="nav-link ${link.route === activeRoute ? "active" : ""}" href="${resolveHash(link.route)}">
                ${link.label}
              </a>
            `)
        .join("")}
      </nav>
      <div class="session-chip">${session ? `已登录：${session.jobNumber}` : "未登录"}</div>
    </header>
  `;
}
function resolveHash(route) {
    switch (route) {
        case "login":
            return "#/login";
        case "rooms":
            return "#/rooms";
        case "booking":
            return "#/booking";
        case "admin":
            return "#/admin";
        case "home":
        default:
            return "#/";
    }
}
//# sourceMappingURL=index.js.map