import http from "./http";
import type { UserCreatePayload } from "../types.js";

interface UserResponse {
  id: number;
  name: string;
  phone_number: string;
  identity_number: string;
}

/**
 * 创建用户
 */
export async function createUser(
  payload: UserCreatePayload
): Promise<UserResponse> {
  const res = await http.post<UserResponse>("/admins/", payload);
  return res.data;
}
