<template>
  <h1>Perfil</h1>
  <div>
    <button><router-link to="/profile/edit">Editar perfil</router-link></button>
  </div>
  <table class="profile-table">
    <tr>
      <td>Nombre de usuario:</td>
      <td>{{ user.nickname }}</td>
    </tr>
    <tr>
      <td>Correo electrónico:</td>
      <td>{{ user.email }}</td>
    </tr>
    <tr>
      <td>Usuario de codeforces:</td>
      <td>{{ user.codeforces_handle }}</td>
    </tr>
    <tr>
      <td>Usuario de VJudge:</td>
      <td>{{ user.vjudge_handle }}</td>
    </tr>
    <tr>
      <td>Usuario de AtCoder:</td>
      <td>{{ user.atcoder_handle }}</td>
    </tr>
    <tr>
      <td>Fecha de registro:</td>
      <td>{{ user.created_at }}</td>
    </tr>
    <tr>
      <td>Última modificación:</td>
      <td>{{ user.modified_at }}</td>
    </tr>
  </table>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "ProfileView",
  computed: {
    ...mapGetters(["user"]),
  },
};
</script>

<style>
.profile-table {
  width: 100%;
  border-collapse: collapse;
}

.profile-table td {
  padding: 10px;
  border: 1px solid #f16c6c;
}

.profile-table td:first-child {
  font-weight: bold;
  background-color: #f85d5d;
}

.profile-table tr:last-child td {
  border-bottom: none;
}
</style>
