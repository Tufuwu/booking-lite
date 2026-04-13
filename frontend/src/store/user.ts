import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    user: null as string | null,
  }),

  actions: {
    login(name: string) {
      this.user = name;
    },
    logout() {
      this.user = null;
    },
  },
});