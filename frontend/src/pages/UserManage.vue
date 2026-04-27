<template>
  <div class="admin-page">
    <section class="panel">
      <p class="eyebrow">User management</p>
      <h1>People directory</h1>
      <p class="muted">Create, review, and organize guest or staff records from one clean workspace.</p>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Create user</p>
        <h2>New profile</h2>
        <form @submit.prevent="handleCreateUser" class="form-stack">
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
              <option value="guest">Guest</option>
              <option value="staff">Staff</option>
              <option value="admin">Admin</option>
            </select>
          </label>
          <button type="submit">Create user</button>
          <p class="feedback">{{ userFeedback }}</p>
        </form>
      </article>

      <article class="card empty-panel">
        <p class="eyebrow">Directory</p>
        <h2>User list</h2>
        <p class="muted">Connect the list API here to search profiles by role, phone, or identity number.</p>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { createUser } from "@/api/users";
import type { UserCreatePayload } from "@/types";

const userFeedback = ref("");
const userForm = reactive<UserCreatePayload>({
  name: "",
  phone_number: "",
  identity_number: "",
  type_: "guest",
  password: "",
});

const handleCreateUser = async () => {
  try {
    const created = await createUser(userForm);
    userFeedback.value = `Created: ${created.name}`;
  } catch (e: any) {
    userFeedback.value = e.message;
  }
};
</script>
