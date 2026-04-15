import router from "./index"
import { useUserStore } from "@/store/user"
import { asyncRoutes } from "./dynamicRoutes"

let isRouteAdded = false

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  // 初始化权限
  if (!userStore.ready) {
    await userStore.initAuth()
  }

  const token = userStore.token

  // 未登录
  if (!token && to.path !== "/login") {
    return next("/login")
  }

  // 已登录访问 login
  if (token && to.path === "/login") {
    return next("/")
  }

  // ⭐ 动态路由注入（关键修复）
  if (!isRouteAdded && token) {
    const roles = userStore.roles ?? []   // ✅ 防御

    const accessRoutes = filterRoutes(asyncRoutes, roles)

    accessRoutes.forEach(r => router.addRoute(r))

    isRouteAdded = true

    return next({ ...to, replace: true })
  }

  next()
})

/**
 * 根据 roles 过滤路由（安全版）
 */
function filterRoutes(routes: any[], roles: string[] = []) {
  const safeRoles = roles ?? []

  return routes.filter(route => {
    const needRoles = route.meta?.roles

    // 没有限制 => 放行
    if (!needRoles || needRoles.length === 0) return true

    // 防止 some/includes 报错
    if (!Array.isArray(needRoles)) return true

    return needRoles.some((r: string) => safeRoles.includes(r))
  })
}