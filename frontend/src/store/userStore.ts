import type { SessionUser } from "../types.js";

type Listener = () => void;

const STORAGE_KEY = "booking-lite-admin-session";

class UserStore {
  private listeners = new Set<Listener>();

  private session: SessionUser | null = this.read();

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getState(): SessionUser | null {
    return this.session;
  }

  setSession(session: SessionUser | null): void {
    this.session = session;
    if (session) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
    this.emit();
  }

  isLoggedIn(): boolean {
    return Boolean(this.session);
  }

  private read(): SessionUser | null {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return null;
    }

    try {
      return JSON.parse(raw) as SessionUser;
    } catch {
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }
  }

  private emit(): void {
    for (const listener of this.listeners) {
      listener();
    }
  }
}

export const userStore = new UserStore();
