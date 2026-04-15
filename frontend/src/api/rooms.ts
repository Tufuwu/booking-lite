import http from "./http";
import type { RoomCreatePayload, RoomUpdatePayload } from "../types.js";

interface RoomResponse {
  id: number;
  room_number: string;
  type_: string;
  price: number;
}

/**
 * 创建房间
 */
export async function createRoom(
  payload: RoomCreatePayload
): Promise<RoomResponse> {
  const res = await http.post<RoomResponse>("/admins/room/", payload);
  return res.data;
}

/**
 * 删除房间
 */
export async function deleteRoom(roomId: number): Promise<void> {
  await http.delete(`/admins/room/${roomId}`);
}

/**
 * 更新房间
 */
export async function updateRoom(
  payload: RoomUpdatePayload
): Promise<RoomResponse[]> {
  const res = await http.patch<RoomResponse[]>("/admins/room/", payload);
  return res.data;
}