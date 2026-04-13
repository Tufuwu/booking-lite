const STORAGE_KEY = "booking-lite-admin-session";
class UserStore {
    constructor() {
        this.listeners = new Set();
        this.session = this.read();
    }
    subscribe(listener) {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }
    getState() {
        return this.session;
    }
    setSession(session) {
        this.session = session;
        if (session) {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(session));
        }
        else {
            localStorage.removeItem(STORAGE_KEY);
        }
        this.emit();
    }
    isLoggedIn() {
        return Boolean(this.session);
    }
    read() {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            return null;
        }
        try {
            return JSON.parse(raw);
        }
        catch {
            localStorage.removeItem(STORAGE_KEY);
            return null;
        }
    }
    emit() {
        for (const listener of this.listeners) {
            listener();
        }
    }
}
export const userStore = new UserStore();
//# sourceMappingURL=userStore.js.map