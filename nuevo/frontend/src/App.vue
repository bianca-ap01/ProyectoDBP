<template>
  <div class="app-container">
    <div class="menu">
      <NavigationBar />
    </div>
    <router-view />
  </div>
</template>

<script>
import axios from "axios";

import NavigationBar from "@/views/Navigation.vue";
export default {
  name: "App",
  components: {
    NavigationBar,
  },

  async created() {
    const response = await axios.get(
      "http://127.0.0.1:5000/usuarios/" + localStorage.getItem("TOKEN")
    );
    this.$store.dispatch("user", response);
    console.log(this.user);
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
