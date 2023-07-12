import { createStore } from "vuex";

import {
  fetchSurveys,
  fetchSurvey,
  saveSurveyResponse,
  postNewSurvey,
} from "@/services/quizzes.api";

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
    // isolated data mutations
    setSurveys(state, payload) {
      state.surveys = payload.surveys;
    },
    setSurvey(state, payload) {
      const nQuestions = payload.survey.questions.length;
      for (let i = 0; i < nQuestions; i++) {
        payload.survey.questions[i].choice = null;
      }
      state.currentSurvey = payload.survey;
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
  getters: {},
});

export default store;
