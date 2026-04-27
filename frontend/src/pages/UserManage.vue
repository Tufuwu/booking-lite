<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">User management</p>
      <h1>People directory</h1>
      <p class="muted">Create, review, and organize guest or staff records from one clean workspace.</p>
    </section>

    <section class="card">
      <div class="table-header">
        <div>
          <p class="eyebrow">Directory</p>
          <h2>User list</h2>
        </div>
        <div class="button-row">
          <span class="muted">{{ users.length }} user(s)</span>
          <button type="button" class="button-ghost" :disabled="isLoadingUsers" @click="handleGetAllUsers">
            Refresh list
          </button>
        </div>
      </div>

      <p class="feedback">{{ userFeedback }}</p>

      <div v-if="isLoadingUsers" class="empty-panel">
        <p class="muted">Loading users...</p>
      </div>

      <div v-else-if="users.length === 0" class="empty-panel">
        <p class="muted">No users found.</p>
      </div>

      <div v-else class="data-table">
        <div class="data-row data-row-head">
          <span>ID</span>
          <span>Name</span>
          <span>Phone</span>
          <span>Orders</span>
        </div>
        <div v-for="user in users" :key="user.id" class="data-row">
          <strong>{{ user.id }}</strong>
          <span>{{ user.name }}</span>
          <span>{{ getUserPhoneNumber(user) }}</span>
          <span>{{ user.order?.length ?? 0 }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import axios from "axios";
import { getAllUsers } from "@/api/users";
import type { UserCreatePayload, UserResponse } from "@/types";

const userFeedback = ref("");
const isLoadingUsers = ref(false);
const users = ref<UserResponse[]>([]);
const userForm = reactive<UserCreatePayload>({
  name: "",
  phone_number: "",
  identity_number: "",
  role: "guest",
  password: "",
});


const handleGetAllUsers = async () => {
  userFeedback.value = "";
  isLoadingUsers.value = true;

  try {
    users.value = await getAllUsers();
    userFeedback.value = "User list refreshed.";
  } catch (e: any) {
    userFeedback.value = getErrorMessage(e);
  } finally {
    isLoadingUsers.value = false;
  }
};

const getUserPhoneNumber = (user: UserResponse) =>
  user.phone_number ?? (user as UserResponse & { room_number?: string }).room_number ?? "-";

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
  void handleGetAllUsers();
});
</script>
