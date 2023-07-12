import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";

export function fetchSurveys() {
  return axios.get(`${BASE_URL}/quizzes/`);
}

export function fetchSurvey(surveyId) {
  return axios.get(`${BASE_URL}/quizzes/${surveyId}/`);
}

export function saveSurveyResponse(surveyResponse) {
  return axios.put(`${BASE_URL}/quizzes/${surveyResponse.id}/`, surveyResponse);
}

export function postNewSurvey(survey) {
  return axios.post(`${BASE_URL}/quizzes/`, survey);
}
