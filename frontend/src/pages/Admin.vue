<template>
  <div class="admin-page">
    <section class="grid grid-2">
      <article class="card">
        <h2>Admin console</h2>
        <p class="muted">
          User:
          {{ userStore.session ? `${userStore.session.jobNumber}` : "errors" }}
        </p>
        <p class="feedback">{{ sessionFeedback }}</p>
      </article>

      <article class="card danger-card">
        <p class="eyebrow">Settings</p>
        <h3>Delete admin</h3>
        <form @submit.prevent="handleDeleteAdmin" class="form-stack">
          <label>
            <span>Confirm password</span>
            <input v-model="deleteForm.password" type="password" required />
          </label>
          <button type="submit" class="button-danger">Delete current admin</button>
          <p class="feedback">{{ deleteFeedback }}</p>
        </form>
      </article>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <h3>Update admin</h3>
        <form @submit.prevent="handleUpdateAdmin" class="form-stack">
          <input v-model="adminUpdateForm.name" placeholder="Name"  />
          <input v-model="adminUpdateForm.password" placeholder="Password"  />
          <button type="submit">Update admin</button>
          <p class="feedback">{{ adminFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <h3>Create admin</h3>
        <form @submit.prevent="handleCreateAdmin" class="form-stack">
          <input v-model="adminForm.job_number" placeholder="Job number" required />
          <input v-model="adminForm.name" placeholder="Name" required />
          <input v-model="adminForm.password" type="password" required />
          <button type="submit">Create admin</button>
          <p class="feedback">{{ adminFeedback }}</p>
        </form>
      </article>

      <article class="card">
        <h3>Create room</h3>
        <form @submit.prevent="handleCreateRoom" class="form-stack">
          <input v-model="roomForm.room_number" placeholder="Room number" required />
          <select v-model="roomForm.type_">
            <option value="single">single</option>
            <option value="twin">twin</option>
            <option value="family">family</option>
          </select>
          <input v-model="roomForm.price" type="number" step="0.01" required />
          <button type="submit">Create room</button>
          <p class="feedback">{{ roomFeedback }}</p>
        </form>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { useUserStore } from "@/store/user";
import { useRouter } from "vue-router";
import { createAdmin, deleteCurrentAdmin, logoutAdmin, updateAdmin } from "@/api/auth";
import { createRoom } from "@/api/booking";
import type { AdminUpdatePayload, RoomCreatePayload } from "@/types";

const userStore = useUserStore();
const router = useRouter();
// 反馈信息状态
const sessionFeedback = ref("");
const deleteFeedback = ref("");
const adminFeedback = ref("");
const roomFeedback = ref("");

// 表单数据绑定
const deleteForm = reactive({ password: "" });
const adminForm = reactive({ job_number: "", name: "", password: "" });
const roomForm = reactive<RoomCreatePayload>({ room_number: "", type_: "single", price: "" });
const adminUpdateForm = reactive({ name: "", password: "" });
// 处理逻辑
const handleUpdateAdmin = async () => {
  try {
    const payload: AdminUpdatePayload = {};

    if (adminUpdateForm.name.trim()) {
      payload.name = adminUpdateForm.name;
    }

    if (adminUpdateForm.password.trim()) {
      payload.password = adminUpdateForm.password;
    }

    await updateAdmin(payload);
    userStore.logout();
    router.push("/login");
  } catch (e : any) {
    sessionFeedback.value = e.message;
  }
};
const handleDeleteAdmin = async () => {
  try {
    await deleteCurrentAdmin(deleteForm.password);
    router.push("/login");
  } catch (e: any) { deleteFeedback.value = e.message; }
};

const handleCreateAdmin = async () => {
  try {
    const created = await createAdmin(adminForm);
    adminFeedback.value = `Created: ${created.name}`;
  } catch (e: any) { adminFeedback.value = e.message; }
};

const handleCreateRoom = async () => {
  try {
    await createRoom(roomForm);
    roomFeedback.value = "Room created successfully";
  } catch (e: any) { roomFeedback.value = e.message; }
};
</script>