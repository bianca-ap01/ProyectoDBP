<template>
  <div class="app-container">
    <div class="menu">
      <NavigationBar />
    </div>
    <router-view />
  </div>
</template>

<script>
//import axios from "axios";

import NavigationBar from "@/views/Navigation.vue";
export default {
  name: "App",
  components: {
    NavigationBar,
  },
  watch() {
    if (
      localStorage.getItem("TOKEN") != null ||
      localStorage.getItem("user") != null
    ) {
      this.user = localStorage.getItem("user");
      this.$store.dispatch("user", this.user);
    } else {
      this.$router.push("/");
    }
  },
  // async created() {
  //   this.user = localStorage.getItem("user");
  //   if (localStorage.getItem("TOKEN") == null) {
  //     console.log(this.user);
  //   } else {
  //     // const response = await axios.get(
  //     //   "http://127.0.0.1:5000/usuarios" + "/" + localStorage.getItem("TOKEN")
  //     // );
  //     this.$store.dispatch("user", this.user);
  //     console.log(this.user);
  //     this.user = localStorage.getItem("user");
  //   }
  // },
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
