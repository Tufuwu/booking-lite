import { loginAdmin } from "../../api/auth.js";
import { userStore } from "../../store/userStore.js";
import { navigate } from "../../router/index.js";

export function renderLoginPage(): string {
  return `
    <section class="grid grid-2">
      <article class="card">
        <p class="eyebrow">Admin Login</p>
        <h2>Connect to the FastAPI session flow</h2>
        <form id="login-form" class="form-stack">
          <label>
            <span>Admin name</span>
            <input name="username" placeholder="For example: Super Admin" required />
          </label>
          <label>
            <span>Password</span>
            <input name="password" type="password" placeholder="Enter password" required />
          </label>
          <button type="submit">Login</button>
          <p id="login-feedback" class="feedback"></p>
        </form>
      </article>

      <article class="card accent-card">
        <p class="eyebrow">Seed Account</p>
        <h3>The backend attempts to create this on startup</h3>
        <p class="muted">Name: Super Admin</p>
        <p class="muted">Job number: 0001</p>
        <p class="muted">Password: admin123</p>
        <p class="note">The login route expects an OAuth form, so the username field must carry the admin name.</p>
      </article>
    </section>
  `;
}

export function bindLoginPage(): void {
  const form = document.querySelector<HTMLFormElement>("#login-form");
  const feedback = document.querySelector<HTMLElement>("#login-feedback");
  if (!form || !feedback) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    feedback.textContent = "Logging in...";

    const formData = new FormData(form);
    const username = String(formData.get("username") ?? "").trim();
    const password = String(formData.get("password") ?? "");

    try {
      const session = await loginAdmin(username, password);
      userStore.setSession(session);
      feedback.textContent = "Login successful. Redirecting...";
      navigate("admin");
    } catch (error) {
      feedback.textContent = error instanceof Error ? error.message : "Login failed";
    }
  });
}
