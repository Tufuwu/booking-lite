export const asyncRoutes = [
  {
    path: "/admin",
    name: "Admin", // ✅ 必须加
    component: () => import("@/pages/Admin.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/users",
    component: () => import("@/pages/User.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/admin/room",
    component: () => import("@/pages/RoomManage.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/admin/orders",
    component: () => import("@/pages/OrderManage.vue"),
    meta: { roles: ["admin", "staff"] }
  }
]