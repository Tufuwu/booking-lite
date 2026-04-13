export type AdminRole = "admin";

export type RouteKey = "home" | "login" | "rooms" | "booking" | "admin";

export interface SessionUser {
  jobNumber: string;
  role: AdminRole;
  loggedInAt: string;
}

export interface AdminCreatePayload {
  job_number: string;
  name: string;
  password: string;
}

export interface RoomTypeOption {
  value: "single" | "twin" | "family";
  label: string;
}

export interface RoomCreatePayload {
  room_number: string;
  type_: "single" | "twin" | "family";
  price: string;
}

export interface ApiErrorShape {
  detail?: string | { msg?: string };
  msg?: string;
}
