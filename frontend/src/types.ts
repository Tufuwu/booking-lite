export type UserRole = "admin" | "staff" | "guest";
export type AdminRole = "admin";

export type RouteKey = "home" | "login" | "rooms" | "booking" | "admin";

export interface SessionUser {
  jobNumber: string;
  role: AdminRole;
  loggedInAt: string;
}

export interface UserCreatePayload {
  name: string;
  phone_number: string;
  identity_number: string;
  type_: UserRole;
  password: string;
}

export type AdminCreatePayload = UserCreatePayload;

export interface AdminUpdatePayload {
  name?: string;
  password?: string;
}

export interface RoomTypeOption {
  value: "single" | "twin" | "family";
  label: string;
}

export interface RoomCreatePayload {
  room_number: string;
  type_: RoomTypeOption["value"];
  price: string;
}

export interface RoomUpdatePayload {
  room_number: string;
  type_?: RoomTypeOption["value"];
  price?: string;
}

export interface ApiErrorShape {
  detail?: string | { msg?: string };
  msg?: string;
}

export interface LoginPayload {
  username: string;
  password: string;
}

export interface RoomResponse {
  id: number;
  room_number: string;
  type_: string;
  price: number | string;
  room_status?: string;
}
