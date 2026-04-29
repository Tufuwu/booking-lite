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
  role: UserRole;
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

export type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "CHECKED_IN"
  | "COMPLETED"
  | "CANCELLED"
  | "CANCELLED_UNPAID"
  | "CANCELLED_PAID"
  | "REFUNDED";

export interface OrderResponse {
  id: number;
  user_id?: number;
  room_id?: number;
  check_in_time?: string;
  check_in_date?: string;
  check_out_date?: string;
  stay_length?: number;
  expense?: number;
  status?: OrderStatus | string;
  created_at?: string;
  updated_at?: string;
  user?: {
    id?: number;
    name?: string;
    phone_number?: string;
    identity_number?: string;
  };
  room?: {
    id?: number;
    room_number?: string;
    type_?: string;
    price?: number;
    room_status?: string;
  };
}

export interface UserResponse {
  id: number;
  name: string;
  phone_number: string;
  identity_number?: string;
  order?: OrderResponse[];
}
