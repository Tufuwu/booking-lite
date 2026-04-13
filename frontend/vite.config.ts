import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from 'node:url'; // 使用原生 url 模块，无需安装额外依赖

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // 这种方式不需要 path 模块，直接利用 URL 对象处理路径
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000', // 统一指向 127.0.0.1
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''), // 转发时不带 /api 前缀
        }
      }
    }
});