import http from "./http";
import type { OrderCreatePayload } from "./order";
import type {
  OrderResponse,
  RoomResponse,
  UserCreatePayload,
  UserResponse,
} from "@/types";

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

export async function getCurrentUserOrders(): Promise<OrderResponse[]> {
  const res = await http.get<OrderResponse[]>("/user/orders");
  return res.data;
}

export async function createCurrentUserOrder(
  payload: OrderCreatePayload,
): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>("/user/orders", payload);
  return res.data;
}

export async function getCurrentUserRooms(): Promise<RoomResponse[]> {
  const res = await http.get<RoomResponse[]>("/user/rooms");
  return res.data;
}

export async function confirmCurrentUserOrder(
  orderId: number,
): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/user/orders/${orderId}/confirm`);
  return res.data;
}
