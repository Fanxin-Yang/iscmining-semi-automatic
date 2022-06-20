import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/dataset",
      name: "dataset",
      component: () => import("../views/DatasetView.vue"),
    },
    {
      path: "/:dataSet",
      name: "one",
      component: () => import("../views/PreprocessView.vue"),
    },
    {
      path: "/:dataSet/:csv",
      name: "discovery",
      component: () => import("../views/DiscoveryView.vue"),
    },
  ],
  sensitive: true,
  strict: true,
});

export default router;
