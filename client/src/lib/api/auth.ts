import api from "../axios";
import { LoginPayload, ResetPasswordPayload } from "@/types/auth";

export const setTokens = (access: string, refresh: string) => {
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
};

export const getAccessToken = () => localStorage.getItem("access_token");
export const getRefreshToken = () => localStorage.getItem("refresh_token");

export const clearTokens = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
};

export const login = async (payload: LoginPayload) => {
  const { data } = await api.post("/auth/login", payload);
  return data;
};

export const resetPassword = async(payload: ResetPasswordPayload) => {
   const { data } = await api.post("/auth/request-reset-password", payload);
   return data;
}
