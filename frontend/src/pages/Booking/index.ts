import { bookingStore } from "../../store/bookingStore.js";

export function renderBookingPage(): string {
  const { info } = bookingStore.getState();

  return `
    <section class="card">
      <p class="eyebrow">Booking Placeholder</p>
      <h2>Booking, check-in, and payment APIs are still pending</h2>
      <p class="muted">${info}</p>
      <p class="note">
        The backend already has an Order model, but it does not expose create-order, list-order, or payment-status routes yet, so this page is intentionally a shell for the next step.
      </p>
    </section>
  `;
}
