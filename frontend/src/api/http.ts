import axios from "axios";

// 1. 创建 axios 实例
const http = axios.create({
  baseURL: "/api",
  timeout: 10000,
});

// 2. 请求拦截器（统一加 token）
http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// 3. 响应拦截器（可选：统一处理401）
http.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default http;