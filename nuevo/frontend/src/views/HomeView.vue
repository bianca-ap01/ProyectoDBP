<template>
  <div v-if="!user">
    <h1>Placeholder</h1>
    <span
      >Por favor <router-link to="/signup">Regístrese</router-link> o
      <router-link to="/login">Ingrese</router-link></span
    >
  </div>
  <div v-if="user">
    <h1>Bienvenido {{ user.nickname }}</h1>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
// import { getUser } from "@/services/users.api";
export default {
  name: "HomeView",
  computed: {
    ...mapGetters(["user"]),
  },
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
