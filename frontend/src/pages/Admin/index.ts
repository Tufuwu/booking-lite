import { createAdmin, deleteCurrentAdmin, logoutAdmin } from "../../api/auth.js";
import { createRoom } from "../../api/booking.js";
import { navigate } from "../../router/index.js";
import { userStore } from "../../store/userStore.js";

export function renderAdminPage(): string {
  const session = userStore.getState();

  return `
    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Session</p>
        <h2>Admin console</h2>
        <p class="muted">Status: ${session ? `logged in as ${session.jobNumber}` : "not logged in yet, protected routes will return 401"}</p>
        <div class="button-row">
          <button id="logout-button" type="button" class="button-secondary">Logout</button>
          <button id="go-login-button" type="button" class="button-ghost">Go to login</button>
        </div>
        <p id="session-feedback" class="feedback"></p>
      </article>

      <article class="card danger-card">
        <p class="eyebrow">Danger Zone</p>
        <h3>Delete current admin</h3>
        <form id="delete-admin-form" class="form-stack">
          <label>
            <span>Confirm password</span>
            <input name="password" type="password" required />
          </label>
          <button type="submit" class="button-danger">Delete current admin</button>
          <p id="delete-feedback" class="feedback"></p>
        </form>
      </article>
    </section>

    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Admin Management</p>
        <h3>Create admin</h3>
        <form id="create-admin-form" class="form-stack">
          <label>
            <span>Job number</span>
            <input name="job_number" placeholder="0002" required />
          </label>
          <label>
            <span>Name</span>
            <input name="name" placeholder="Alice" required />
          </label>
          <label>
            <span>Password</span>
            <input name="password" type="password" required />
          </label>
          <button type="submit">Create admin</button>
          <p id="create-admin-feedback" class="feedback"></p>
        </form>
      </article>

      <article class="card">
        <p class="eyebrow">Room Management</p>
        <h3>Create room</h3>
        <form id="create-room-form" class="form-stack">
          <label>
            <span>Room number</span>
            <input name="room_number" placeholder="1208" required />
          </label>
          <label>
            <span>Room type</span>
            <select name="type_">
              <option value="single">single</option>
              <option value="twin">twin</option>
              <option value="family">family</option>
            </select>
          </label>
          <label>
            <span>Price</span>
            <input name="price" type="number" min="0" step="0.01" placeholder="399.00" required />
          </label>
          <button type="submit">Create room</button>
          <p id="create-room-feedback" class="feedback"></p>
        </form>
      </article>
    </section>
  `;
}

export function bindAdminPage(): void {
  bindLogout();
  bindDeleteCurrentAdmin();
  bindCreateAdmin();
  bindCreateRoom();
}

function bindLogout(): void {
  const logoutButton = document.querySelector<HTMLButtonElement>("#logout-button");
  const loginButton = document.querySelector<HTMLButtonElement>("#go-login-button");
  const feedback = document.querySelector<HTMLElement>("#session-feedback");

  logoutButton?.addEventListener("click", async () => {
    if (!feedback) {
      return;
    }
    try {
      await logoutAdmin();
      userStore.setSession(null);
      feedback.textContent = "Logged out.";
      navigate("login");
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Logout failed";
    }
  });

  loginButton?.addEventListener("click", () => navigate("login"));
}

function bindDeleteCurrentAdmin(): void {
  const form = document.querySelector<HTMLFormElement>("#delete-admin-form");
  const feedback = document.querySelector<HTMLElement>("#delete-feedback");
  if (!form || !feedback) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const password = String(formData.get("password") ?? "");

    try {
      await deleteCurrentAdmin(password);
      userStore.setSession(null);
      feedback.textContent = "Admin deleted. Redirecting to login...";
      navigate("login");
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Delete failed";
    }
  });
}

function bindCreateAdmin(): void {
  const form = document.querySelector<HTMLFormElement>("#create-admin-form");
  const feedback = document.querySelector<HTMLElement>("#create-admin-feedback");
  if (!form || !feedback) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    try {
      const created = await createAdmin({
        job_number: String(formData.get("job_number") ?? "").trim(),
        name: String(formData.get("name") ?? "").trim(),
        password: String(formData.get("password") ?? ""),
      });
      feedback.textContent = `Created: ${created.name} (ID ${created.id})`;
      form.reset();
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Create failed";
    }
  });
}

function bindCreateRoom(): void {
  const form = document.querySelector<HTMLFormElement>("#create-room-form");
  const feedback = document.querySelector<HTMLElement>("#create-room-feedback");
  if (!form || !feedback) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    try {
      const created = await createRoom({
        room_number: String(formData.get("room_number") ?? "").trim(),
        type_: String(formData.get("type_") ?? "single") as "single" | "twin" | "family",
        price: String(formData.get("price") ?? ""),
      });
      feedback.textContent = `Room ${created.room_number} created`;
      form.reset();
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Create failed";
    }
  });
}
