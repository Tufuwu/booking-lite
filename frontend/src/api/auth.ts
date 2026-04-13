import { createFormBody, request } from "./http.js";
import type { AdminCreatePayload, SessionUser, AdminUpdatePayload } from "../types.js";
import axios from "axios";

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
  const res = await axios.post<AdminResponse>("/admins/", payload);
  return res.data;
}

export async function logoutAdmin(): Promise<void> {
  await axios.post("/api/admins/logout");
}

export async function updateAdmin(payload: AdminUpdatePayload): Promise<AdminResponse> {
  const res = await axios.patch<AdminResponse>("/api/admins/update", payload);
  await axios.post("/api/admins/logout");
  return res.data;
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
