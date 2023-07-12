<template>
  <h1>Perfil</h1>
  <div>
    <div>
      Nombre de usuario:
      {{ user.nickname }}
    </div>
    <div>
      Correo electrónico:
      {{ user.email }}
    </div>

    <div>
      Usuario de codeforces:
      {{ user.codeforces_handle }}
    </div>
    <div>
      Usuario de VJudge:
      {{ user.vjudge_handle }}
    </div>
    <div>
      Usuario de AtCoder:
      {{ user.atcoder_handle }}
    </div>
    <div>
      Fecha de registro:
      {{ user.created_at }}
    </div>
  </div>
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
