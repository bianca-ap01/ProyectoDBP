import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import SolveQuiz from "@/components/SolveQuiz";
import CrearQuiz from "@/components/CrearQuiz";
import SignUp from "../views/SignUpView.vue";
import Login from "../views/LogInView.vue";
import Profile from "../views/ProfileView.vue";
import QuizHome from "@/components/QuizHome";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/quizzes",
    name: "Surveys",
    component: QuizHome,
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
    component: () =>
      import(/* webpackChunkName: "dashboard" */ "../views/DashboardView.vue"),
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
