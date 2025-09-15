import api from "../axios";
import { LoginPayload } from "@/types/auth";

export const setTokens = (access: string, refresh: string) => {
   localStorage.setItem("token", access);
   localStorage.setItem("refreshToken", refresh);
}

export const getAccessToken = () => localStorage.getItem("token");
export const getRefreshToken = () => localStorage.getItem("refresh_token");

export const clearTokens = () => {
   localStorage.removeItem("access_token");
   localStorage.removeItem("refresh_token");
}

export const login = async (payload: LoginPayload) => {
  const { data } = await api.post("/auth/login", payload);
  return data;
};
