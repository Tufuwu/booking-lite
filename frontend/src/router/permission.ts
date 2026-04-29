import router from "./index";
import { useUserStore } from "@/store/user";
import { asyncRoutes } from "./dynamicRoutes";

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();

  if (!userStore.ready) {
    await userStore.initAuth();
  }

  const token = userStore.token;
  const roles = userStore.roles ?? [];

  if (!token && to.path !== "/login") {
    return next("/login");
  }

  if (token && to.path === "/login") {
    return next(getRoleHome(roles));
  }

  if (token && ensureAccessRoutes(roles)) {
    return next({ ...to, replace: true });
  }

  if (token && isProtectedPath(to.path) && !canAccess(to, roles)) {
    return next(getRoleHome(roles));
  }

  next();
});

function filterRoutes(routes: any[], roles: string[] = []) {
  return routes.filter((route) => {
    const needRoles = route.meta?.roles;

    if (!needRoles || needRoles.length === 0) return true;
    if (!Array.isArray(needRoles)) return true;

    return needRoles.some((role: string) => roles.includes(role));
  });
}

function ensureAccessRoutes(roles: string[] = []) {
  let hasAddedRoute = false;
  const accessRoutes = filterRoutes(asyncRoutes, roles);

  accessRoutes.forEach((route) => {
    if (route.name && !router.hasRoute(route.name)) {
      router.addRoute(route);
      hasAddedRoute = true;
    }
  });

  return hasAddedRoute;
}

function canAccess(to: any, roles: string[] = []) {
  const matchedRoutes = to.matched ?? [];

  if (matchedRoutes.length === 0) {
    return !isProtectedPath(to.path);
  }

  return matchedRoutes.every((route: any) => {
    const needRoles = route.meta?.roles;

    if (!needRoles || needRoles.length === 0) return true;
    if (!Array.isArray(needRoles)) return true;

    return needRoles.some((role: string) => roles.includes(role));
  });
}

function isProtectedPath(path: string) {
  return path.startsWith("/admin") || path.startsWith("/guest");
}

function getRoleHome(roles: string[] = []) {
  if (roles.includes("admin")) return "/admin";
  if (roles.includes("staff")) return "/admin/order";
  if (roles.includes("guest")) return "/guest";
  return "/";
}
