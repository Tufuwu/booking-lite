import http from "./http";
import type { UserCreatePayload, UserResponse } from "@/types";

/**
 * 创建用户
 */
export async function createUser(
  payload: UserCreatePayload
): Promise<UserResponse> {
  const res = await http.post<UserResponse>("/users", payload);
  return res.data;
}


export async function getAllUsers():Promise<UserResponse[]> {
  const res = await http.get<UserResponse[]>("/admins/user/all");
  return res.data;
}
