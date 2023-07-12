import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    user: localStorage.getItem("user"),
  },
  getters: {
    user: (state) => {
      return state.user;
    },
  },
  mutations: {
    user(state, user) {
      state.user = user;
    },
  },
  actions: {
    user(context, user) {
      context.commit("user", user);
    },
  },
  modules: {},
  plugins: [createPersistedState()],
});
