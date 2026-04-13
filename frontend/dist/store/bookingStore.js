class BookingStore {
    constructor() {
        this.listeners = new Set();
        this.state = {
            info: "当前后端尚未开放住客预订与订单查询接口，页面先保留接入位。",
        };
    }
    subscribe(listener) {
        this.listeners.add(listener);
        return () => this.listeners.delete(listener);
    }
    getState() {
        return this.state;
    }
    setInfo(info) {
        this.state = { info };
        for (const listener of this.listeners) {
            listener();
        }
    }
}
export const bookingStore = new BookingStore();
//# sourceMappingURL=bookingStore.js.map