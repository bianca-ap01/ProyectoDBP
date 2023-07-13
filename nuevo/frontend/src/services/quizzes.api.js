import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/quizzes";

// export function fetchSurveys() {
//   return axios.get(BASE_URL);
// }

const CONFIG = {
  headers: {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": localStorage.getItem("TOKEN"),
  },
};

export const fetchSurvey = async (surveyId) => {
  try {
    const { data } = axios.get(`/${BASE_URL}/${surveyId}`, CONFIG);
    return data;
  } catch (error) {
    console.log("error here", error);
  }
};

export const saveSurveyResponse = async (surveyResponse) => {
  try {
    const { data } = await axios.put(
      `/${BASE_URL}/${surveyResponse.id}`,
      surveyResponse,
      CONFIG
    );
    return data;
  } catch (error) {
    console.log("error here:", error);
  }
};

export const postNewSurvey = async (survey) => {
  try {
    const { data } = await axios.post(`${BASE_URL}`, survey, CONFIG);
    return data;
  } catch (error) {
    console.log("error here:", error);
  }
};

export const fetchSurveys = async () => {
  try {
    const { data } = await axios.get(BASE_URL, CONFIG);
    console.log("data: ", data);
    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
};
