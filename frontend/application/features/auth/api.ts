import axios from "axios";
import { SignupUser } from "./types";

export const fetchAsyncLoginUser = async (number: string, password: string) => {
  try {
    const response = await axios.post(
      `http://localhost:8000/api/auth/login/`,
      {
        number,
        password,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
    return response.data;
  } catch (error: any) {
    throw error.response.data;
  }
};

export const fetchAsyncLogoutUser = async () => {
  try {
    await axios.post(
      `http://localhost:8000/api/auth/logout/`,
      {}, // 空のPOSTリクエストを使用
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    );
  } catch (error: any) {
    throw error.response.data;
  }
};

export const fetchAsyncTokenVerify = async () => {
  const response = await axios.post(
    "http://localhost:8000/api/auth/verify/",
    {},
    {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    }
  );
  return response.data;
};

export const fetchAsyncTokenRefresh = async () => {
  await axios.post(
    "http://localhost:8000/api/auth/refresh/",
    {},
    {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    }
  );
};

export const fetchAsyncSignup = async (props: SignupUser) => {
  const formedData = {
    name: props.name,
    number: props.number,
    password: props.password,
  };
  await axios.post("http://localhost:8000/api/auth/users/", formedData, {
    headers: {
      "Content-Type": "application/json",
    },
    withCredentials: true,
  });
};
