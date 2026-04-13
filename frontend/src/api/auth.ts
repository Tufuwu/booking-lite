import { createFormBody, request } from "./http.js";
import type { AdminCreatePayload, SessionUser } from "../types.js";

interface LoginResponse {
  msg: string;
}

interface AdminResponse {
  id: number;
  job_number: string;
  name: string;
}

export async function loginAdmin(username: string, password: string): Promise<SessionUser> {
  await request<LoginResponse>("/admin/login", {
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

export async function createAdmin(payload: AdminCreatePayload): Promise<AdminResponse> {
  return request<AdminResponse>("/admins/", {
    method: "POST",
    body: JSON.stringify(payload),
    headers: {
      "Content-Type": "application/json",
    },
  });
}

export async function logoutAdmin(): Promise<void> {
  await request<void>("/admins/logout", {
    method: "POST",
  });
}

export async function deleteCurrentAdmin(password: string): Promise<void> {
  await request<void>("/admins/", {
    method: "DELETE",
    body: JSON.stringify({ password }),
    headers: {
      "Content-Type": "application/json",
    },
  });
}
