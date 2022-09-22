// import { fileURLToPath, URL } from "url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(({ command, mode }) => {
  console.log(mode);
  if (command === "serve") {
    console.log("serve");
    return {
      // base: "https://lehre.bpm.in.tum.de/ports/8051/",
      // dev specific config
      plugins: [vue()],
      // resolve: {
      //   alias: {
      //     "@": fileURLToPath(new URL("./src", import.meta.url)),
      //   },
      // },
      server: {
        host: "0.0.0.0",
        // port: 3000,
        strictPort: true,
        // open: true,
        proxy: {
          "/test": {
            target: "https://lehre.bpm.in.tum.de/ports/8051/",
            changeOrigin: true,
            rewrite: (path) => path.replace(/^\/test/, ""),
          },
        },
        // origin: "http://127.0.0.1:3000",
      },
      build: {},
    };
  } else if (command === "build") {
    console.log("build");
    return {
      // build specific config
      base: "/iscmining-semi-automatic/",
      plugins: [vue()],
    };
  }
});
