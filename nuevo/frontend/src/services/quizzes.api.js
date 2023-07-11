import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/quizzes";

export const createQuiz = async (payload) => {
  try {
    const { data } = await axios.post(BASE_URL, payload);
    console.log("data", data);
  } catch (error) {
    console.log("Error here:", error);
  }
};

export const getAllQuizzes = async (payload) => {
  //   try {
  const { data } = await axios.get(BASE_URL, payload);
  console.log("data", data);
  return data;
  //   } catch (error) {
  //     console.log("Error here:", error);
  //   }
};
