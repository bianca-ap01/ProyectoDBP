<template>
  <div v-if="!isLogged">
    <h1>Placeholder</h1>
    <span
      >Por favor <router-link to="/signup">Regístrese</router-link> o
      <router-link to="/login">Ingrese</router-link></span
    >
  </div>
  <div v-else>
    <h1>Bienvenido {falta poner esta Contraseña}</h1>
  </div>
</template>

<script>
// import { getUser } from "@/services/users.api";
export default {
  name: "HomeView",
  components: {},
  // data() {
  //   return {
  //     user: null,
  //   };
  // },
  // async created() {
  //   const { data, success } = await getUser();
  //   if (success) {
  //     this.user = data;
  //   }
  // },
};
</script>

<style></style>
