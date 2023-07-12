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
    surveys: [],
    currentSurvey: {},
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
    setChoice(state, payload) {
      const { questionId, choice } = payload;
      const nQuestions = state.currentSurvey.questions.length;
      for (let i = 0; i < nQuestions; i++) {
        if (state.currentSurvey.questions[i].id === questionId) {
          state.currentSurvey.questions[i].choice = choice;
          break;
        }
      }
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
    // asynchronous operations
    loadSurveys(context) {
      return fetchSurveys().then((response) => {
        context.commit("setSurveys", { surveys: response.data });
      });
    },
    loadSurvey(context, { id }) {
      return fetchSurvey(id).then((response) => {
        context.commit("setSurvey", { survey: response.data });
      });
    },
    addSurveyResponse(context) {
      return saveSurveyResponse(context.state.currentSurvey);
    },
    submitNewSurvey(context, survey) {
      return postNewSurvey(survey, context);
    },
  },
});
