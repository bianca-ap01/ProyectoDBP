<template>
  <div>
    <h1 class="title">Log In</h1>
    <div v-if="!isUserSubmitted">
      <form @submit.prevent.stop="logInEvent" class="form">
        <div class="form-group">
          <label class="label">Nombre de usuario:</label>
          <input type="text" v-model="user_C.nickname" class="input" />
        </div>
        <div class="form-group">
          <label class="label">Contraseña:</label>
          <input type="password" v-model="user_C.password" class="input" />
        </div>
        <button class="submit-button" type="submit">Submit</button>
      </form>

      <div class="user-message-errors" v-if="errorLists.length > 0">
        <ul>
          <li v-for="error in errorLists" :key="error">{{ error }}</li>
        </ul>
      </div>
    </div>
    <div v-else>
      <span class="user-message-success">Ingreso existoso</span>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { logIn } from "@/services/users.api";
export default {
  name: "LogIn",
  data() {
    return {
      user_C: {
        nickname: "",
        password: "",
      },
      errorLists: [],
      isUserSubmitted: false,
    };
  },
  methods: {
    async logInEvent() {
      const {
        success,
        token = null,
        errors = [],
        user = null,
      } = await logIn(this.user_C);
      if (success) {
        this.isUserSubmitted = true;
        localStorage.setItem("TOKEN", token);
        localStorage.setItem("user", user);
        this.$store.dispatch("user", user);
        this.$store.dispatch("isLogged", true);
        setTimeout(() => {
          this.$router.push("/");
        }, 2000);
      } else {
        this.errorLists = errors;
      }
    },
  },
  computed: {
    ...mapGetters(["user", "isLogged"]),
  },
};
</script>

<style>
.title {
  text-align: center;
  color: #ff00ff; /* Magenta color */
  font-size: 40px;
  margin-bottom: 30px;
  border-bottom: 5px dotted #00ffff; /* Cyan color */
  padding-bottom: 10px;
}

.form {
  margin: 0 auto;
  max-width: 400px;
  border: 2px dashed #ffff00; /* Yellow color */
  padding: 20px;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #ff00ff; /* Magenta color */
}

.input {
  padding: 10px;
  border: 2px solid #ff00ff; /* Magenta color */
  border-radius: 5px;
  width: 300px;
}

.submit-button {
  background-color: #00ffff; /* Cyan color */
  color: #ff00ff; /* Magenta color */
  padding: 15px 30px;
  border: 2px dashed #00ffff; /* Cyan color */
  border-radius: 10px;
  cursor: pointer;
  font-weight: bold;
  text-transform: uppercase;
}

.user-message-success {
  color: #00ff00; /* Green color */
  font-size: 28px;
  border: 3px double #00ff00; /* Green color */
  padding: 20px;
  border-radius: 20px;
  text-align: center;
}

.user-message-errors {
  color: #ff0000; /* Red color */
  font-size: 24px;
  border: 3px ridge #ff0000; /* Red color */
  padding: 15px;
  border-radius: 10px;
}
</style>
