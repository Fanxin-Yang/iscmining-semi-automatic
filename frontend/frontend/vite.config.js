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
// export default defineConfig(({ command, mode }) => {
//   console.log(mode);
//   if (command === "serve") {
//     return {
//       // base: "https://lehre.bpm.in.tum.de/ports/8051/",
//       // dev specific config
//       plugins: [vue()],
//       // resolve: {
//       //   alias: {
//       //     "@": fileURLToPath(new URL("./src", import.meta.url)),
//       //   },
//       // },
//       server: {
//         // host: "localhost",
//         // port: 8051,
//         // strictPort: true,
//         // open: true,
//         // proxy: {
//         //   "/ports/8051/.**": {
//         //     rewrite: (path) => path.replace("/ports/8051", ""),
//         //   },
//         // },
//         // origin: "http://127.0.0.1:3000",
//       },
//       build: {},
//     };
//   } else if (command === "build") {
//     return {
//       // build specific config
//       base: "/iscmining-semi-automatic/",
//       plugins: [vue()],
//     };
//   }
// });
