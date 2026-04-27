<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">Admin console</p>
      <p class="muted">
        Signed in as {{ userStore.user?.name || "current staff" }}.
      </p>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Create account</p>
        <h2>New staff</h2>
        <form @submit.prevent="handleCreateAdmin" class="form-stack">
          <div class="form-grid">
            <label>
              <span>Name</span>
              <input v-model="userForm.name" placeholder="Full name" required />
            </label>
            <label>
              <span>Phone number</span>
              <input v-model="userForm.phone_number" placeholder="Contact phone" required />
            </label>
            <label>
              <span>Identity number</span>
              <input v-model="userForm.identity_number" placeholder="ID number" required />
            </label>
            <label>
              <span>Password</span>
              <input v-model="userForm.password" type="password" placeholder="Temporary password" required />
            </label>
          </div>
          <label>
            <span>Role</span>
            <select v-model="userForm.type_">
              <option value="admin">Admin</option>
              <option value="staff">Staff</option>
              <option value="guest">Guest</option>
            </select>
          </label>
          <button type="submit">Create account</button>
          <p class="feedback">{{ adminFeedback }}</p>
        </form>
      </article>

      <article class="card danger-card">
        <p class="eyebrow">Danger zone</p>
        <h2>Delete current admin</h2>
        <p class="muted">This action requires password confirmation.</p>
        <form @submit.prevent="handleDeleteAdmin" class="form-stack">
          <label>
            <span>Confirm password</span>
            <input v-model="deleteForm.password" type="password" required />
          </label>
          <button type="submit" class="button-danger">Delete account</button>
          <p class="feedback">{{ deleteFeedback }}</p>
        </form>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { createAdmin, deleteCurrentAdmin } from "@/api/auth";
import { useUserStore } from "@/store/user";
import type { UserCreatePayload } from "@/types";

const userStore = useUserStore();
const router = useRouter();
const deleteFeedback = ref("");
const adminFeedback = ref("");

const deleteForm = reactive({ password: "" });
const userForm = reactive<UserCreatePayload>({
  name: "",
  phone_number: "",
  identity_number: "",
  type_: "staff",
  password: "",
});

const moveToRoomAdmin = () => router.push("/admin/room");
const moveToAdmin = () => router.push("/admin");
const moveToOrderAdmin = () => router.push("/admin/order");
const moveToUserAdmin = () => router.push("/admin/user");

const handleDeleteAdmin = async () => {
  try {
    await deleteCurrentAdmin(deleteForm.password);
    userStore.logout();
    await router.push("/login");
  } catch (e: any) {
    deleteFeedback.value = e.message;
  }
};

const handleCreateAdmin = async () => {
  try {
    const created = await createAdmin(userForm);
    adminFeedback.value = `Created: ${created.name}`;
  } catch (e: any) {
    adminFeedback.value = e.message;
  }
};
</script>
