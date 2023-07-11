import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/opciones";

export const createOption = async (payload) => {
  try {
    const { data } = await axios.post(BASE_URL, payload);
    console.log("data", data);

    return data;
  } catch (error) {
    console.log("Error here:", here);
  }
};

export const getOptions = async (payload) => {
  try {
    const { data } = await axios.get(BASE_URL, payload);
    console.log("data", data);

    return data;
  } catch (error) {
    console.log("Error here:", here);
  }
};

// export const modifyOption = async (payload) => {
//   try {
//     const { data } = await axios.patch(BASE_URL + "/{id}", payload);
//     console.log("data", data);

//     return data;
//   } catch (error) {
//     console.log("Error here:", here);
//   }
// };

// export const deleteOption = async (payload) => {
//   try {
//     const { data } = await axios.delete(BASE_URL + "/{id}", payload);
//     console.log("data", data);

//     return data;
//   } catch (error) {
//     console.log("Error here:", here);
//   }
// };
