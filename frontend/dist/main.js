import { renderNavbar } from "./components/Navbar/index.js";
import { getCurrentRoute } from "./router/index.js";
import { userStore } from "./store/userStore.js";
import { renderHomePage } from "./pages/Home/index.js";
import { bindLoginPage, renderLoginPage } from "./pages/Login/index.js";
import { bindAdminPage, renderAdminPage } from "./pages/Admin/index.js";
import { renderRoomListPage } from "./pages/RoomList/index.js";
import { renderBookingPage } from "./pages/Booking/index.js";
const app = document.querySelector("#app");
if (!app) {
    throw new Error("Missing #app root element");
}
const root = app;
function render() {
    const route = getCurrentRoute();
    const page = resolvePage(route);
    root.innerHTML = `
    <div class="shell">
      ${renderNavbar(route)}
      <main class="page">${page}</main>
    </div>
  `;
    bindPage(route);
}
function resolvePage(route) {
    switch (route) {
        case "login":
            return renderLoginPage();
        case "rooms":
            return renderRoomListPage();
        case "booking":
            return renderBookingPage();
        case "admin":
            return renderAdminPage();
        case "home":
        default:
            return renderHomePage();
    }
}
function bindPage(route) {
    switch (route) {
        case "login":
            bindLoginPage();
            break;
        case "admin":
            bindAdminPage();
            break;
        default:
            break;
    }
}
window.addEventListener("hashchange", render);
userStore.subscribe(render);
if (!window.location.hash) {
    window.location.hash = "#/";
}
else {
    render();
}
//# sourceMappingURL=main.js.map