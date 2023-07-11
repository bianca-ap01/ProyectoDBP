import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/usuarios";

export const signUp = async (user) => {
  try {
    const { data } = await axios.post(BASE_URL, user);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
};

export const logIn = async (user) => {
  try {
    const { data } = await axios.post(
      "http://127.0.0.1:5000/usuarios/login",
      user
    );
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
};

export const getUser = async (token) => {
  try {
    const { data } = await axios.post(BASE_URL, token);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
};
