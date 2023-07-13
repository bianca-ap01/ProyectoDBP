import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/usuarios";

const CONFIG = {
  headers: {
    "Content-Type": "application/json",
    "X-ACCESS-TOKEN": localStorage.getItem("TOKEN"),
  },
};

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

export const updateUser = async (user) => {
  try {
    const { data } = await axios.patch(BASE_URL, user, CONFIG);
    console.log("data: ", data);

    return data;
  } catch (error) {
    console.log("error here: ", error);
  }
};
