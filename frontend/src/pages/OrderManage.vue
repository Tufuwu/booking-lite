<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">Order management</p>
      <h1>Orders workspace</h1>
      <p class="muted">Create bookings, search orders, and drive the order status workflow.</p>
    </section>

    <section class="metric-row">
      <article class="metric-card">
        <span class="muted">Total</span>
        <strong>{{ orders.length }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Pending</span>
        <strong>{{ countByStatus("PENDING") }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Checked in</span>
        <strong>{{ countByStatus("CHECKED_IN") }}</strong>
      </article>
      <article class="metric-card">
        <span class="muted">Revenue</span>
        <strong>{{ formatMoney(totalRevenue) }}</strong>
      </article>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Create order</p>
        <h2>New booking</h2>
        <form class="form-stack" @submit.prevent="handleCreateOrder">
          <div class="form-grid">
            <label>
              <span>Guest name</span>
              <input v-model="createForm.name" placeholder="Full name" required />
            </label>
            <label>
              <span>Phone number</span>
              <input v-model="createForm.phone_number" placeholder="Contact phone" required />
            </label>
            <label>
              <span>Room number</span>
              <input v-model="createForm.room_number" placeholder="Example: 110" required />
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
          <button type="submit" :disabled="isCreating">Create order</button>
          <p class="feedback">{{ createFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <p class="eyebrow">Search</p>
        <h2>Filters</h2>
        <form class="form-stack" @submit.prevent="handleLoadOrders">
          <div class="form-grid">
            <label>
              <span>User id</span>
              <input v-model="filterUserId" type="number" min="1" placeholder="All users" />
            </label>
            <label>
              <span>Status</span>
              <select v-model="filterStatus">
                <option value="">All statuses</option>
                <option v-for="status in statusOptions" :key="status" :value="status">
                  {{ formatStatus(status) }}
                </option>
              </select>
            </label>
            <label>
              <span>Order id</span>
              <input v-model="lookupOrderId" type="number" min="1" placeholder="Find one order" />
            </label>
          </div>
          <div class="button-row">
            <button type="submit" :disabled="isLoading">Refresh list</button>
            <button type="button" class="button-ghost" :disabled="isLoadingOne" @click="handleLookupOrder">
              Lookup order
            </button>
          </div>
          <p class="feedback">{{ listFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <p class="eyebrow">Extend stay</p>
        <h2>Add nights</h2>
        <form class="form-stack" @submit.prevent="handleExtendOrder">
          <div class="form-grid">
            <label>
              <span>Order id</span>
              <input v-model.number="extendForm.order_id" type="number" min="1" required />
            </label>
            <label>
              <span>Extra days</span>
              <input v-model.number="extendForm.extra_days" type="number" min="1" required />
            </label>
          </div>
          <button type="submit" :disabled="activeAction === 'extend'">Extend order</button>
          <p class="feedback">{{ actionFeedback }}</p>
        </form>
      </article>

      <article class="card empty-panel">
        <p class="eyebrow">Workflow</p>
        <h2>Status actions</h2>
        <p class="muted">
          Use the buttons in the table to confirm, check in, check out, cancel, refund, or recalculate an order.
        </p>
      </article>
    </section>

    <section class="card">
      <div class="table-header">
        <div>
          <p class="eyebrow">Orders</p>
          <h2>Order list</h2>
        </div>
        <span class="muted">{{ orders.length }} order(s)</span>
      </div>

      <div v-if="isLoading" class="empty-panel">
        <p class="muted">Loading orders...</p>
      </div>

      <div v-else-if="orders.length === 0" class="empty-panel">
        <p class="muted">No orders found.</p>
      </div>

      <div v-else class="data-table">
        <div class="data-row admin-order-row data-row-head">
          <span>ID</span>
          <span>Guest</span>
          <span>Room</span>
          <span>Stay</span>
          <span>Expense</span>
          <span>Status</span>
          <span>Dates</span>
          <span>Actions</span>
        </div>
        <div v-for="order in orders" :key="order.id" class="data-row admin-order-row">
          <strong>#{{ order.id }}</strong>
          <span>{{ order.user?.name || `User ${order.user_id ?? "-"}` }}</span>
          <span>{{ order.room?.room_number || order.room_id || "-" }}</span>
          <span>{{ order.stay_length ?? "-" }} day(s)</span>
          <span>{{ formatMoney(order.expense) }}</span>
          <span class="status-pill">{{ formatStatus(order.status) }}</span>
          <span>{{ formatDateRange(order) }}</span>
          <span class="table-actions">
            <button
              type="button"
              class="button-ghost"
              :disabled="!canRunAction(order, 'confirm')"
              @click="handleOrderAction(order.id, 'confirm')"
            >
              Confirm
            </button>
            <button
              type="button"
              class="button-ghost"
              :disabled="!canRunAction(order, 'check-in')"
              @click="handleOrderAction(order.id, 'check-in')"
            >
              Check in
            </button>
            <button
              type="button"
              class="button-ghost"
              :disabled="!canRunAction(order, 'check-out')"
              @click="handleOrderAction(order.id, 'check-out')"
            >
              Check out
            </button>
            <button
              type="button"
              class="button-ghost"
              :disabled="!canRunAction(order, 'recalculate')"
              @click="handleOrderAction(order.id, 'recalculate')"
            >
              Recalc
            </button>
            <button
              type="button"
              class="button-danger"
              :disabled="!canRunAction(order, 'cancel')"
              @click="handleOrderAction(order.id, 'cancel')"
            >
              Cancel
            </button>
            <button
              type="button"
              class="button-danger"
              :disabled="!canRunAction(order, 'refund')"
              @click="handleOrderAction(order.id, 'refund')"
            >
              Refund
            </button>
          </span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import axios from "axios";
import { computed, onMounted, reactive, ref } from "vue";
import {
  cancelOrder,
  checkInOrder,
  checkOutOrder,
  confirmOrder,
  createOrder,
  extendOrder,
  getOrder,
  listOrders,
  recalculateOrder,
  refundOrder,
  type OrderCreatePayload,
} from "@/api/order";
import type { OrderResponse, OrderStatus } from "@/types";

type OrderAction = "confirm" | "check-in" | "check-out" | "cancel" | "refund" | "recalculate" | "extend";

const statusOptions: OrderStatus[] = [
  "PENDING",
  "CONFIRMED",
  "CHECKED_IN",
  "COMPLETED",
  "CANCELLED_UNPAID",
  "CANCELLED_PAID",
  "REFUNDED",
];

const orders = ref<OrderResponse[]>([]);
const isLoading = ref(false);
const isLoadingOne = ref(false);
const isCreating = ref(false);
const activeAction = ref<OrderAction | "">("");
const createFeedback = ref("");
const listFeedback = ref("");
const actionFeedback = ref("");
const filterUserId = ref("");
const filterStatus = ref<OrderStatus | "">("");
const lookupOrderId = ref("");
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

const extendForm = reactive({
  order_id: 1,
  extra_days: 1,
});

const totalRevenue = computed(() =>
  orders.value.reduce((sum, order) => sum + Number(order.expense ?? 0), 0),
);

const countByStatus = (status: OrderStatus) =>
  orders.value.filter((order) => order.status === status).length;

const allowedActionsByStatus: Record<OrderStatus, OrderAction[]> = {
  PENDING: ["confirm", "cancel", "recalculate", "extend"],
  CONFIRMED: ["check-in", "cancel", "recalculate", "extend"],
  CHECKED_IN: ["check-out", "refund", "recalculate"],
  COMPLETED: ["recalculate"],
  CANCELLED: ["recalculate"],
  CANCELLED_UNPAID: ["recalculate"],
  CANCELLED_PAID: ["refund", "recalculate"],
  REFUNDED: ["recalculate"],
};

const isOrderStatus = (status?: string): status is OrderStatus =>
  statusOptions.includes(status as OrderStatus);

const canRunAction = (order: OrderResponse, action: OrderAction) => {
  if (!isOrderStatus(order.status)) {
    return action === "recalculate";
  }

  return allowedActionsByStatus[order.status].includes(action);
};

const handleLoadOrders = async () => {
  isLoading.value = true;
  listFeedback.value = "";

  try {
    const userId = filterUserId.value ? Number(filterUserId.value) : undefined;
    const params: { user_id?: number; status?: OrderStatus | "" } = {};

    if (userId !== undefined) {
      params.user_id = userId;
    }

    if (filterStatus.value) {
      params.status = filterStatus.value;
    }

    orders.value = await listOrders(params);
    listFeedback.value = "Order list refreshed.";
  } catch (e: unknown) {
    listFeedback.value = getErrorMessage(e);
  } finally {
    isLoading.value = false;
  }
};

const handleLookupOrder = async () => {
  const orderId = Number(lookupOrderId.value);
  if (!Number.isFinite(orderId) || orderId <= 0) {
    listFeedback.value = "Please enter a valid order id.";
    return;
  }

  isLoadingOne.value = true;
  listFeedback.value = "";

  try {
    orders.value = [await getOrder(orderId)];
    listFeedback.value = `Loaded order #${orderId}.`;
  } catch (e: unknown) {
    listFeedback.value = getErrorMessage(e);
  } finally {
    isLoadingOne.value = false;
  }
};

const handleCreateOrder = async () => {
  createFeedback.value = "";
  isCreating.value = true;

  try {
    const created = await createOrder(createForm);
    createFeedback.value = `Created order #${created.id}.`;
    createForm.name = "";
    createForm.phone_number = "";
    createForm.room_number = "";
    createForm.check_in_date = today;
    createForm.check_out_date = getDateInputValue(addDays(new Date(), 1));
    createForm.stay_length = 1;
    await handleLoadOrders();
  } catch (e: unknown) {
    createFeedback.value = getErrorMessage(e);
  } finally {
    isCreating.value = false;
  }
};

const handleOrderAction = async (orderId: number, action: OrderAction) => {
  activeAction.value = action;
  actionFeedback.value = "";

  const order = orders.value.find((item) => item.id === orderId);
  if (order && !canRunAction(order, action)) {
    actionFeedback.value = `${formatStatus(order.status)} orders cannot ${action}.`;
    activeAction.value = "";
    return;
  }

  try {
    const actionMap = {
      confirm: () => confirmOrder(orderId),
      "check-in": () => checkInOrder(orderId),
      "check-out": () => checkOutOrder(orderId),
      cancel: () => cancelOrder(orderId),
      refund: () => refundOrder(orderId),
      recalculate: () => recalculateOrder(orderId),
      extend: () => extendOrder(orderId, { extra_days: extendForm.extra_days }),
    };

    const updated = await actionMap[action]();
    actionFeedback.value = `Order #${updated.id} ${action} completed.`;
    await handleLoadOrders();
  } catch (e: unknown) {
    actionFeedback.value = getErrorMessage(e);
  } finally {
    activeAction.value = "";
  }
};

const handleExtendOrder = async () => {
  await handleOrderAction(extendForm.order_id, "extend");
};

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

const formatStatus = (status?: string) => {
  if (!status) return "Unknown";
  return status
    .split("_")
    .join(" ")
    .toLowerCase()
    .replace(/\b\w/g, (char: string) => char.toUpperCase());
};

const formatMoney = (value?: number) => {
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

    if (Array.isArray(detail)) {
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
  void handleLoadOrders();
});
</script>

<style scoped>
.admin-order-row {
  grid-template-columns: 0.5fr 1fr 0.75fr 0.75fr 0.85fr 0.95fr 1.35fr 2.2fr;
}

@media (max-width: 900px) {
  .admin-order-row {
    grid-template-columns: 1fr;
  }
}
</style>
