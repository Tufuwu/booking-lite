import { defineStore } from "pinia";
import axios from "axios";

interface Session {
  jobNumber: string;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    session: null as Session | null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.session,
  },
  actions: {
    async login(name: string, pass: string) {
      try {
        const params = new URLSearchParams();
        params.append("username", name);
        params.append("password", pass);

        await axios.post("/api/admin/login", params, {
          withCredentials: true,
        });

        const user = await this.fetchMe();

        return user;
      } catch (error: any) {
        return null;
      }
    },
    async fetchMe() {
      const res = await axios.get("/api/admins/me", {
        withCredentials: true,
      });

      this.session = res.data;
      return res.data;
    },
    logout() {
      this.session = null;
    },
  },
});