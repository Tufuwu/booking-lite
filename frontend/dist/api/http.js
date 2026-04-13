const BASE_URL = "http://127.0.0.1:8000";
export class HttpError extends Error {
    constructor(status, message) {
        super(message);
        this.name = "HttpError";
        this.status = status;
    }
}
function resolveMessage(payload, fallback) {
    if (!payload || typeof payload !== "object") {
        return fallback;
    }
    const typed = payload;
    if (typeof typed.detail === "string") {
        return typed.detail;
    }
    if (typed.detail && typeof typed.detail === "object" && typeof typed.detail.msg === "string") {
        return typed.detail.msg;
    }
    if (typeof typed.msg === "string") {
        return typed.msg;
    }
    return fallback;
}
export async function request(path, options = {}) {
    const requestInit = {
        method: options.method ?? "GET",
        body: options.body ?? null,
        credentials: "include",
    };
    if (options.headers) {
        requestInit.headers = options.headers;
    }
    const response = await fetch(`${BASE_URL}${path}`, requestInit);
    const contentType = response.headers.get("content-type") ?? "";
    const isJson = contentType.includes("application/json");
    const payload = isJson ? await response.json() : await response.text();
    if (!response.ok) {
        throw new HttpError(response.status, resolveMessage(payload, "请求失败，请稍后再试"));
    }
    return payload;
}
export function createFormBody(values) {
    const body = new URLSearchParams();
    for (const [key, value] of Object.entries(values)) {
        body.set(key, value);
    }
    return body;
}
//# sourceMappingURL=http.js.map