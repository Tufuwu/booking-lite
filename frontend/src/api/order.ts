import http from "./http";
import type { OrderResponse, OrderStatus } from "@/types";

export interface OrderCreatePayload {
  name: string;
  phone_number: string;
  room_number: string;
  stay_length: number;
}

export interface OrderExtendPayload {
  extra_days: number;
}

export interface OrderListParams {
  user_id?: number;
  status?: OrderStatus | "";
}

function buildListParams(params: OrderListParams = {}) {
  const query: Record<string, number | string> = {};

  if (params.user_id !== undefined) {
    query.user_id = params.user_id;
  }

  if (params.status) {
    query.status = params.status;
  }

  return query;
}

export async function createOrder(payload: OrderCreatePayload): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>("/orders", payload);
  return res.data;
}

export async function getOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.get<OrderResponse>(`/orders/${orderId}`);
  return res.data;
}

export async function listOrders(params: OrderListParams = {}): Promise<OrderResponse[]> {
  const res = await http.get<OrderResponse[]>("/orders", {
    params: buildListParams(params),
  });
  return res.data;
}

export async function confirmOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/confirm`);
  return res.data;
}

export async function checkInOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/check-in`);
  return res.data;
}

export async function checkOutOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/check-out`);
  return res.data;
}

export async function cancelOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/cancel`);
  return res.data;
}

export async function refundOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/refund`);
  return res.data;
}

export async function extendOrder(
  orderId: number,
  payload: OrderExtendPayload,
): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/extend`, payload);
  return res.data;
}

export async function recalculateOrder(orderId: number): Promise<OrderResponse> {
  const res = await http.post<OrderResponse>(`/orders/${orderId}/recalculate`);
  return res.data;
}
