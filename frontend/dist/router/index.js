const routeMap = {
    "#/": "home",
    "#/login": "login",
    "#/rooms": "rooms",
    "#/booking": "booking",
    "#/admin": "admin",
};
export function getCurrentRoute() {
    return routeMap[window.location.hash] ?? "home";
}
export function navigate(route) {
    const target = Object.entries(routeMap).find(([, value]) => value === route)?.[0] ?? "#/";
    if (window.location.hash === target) {
        window.dispatchEvent(new HashChangeEvent("hashchange"));
        return;
    }
    window.location.hash = target;
}
//# sourceMappingURL=index.js.map