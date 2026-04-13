type Listener = () => void;

export interface BookingNoticeState {
  info: string;
}

class BookingStore {
  private listeners = new Set<Listener>();

  private state: BookingNoticeState = {
    info: "当前后端尚未开放住客预订与订单查询接口，页面先保留接入位。",
  };

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getState(): BookingNoticeState {
    return this.state;
  }

  setInfo(info: string): void {
    this.state = { info };
    for (const listener of this.listeners) {
      listener();
    }
  }
}

export const bookingStore = new BookingStore();
