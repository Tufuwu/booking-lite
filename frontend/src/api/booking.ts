import { request } from "./http.js";
import type { RoomCreatePayload } from "../types.js";

interface RoomResponse {
  id: number;
  room_number: string;
  type_: string;
  price: number;
}

export async function createRoom(payload: RoomCreatePayload): Promise<RoomResponse> {
  return request<RoomResponse>("/admins/room/", {
    method: "POST",
    body: JSON.stringify({
      ...payload,
      price: Number(payload.price),
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
}
