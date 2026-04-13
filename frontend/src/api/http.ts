import type { ApiErrorShape } from "../types.js";

const BASE_URL = "http://127.0.0.1:8000";

export class HttpError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "HttpError";
    this.status = status;
  }
}

type RequestOptions = {
  method?: "GET" | "POST" | "DELETE";
  body?: BodyInit | null;
  headers?: HeadersInit;
};

function resolveMessage(payload: unknown, fallback: string): string {
  if (!payload || typeof payload !== "object") {
    return fallback;
  }

  const typed = payload as ApiErrorShape;
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

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const requestInit: RequestInit = {
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

  return payload as T;
}

export function createFormBody(values: Record<string, string>): URLSearchParams {
  const body = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) {
    body.set(key, value);
  }
  return body;
}
