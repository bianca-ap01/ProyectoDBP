import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";

export default createStore({
  state: {
    user: {
      id: "",
      nickname: "",
      email: "",
      codeforces_handle: "",
      atcoder_handle: "",
      vjudge_handle: "",
      created_at: "",
      modified_at: "",
    },
    isLogged: false,
  },
  getters: {
    user: (state) => {
      return state.user;
    },
    isLogged: (state) => {
      return state.isLogged;
    },
  },
  mutations: {
    user(state, user) {
      state.user = user;
    },

    isLogged(state, log) {
      state.isLogged = log;
    },
  },
  actions: {
    user(context, user) {
      context.commit("user", user);
    },
    isLogged(context, isLogged) {
      context.commit("isLogged", isLogged);
    },
  },
  modules: {},
  plugins: [createPersistedState()],
});
