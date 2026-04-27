export const asyncRoutes = [
  {
    path: "/admin",
    name: "Admin", // ✅ 必须加
    component: () => import("@/pages/Admin.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/admin/user",
    component: () => import("@/pages/UserManage.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/admin/room",
    component: () => import("@/pages/RoomManage.vue"),
    meta: { roles: ["admin"] }
  },
  {
    path: "/admin/order",
    component: () => import("@/pages/OrderManage.vue"),
    meta: { roles: ["admin", "staff"] }
  }
]