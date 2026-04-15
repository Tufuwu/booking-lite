import { defineStore } from "pinia";
import axios from "axios";

interface Session {
  jobNumber: string;
}

export const useUserStore = defineStore("user", {
  state: () => ({
    token: localStorage.getItem("token") || "",
    user: null as any,
    roles: [] as string[],
    permissions: [] as string[],
    ready: false
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    role: (state) => state.user?.role,
  },

  actions: {
    // ✅ 统一登录（不分 admin/user API）
    async login(username: string, password: string) {
      try {
        const data = new URLSearchParams()
        data.append("username", username)
        data.append("password", password)

        const res = await axios.post("/api/login", data, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded"
          }
        })

        this.token = res.data.access_token
        localStorage.setItem("token", this.token)

        await this.initAuth()

        return true   // ⭐关键
      } catch (e: any) {
        return false
      }
    },

    // ⭐启动鉴权（核心）
    async initAuth() {
      if (!this.token) {
        this.ready = true
        return
      }

      try {
        const res = await axios.get("/api/users/me", {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })

        this.user = res.data
        this.roles = res.data.role ? [res.data.role.name] : []
        this.permissions =
          (res.data.role?.permissions ?? []).map((p: any) => p.code)
      } catch {
        this.logout()
      } finally {
        this.ready = true
      }
    },

    // ✅ 统一用户信息接口
    async fetchMe() {
      const res = await axios.get("/api/users/me", {
        headers: {
          Authorization: `Bearer ${this.token}`,
        },
      });

      this.user = res.data;
      console.log("用户信息已更新:", this.user);
      return res.data;
    },

    logout() {
      this.token = ""
      this.user = null
      this.roles = []
      this.permissions = []
      localStorage.removeItem("token")
    }
  },
});