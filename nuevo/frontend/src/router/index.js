import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/signup",
    name: "signup",
    component: () =>
      import(/* webpackChunkName: "signup" */ "../views/SignUpView.vue"),
  },

  {
    path: "/login",
    name: "login",
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/LogInView.vue"),
  },

  {
    path: "/dashboard",
    name: "dashboard",
    component: () =>
      import(/* webpackChunkName: "dashboard" */ "../views/DashboardView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
