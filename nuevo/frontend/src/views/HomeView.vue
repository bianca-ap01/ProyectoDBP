<template>
  <div v-if="this.$store.state.isLogged == false">
    <h1>Placeholder</h1>
    <span
      >Por favor <router-link to="/signup">Regístrese</router-link> o
      <router-link to="/login">Ingrese</router-link></span
    >
  </div>
  <div v-else>
    <h1>Bienvenido {{ this.$store.state.username }}</h1>
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
