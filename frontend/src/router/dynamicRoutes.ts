export const asyncRoutes = [
  {
    path: "/admin",
    name: "Admin",
    component: () => import("@/pages/Admin.vue"),
    meta: { roles: ["admin"] },
  },
  {
    path: "/admin/user",
    name: "UserManage",
    component: () => import("@/pages/UserManage.vue"),
    meta: { roles: ["admin"] },
  },
  {
    path: "/admin/room",
    name: "RoomManage",
    component: () => import("@/pages/RoomManage.vue"),
    meta: { roles: ["admin"] },
  },
  {
    path: "/admin/order",
    name: "OrderManage",
    component: () => import("@/pages/OrderManage.vue"),
    meta: { roles: ["admin", "staff"] },
  },
  {
    path: "/guest",
    name: "Guest",
    component: () => import("@/pages/Guest.vue"),
    meta: { roles: ["guest"] },
  },
];
