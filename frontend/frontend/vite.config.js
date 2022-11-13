// import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  // base: "/ports/8765/",
  server: {
    port: 3000,
    host: true,
  },
  plugins: [vue()],
});
