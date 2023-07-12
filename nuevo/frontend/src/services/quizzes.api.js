import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/quizzes";

export function fetchSurveys() {
  return axios.get(BASE_URL);
}

export function fetchSurvey(surveyId) {
  return axios.get(`${BASE_URL}/${surveyId}/`);
}

export function saveSurveyResponse(surveyResponse) {
  return axios.put(`${BASE_URL}/${surveyResponse.id}/`, surveyResponse);
}

export function postNewSurvey(survey) {
  return axios.post(`${BASE_URL}/`, survey);
}

// export const fetchSurvey = async (user) => {
//   try {
//     const { data } = await axios.get(BASE_URL, user);
//     console.log("data: ", data);

//     return data;
//   } catch (error) {
//     console.log("error here: ", error);
//   }
// };
