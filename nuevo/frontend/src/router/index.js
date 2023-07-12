import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SolveQuiz from "@/components/SolveQuiz";
import CrearQuiz from "@/components/CrearQuiz";
import SignUp from "../views/SignUpView.vue";
import Login from "../views/LogInView.vue";
import Dashboard from "../views/DashboardView.vue";
import Profile from "../views/ProfileView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/quizzes/:id",
    name: "Survey",
    component: SolveQuiz,
  },
  {
    path: "/quizzes/new",
    name: "NewSurvey",
    component: CrearQuiz,
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUp,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: Dashboard,
  },
  {
    path: "/profile",
    name: "profile",
    component: Profile,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
