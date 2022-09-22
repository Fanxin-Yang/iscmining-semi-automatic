// import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(({ command, mode }) => {
  console.log(mode);
  if (command === "serve") {
    return {
      base: "/ports/8051/",
      // dev specific config
      plugins: [vue()],
      // resolve: {
      //   alias: {
      //     "@": fileURLToPath(new URL("./src", import.meta.url)),
      //   },
      // },
      server: {
        host: "localhost",
        // port: 3000,
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
