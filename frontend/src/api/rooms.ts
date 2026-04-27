import http from "./http";
import type { RoomCreatePayload, RoomResponse, RoomUpdatePayload } from "../types.js";

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
export async function deleteRoom(roomNumber: string): Promise<void> {
  await http.delete(`/admins/room/${roomNumber}`);
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

/**
 * 查询全部房间
 */
export async function getAllRooms(): Promise<RoomResponse[]> {
  const res = await http.get<RoomResponse[]>("/admins/room/all");
  return res.data;
}
