import { createFormBody, request } from "./http.js";
export async function loginAdmin(username, password) {
    await request("/admin/login", {
        method: "POST",
        body: createFormBody({
            username,
            password,
        }),
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });
    return {
        jobNumber: username,
        role: "admin",
        loggedInAt: new Date().toISOString(),
    };
}
export async function createAdmin(payload) {
    return request("/admins/", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
            "Content-Type": "application/json",
        },
    });
}
export async function logoutAdmin() {
    await request("/admins/logout", {
        method: "POST",
    });
}
export async function deleteCurrentAdmin(password) {
    await request("/admins/", {
        method: "DELETE",
        body: JSON.stringify({ password }),
        headers: {
            "Content-Type": "application/json",
        },
    });
}
//# sourceMappingURL=auth.js.map