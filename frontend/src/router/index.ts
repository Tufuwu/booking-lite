import { createRouter, createWebHashHistory } from 'vue-router';
import Home from "../pages/Home.vue";
import Login from "../pages/Login.vue";
import Admin from "../pages/Admin.vue";
import RoomList from "../pages/RoomList.vue";
import Booking from "../pages/Booking.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/rooms", component: RoomList },
  { path: "/booking", component: Booking },
  { path: "/admin", component: Admin },
];

const router = createRouter({
  history: createWebHashHistory(), // 保持和你原来 hash 路由一致
  routes,
});

export default router;