import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    isLogged: false,
    username: "",
  },
  getters: {},
  mutations: {
    isLogged(state) {
      state.isLogged = true;
    },
    setUsername(state, username) {
      state.username = username;
    },
  },
  actions: {},
  modules: {},
  plugins: [createPersistedState()],
});
