<template>
  <div v-if="!isLogged">
    <h1>Placeholder</h1>
    <span
      >Por favor <router-link to="/signup">Regístrese</router-link> o
      <router-link to="/login">Ingrese</router-link></span
    >
  </div>
  <div v-if="isLogged">
    <h1>Bienvenido {{ user.nickname }}</h1>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
// import { getUser } from "@/services/users.api";
export default {
  name: "HomeView",
  computed: {
    ...mapGetters(["user", "isLogged"]),
  },
};
</script>

<style></style>
