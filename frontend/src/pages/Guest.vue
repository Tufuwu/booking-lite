<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">Guest center</p>
      <h1>My bookings</h1>
      <p class="muted">Review available rooms and confirm your pending reservations.</p>
    </section>

    <section class="metric-row">
      <article class="metric-card">
        <span class="muted">My orders</span>
        <strong>{{ orders.length }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Pending</span>
        <strong>{{ countByStatus("PENDING") }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Confirmed</span>
        <strong>{{ countByStatus("CONFIRMED") }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Rooms</span>
        <strong>{{ rooms.length }}</strong>
      </article>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">New booking</p>
        <h2>Create order</h2>
        <form class="form-stack" @submit.prevent="handleCreateOrder">
          <div class="form-grid">
            <label>
              <span>Name</span>
              <input v-model="createForm.name" placeholder="Full name" required />
            </label>
            <label>
              <span>Phone number</span>
              <input v-model="createForm.phone_number" placeholder="Contact phone" required />
            </label>
            <label>
              <span>Room number</span>
              <input v-model="createForm.room_number" placeholder="Example: 1208" required />
            </label>
            <label>
              <span>Check in</span>
              <input
                v-model="createForm.check_in_date"
                type="date"
                :min="today"
                required
                @change="syncStayLength"
              />
            </label>
            <label>
              <span>Check out</span>
              <input
                v-model="createForm.check_out_date"
                type="date"
                :min="minCheckOutDate"
                required
                @change="syncStayLength"
              />
            </label>
            <label>
              <span>Stay length</span>
              <input v-model.number="createForm.stay_length" type="number" min="1" readonly required />
            </label>
          </div>
          <button type="submit" :disabled="isCreatingOrder">Create order</button>
          <p class="feedback">{{ createFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <div class="table-header">
          <div>
            <p class="eyebrow">Rooms</p>
            <h2>Available inventory</h2>
          </div>
          <button type="button" class="button-ghost" :disabled="isLoadingRooms" @click="handleLoadRooms">
            Refresh
          </button>
        </div>

        <p class="feedback">{{ roomFeedback }}</p>

        <div v-if="isLoadingRooms" class="empty-panel">
          <p class="muted">Loading rooms...</p>
        </div>

        <div v-else-if="rooms.length === 0" class="empty-panel">
          <p class="muted">No rooms found.</p>
        </div>

        <div v-else class="data-table">
          <div class="data-row data-row-head">
            <span>Room</span>
            <span>Type</span>
            <span>Price</span>
            <span>Status</span>
          </div>
          <div v-for="room in rooms" :key="room.id" class="data-row">
            <strong>{{ room.room_number }}</strong>
            <span>{{ formatRoomType(room.type_) }}</span>
            <span>{{ formatMoney(room.price) }}</span>
            <span class="status-pill">{{ room.room_status || "unknown" }}</span>
          </div>
        </div>
      </article>

      <article class="card">
        <div class="table-header">
          <div>
            <p class="eyebrow">Orders</p>
            <h2>My order list</h2>
          </div>
          <button type="button" class="button-ghost" :disabled="isLoadingOrders" @click="handleLoadOrders">
            Refresh
          </button>
        </div>

        <p class="feedback">{{ orderFeedback }}</p>

        <div v-if="isLoadingOrders" class="empty-panel">
          <p class="muted">Loading orders...</p>
        </div>

        <div v-else-if="orders.length === 0" class="empty-panel">
          <p class="muted">No orders found.</p>
        </div>

        <div v-else class="data-table">
          <div class="data-row guest-order-row data-row-head">
            <span>ID</span>
            <span>Room</span>
            <span>Stay</span>
            <span>Expense</span>
            <span>Status</span>
            <span>Dates</span>
            <span>Action</span>
          </div>
          <div v-for="order in orders" :key="order.id" class="data-row guest-order-row">
            <strong>#{{ order.id }}</strong>
            <span>{{ order.room?.room_number || order.room_id || "-" }}</span>
            <span>{{ order.stay_length ?? "-" }} day(s)</span>
            <span>{{ formatMoney(order.expense) }}</span>
            <span class="status-pill">{{ formatStatus(order.status) }}</span>
            <span>{{ formatDateRange(order) }}</span>
            <span>
              <button
                type="button"
                class="button-ghost"
                :disabled="order.status !== 'PENDING' || confirmingOrderId === order.id"
                @click="handleConfirmOrder(order.id)"
              >
                Confirm
              </button>
            </span>
          </div>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, reactive, ref } from "vue";
import {
  confirmCurrentUserOrder,
  createCurrentUserOrder,
  getCurrentUserOrders,
  getCurrentUserRooms,
} from "@/api/users";
import type { OrderCreatePayload } from "@/api/order";
import type { OrderResponse, OrderStatus, RoomResponse } from "@/types";

const rooms = ref<RoomResponse[]>([]);
const orders = ref<OrderResponse[]>([]);
const isLoadingRooms = ref(false);
const isLoadingOrders = ref(false);
const isCreatingOrder = ref(false);
const confirmingOrderId = ref<number | null>(null);
const roomFeedback = ref("");
const orderFeedback = ref("");
const createFeedback = ref("");
const today = getDateInputValue(new Date());

const createForm = reactive<OrderCreatePayload>({
  name: "",
  phone_number: "",
  room_number: "",
  check_in_date: today,
  check_out_date: getDateInputValue(addDays(new Date(), 1)),
  stay_length: 1,
});

const minCheckOutDate = computed(() =>
  getDateInputValue(addDays(parseDateInput(createForm.check_in_date) ?? new Date(), 1)),
);

const handleLoadRooms = async () => {
  isLoadingRooms.value = true;
  roomFeedback.value = "";

  try {
    rooms.value = await getCurrentUserRooms();
    roomFeedback.value = "Room list refreshed.";
  } catch (e: unknown) {
    roomFeedback.value = getErrorMessage(e);
  } finally {
    isLoadingRooms.value = false;
  }
};

const handleLoadOrders = async () => {
  isLoadingOrders.value = true;
  orderFeedback.value = "";

  try {
    orders.value = await getCurrentUserOrders();
    orderFeedback.value = "Order list refreshed.";
  } catch (e: unknown) {
    orderFeedback.value = getErrorMessage(e);
  } finally {
    isLoadingOrders.value = false;
  }
};

const handleCreateOrder = async () => {
  isCreatingOrder.value = true;
  createFeedback.value = "";

  try {
    const created = await createCurrentUserOrder(createForm);
    createFeedback.value = `Order #${created.id} created.`;
    createForm.name = "";
    createForm.phone_number = "";
    createForm.room_number = "";
    createForm.check_in_date = today;
    createForm.check_out_date = getDateInputValue(addDays(new Date(), 1));
    createForm.stay_length = 1;
    await Promise.all([handleLoadOrders(), handleLoadRooms()]);
  } catch (e: unknown) {
    createFeedback.value = getErrorMessage(e);
  } finally {
    isCreatingOrder.value = false;
  }
};

const handleConfirmOrder = async (orderId: number) => {
  confirmingOrderId.value = orderId;
  orderFeedback.value = "";

  try {
    const updated = await confirmCurrentUserOrder(orderId);
    orderFeedback.value = `Order #${updated.id} confirmed.`;
    await handleLoadOrders();
  } catch (e: unknown) {
    orderFeedback.value = getErrorMessage(e);
  } finally {
    confirmingOrderId.value = null;
  }
};

const countByStatus = (status: OrderStatus) =>
  orders.value.filter((order) => order.status === status).length;

const syncStayLength = () => {
  const checkIn = parseDateInput(createForm.check_in_date);
  const checkOut = parseDateInput(createForm.check_out_date);

  if (!checkIn) {
    createForm.check_in_date = today;
    return;
  }

  if (!checkOut || checkOut <= checkIn) {
    createForm.check_out_date = getDateInputValue(addDays(checkIn, 1));
    createForm.stay_length = 1;
    return;
  }

  createForm.stay_length = Math.max(
    1,
    Math.round((checkOut.getTime() - checkIn.getTime()) / 86400000),
  );
};

const formatRoomType = (type: string) => {
  const labels: Record<string, string> = {
    single: "Single",
    twin: "Twin",
    family: "Family",
  };

  return labels[type] ?? type;
};

const formatStatus = (status?: string) => {
  if (!status) return "Unknown";
  return status
    .split("_")
    .join(" ")
    .toLowerCase()
    .replace(/\b\w/g, (char: string) => char.toUpperCase());
};

const formatMoney = (value?: number | string) => {
  const amount = Number(value ?? 0);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(Number.isFinite(amount) ? amount : 0);
};

const formatDate = (value?: string) => {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString();
};

const formatDateRange = (order: OrderResponse) =>
  `${formatDate(order.check_in_date ?? order.check_in_time)} - ${formatDate(order.check_out_date)}`;

function parseDateInput(value?: string) {
  if (!value) return null;
  const date = new Date(`${value}T00:00:00`);
  return Number.isNaN(date.getTime()) ? null : date;
}

function addDays(value: Date, days: number) {
  const date = new Date(value);
  date.setDate(date.getDate() + days);
  return date;
}

function getDateInputValue(value: Date) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

const getErrorMessage = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;

    if (typeof detail === "string") return detail;

    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((item) => item?.msg)
        .filter(Boolean)
        .join("; ");
    }
  }

  if (error instanceof Error) return error.message;

  return "Request failed.";
};

onMounted(() => {
  void handleLoadRooms();
  void handleLoadOrders();
});
</script>

<style scoped>
.guest-order-row {
  grid-template-columns: 0.55fr 0.8fr 0.8fr 0.9fr 1fr 0.9fr 0.9fr;
}

@media (max-width: 900px) {
  .guest-order-row {
    grid-template-columns: 1fr;
  }
}
</style>
