// import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(({ command, mode }) => {
  console.log(mode);
  if (command === "serve") {
    return {
      base: "http://131.159.56.59:8051/",
      // dev specific config
      plugins: [vue()],
      // resolve: {
      //   alias: {
      //     "@": fileURLToPath(new URL("./src", import.meta.url)),
      //   },
      // },
      server: {
        host: "[::1]",
        port: 8051,
        // strictPort: true,
        // open: true,
        // proxy: {},
        // origin: "http://127.0.0.1:3000",
      },
      build: {},
    };
  } else if (command === "build") {
    return {
      // build specific config
      base: "/iscmining-semi-automatic/",
      plugins: [vue()],
    };
  }
});
