import http from "./http";
import type {
  AdminCreatePayload,
  SessionUser,
  AdminUpdatePayload,
} from "../types.js";

interface AdminResponse {
  id: number;
  job_number: string;
  name: string;
}

/**
 * 登录
 */
export async function loginAdmin(
  username: string,
  password: string
): Promise<SessionUser> {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  // 1. 登录接口（返回 JWT）
  const loginRes = await http.post("/admin/login", params);

  const token = loginRes.data.access_token;

  // 2. 保存 token（如果你 http.ts 没做这一步）
  localStorage.setItem("token", token);

  // 3. 获取当前用户信息（http 自动带 token）
  const res = await http.get("/admins/me");

  return res.data;
}

/**
 * 创建管理员
 */
export async function createAdmin(
  payload: AdminCreatePayload
): Promise<AdminResponse> {
  const res = await http.post<AdminResponse>("/admins/", payload);
  return res.data;
}

/**
 * 登出
 */
export async function logoutAdmin(): Promise<void> {
  // 可选：通知后端（如果后端做 blacklist）
  await http.post("/admins/logout");

  // 清理本地 token
  localStorage.removeItem("token");
}

/**
 * 更新管理员
 */
export async function updateAdmin(
  payload: AdminUpdatePayload
): Promise<AdminResponse> {
  const res = await http.patch<AdminResponse>("/admins/update", payload);

  // ❌ JWT模式不需要自动 logout
  return res.data;
}

/**
 * 删除当前管理员
 */
export async function deleteCurrentAdmin(password: string): Promise<void> {
  await http.delete("/admins/", {
    data: { password },
  });
}