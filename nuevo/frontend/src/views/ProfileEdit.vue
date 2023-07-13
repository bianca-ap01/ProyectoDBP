<template>
  <h1 class="title">Actualizar datos</h1>
  <div v-if="!isUpdated">
    <form @submit.prevent.stop="updateEvent" class="form">
      <div>
        <label>Apodo: </label>
        <input type="text" v-model="user_C.nickname" />
      </div>
      <div>
        <label>Correo: </label>
        <input type="text" v-model="user_C.email" />
      </div>
      <div>
        <label>Usuario de AtCoder: </label>
        <input type="text" v-model="user_C.atcoder_handle" />
      </div>
      <div>
        <label>Usuario de VJudge: </label>
        <input type="text" v-model="user_C.vjudge_handle" />
      </div>
      <div>
        <label>Usuario de codeforces: </label>
        <input type="text" v-model="user_C.codeforces_handle" />
      </div>
      <button type="submit">Actualizar</button>
    </form>
    <div class="user-message-errors" v-if="errorLists.length > 0">
      <ul>
        <li v-for="error in errorLists" :key="error">{{ error }}</li>
      </ul>
    </div>
  </div>

  <div v-else>
    <span class="user-message-success">Actualización existosa</span>
  </div>
</template>

<script>
import { updateUser } from "@/services/users.api";
export default {
  name: "ProfileEdit",
  data() {
    return {
      errorLists: [],
      user_C: {
        nickname: "",
        email: "",
        codeforces_handle: "",
        vjudge_handle: "",
        atcoder_handle: "",
      },
      isUpdated: false,
    };
  },
  methods: {
    async updateEvent() {
      const {
        errors = [],
        success,
        user,
        message,
      } = await updateUser(this.user_C);
      if (success) {
        this.isUpdated = true;
        localStorage.setItem("user", user);
        this.$store.dispatch("user", user);
        console.log(message);

        setTimeout(() => {
          this.$router.push("/profile");
        }, 2000);
      } else {
        this.errorLists = errors;
        console.log(message);
      }
    },
  },
};
</script>
