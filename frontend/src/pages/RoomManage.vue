<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">Room management</p>
      <h1>Room inventory</h1>
      <p class="muted">Create, update, and delete rooms for booking operations.</p>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Create room</p>
        <h2>New room</h2>
        <form @submit.prevent="handleCreateRoom" class="form-stack">
          <label>
            <span>Room number</span>
            <input v-model="createForm.room_number" placeholder="Example: 1208" required />
          </label>
          <div class="form-grid">
            <label>
              <span>Room type</span>
              <select v-model="createForm.type_">
                <option value="single">Single</option>
                <option value="twin">Twin</option>
                <option value="family">Family</option>
              </select>
            </label>
            <label>
              <span>Price</span>
              <input v-model="createForm.price" type="number" min="0" step="0.01" placeholder="0.00" required />
            </label>
          </div>
          <button type="submit" :disabled="isCreatingRoom">Create room</button>
          <p class="feedback">{{ createFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <p class="eyebrow">Update room</p>
        <h2>Edit room details</h2>
        <form @submit.prevent="handleUpdateRoom" class="form-stack">
          <label>
            <span>Room number</span>
            <input v-model="updateForm.room_number" placeholder="Room to update" required />
          </label>
          <div class="form-grid">
            <label>
              <span>Room type</span>
              <select v-model="updateForm.type_">
                <option value="">Keep current</option>
                <option value="single">Single</option>
                <option value="twin">Twin</option>
                <option value="family">Family</option>
              </select>
            </label>
            <label>
              <span>Price</span>
              <input v-model="updateForm.price" type="number" min="0" step="0.01" placeholder="Keep current" />
            </label>
          </div>
          <button type="submit" :disabled="isUpdatingRoom">Update room</button>
          <p class="feedback">{{ updateFeedback }}</p>
        </form>
      </article>

      <article class="card danger-card">
        <p class="eyebrow">Delete room</p>
        <h2>Remove room</h2>
        <form @submit.prevent="handleDeleteRoom" class="form-stack">
          <label>
            <span>Room number</span>
            <input v-model="deleteRoomNumber" placeholder="Example: 1208" required />
          </label>
          <button type="submit" class="button-danger" :disabled="isDeletingRoom">Delete room</button>
          <p class="feedback">{{ deleteFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <p class="eyebrow">Room query</p>
        <h2>All rooms</h2>
        <div class="button-row">
          <button type="button" class="button-ghost" :disabled="isLoadingRooms" @click="handleLoadRooms">
            Refresh list
          </button>
        </div>
        <p class="feedback">{{ listFeedback }}</p>
      </article>
    </section>

    <section class="card">
      <div class="table-header">
        <div>
          <p class="eyebrow">Inventory</p>
          <h2>Room list</h2>
        </div>
        <span class="muted">{{ rooms.length }} room(s)</span>
      </div>

      <div v-if="isLoadingRooms" class="empty-panel">
        <p class="muted">Loading rooms...</p>
      </div>

      <div v-else-if="rooms.length === 0" class="empty-panel">
        <p class="muted">No rooms found.</p>
      </div>

      <div v-else class="data-table">
        <div class="data-row data-row-head">
          <span>Room number</span>
          <span>Type</span>
          <span>Price</span>
          <span>Status</span>
        </div>
        <div v-for="room in rooms" :key="room.id" class="data-row">
          <strong>{{ room.room_number }}</strong>
          <span>{{ formatRoomType(room.type_) }}</span>
          <span>{{ formatPrice(room.price) }}</span>
          <span class="status-pill">{{ room.room_status || "unknown" }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import axios from "axios";
import { createRoom, deleteRoom, getAllRooms, updateRoom } from "@/api/rooms";
import type { RoomCreatePayload, RoomUpdatePayload, RoomTypeOption, RoomResponse } from "@/types";

type OptionalRoomType = RoomTypeOption["value"] | "";
interface RoomUpdateForm {
  room_number: string;
  type_: OptionalRoomType;
  price: string;
}

const createFeedback = ref("");
const updateFeedback = ref("");
const deleteFeedback = ref("");
const listFeedback = ref("");
const deleteRoomNumber = ref("");
const isLoadingRooms = ref(false);
const isCreatingRoom = ref(false);
const isUpdatingRoom = ref(false);
const isDeletingRoom = ref(false);
const rooms = ref<RoomResponse[]>([]);

const createForm = reactive<RoomCreatePayload>({
  room_number: "",
  type_: "single",
  price: "",
});

const updateForm = reactive<RoomUpdateForm>({
  room_number: "",
  type_: "",
  price: "",
});

const handleCreateRoom = async () => {
  createFeedback.value = "";
  isCreatingRoom.value = true;

  try {
    const created = await createRoom(createForm);
    createFeedback.value = `Created room ${created.room_number}`;
    createForm.room_number = "";
    createForm.type_ = "single";
    createForm.price = "";
    await handleLoadRooms();
  } catch (e: any) {
    createFeedback.value = getErrorMessage(e);
  } finally {
    isCreatingRoom.value = false;
  }
};

const handleUpdateRoom = async () => {
  updateFeedback.value = "";

  const payload: RoomUpdatePayload = {
    room_number: updateForm.room_number,
  };

  if (updateForm.type_) {
    payload.type_ = updateForm.type_;
  }

  if (updateForm.price) {
    payload.price = updateForm.price;
  }

  if (!payload.type_ && !payload.price) {
    updateFeedback.value = "Please choose a new room type or enter a new price.";
    return;
  }

  isUpdatingRoom.value = true;
  try {
    const updatedRooms = await updateRoom(payload);
    updateFeedback.value = `Updated ${updatedRooms.length} room record(s)`;
    updateForm.room_number = "";
    updateForm.type_ = "";
    updateForm.price = "";
    await handleLoadRooms();
  } catch (e: any) {
    updateFeedback.value = getErrorMessage(e);
  } finally {
    isUpdatingRoom.value = false;
  }
};

const handleDeleteRoom = async () => {
  deleteFeedback.value = "";

  const roomNumber = deleteRoomNumber.value.trim();
  if (!roomNumber) {
    deleteFeedback.value = "Please enter a valid room number.";
    return;
  }

  isDeletingRoom.value = true;
  try {
    await deleteRoom(roomNumber);
    deleteFeedback.value = `Deleted room ${roomNumber}`;
    deleteRoomNumber.value = "";
    await handleLoadRooms();
  } catch (e: any) {
    deleteFeedback.value = getErrorMessage(e);
  } finally {
    isDeletingRoom.value = false;
  }
};

const handleLoadRooms = async () => {
  isLoadingRooms.value = true;
  listFeedback.value = "";

  try {
    rooms.value = await getAllRooms();
    listFeedback.value = "Room list refreshed.";
  } catch (e: any) {
    listFeedback.value = getErrorMessage(e);
  } finally {
    isLoadingRooms.value = false;
  }
};

const formatRoomType = (type: string) => {
  const labels: Record<string, string> = {
    single: "Single",
    twin: "Twin",
    family: "Family",
  };

  return labels[type] ?? type;
};

const formatPrice = (price: number | string) => {
  const numericPrice = Number(price);

  if (!Number.isFinite(numericPrice)) {
    return String(price);
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(numericPrice);
};

const getErrorMessage = (error: unknown) => {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;

    if (typeof detail === "string") {
      return detail;
    }

    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((item) => item?.msg)
        .filter(Boolean)
        .join("; ");
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "Request failed.";
};

onMounted(() => {
  void handleLoadRooms();
});
</script>
