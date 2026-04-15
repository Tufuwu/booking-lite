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
    path: "/orders",
    component: () => import("@/pages/Order.vue"),
    meta: { roles: ["admin", "staff"] }
  }
]