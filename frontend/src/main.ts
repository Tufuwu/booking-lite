import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"
import { useUserStore } from "@/store/user"

import "./router/permission"

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)

async function bootstrap() {
  const userStore = useUserStore()

  // ⭐关键：启动时身份校验
  await userStore.initAuth()
  app.use(router)
  app.mount("#app")

}

bootstrap()