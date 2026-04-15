export const constantRoutes = [
  { path: "/login", component: () => import("@/pages/Login.vue") },
  { path: "/", component: () => import("@/pages/Home.vue") }
]