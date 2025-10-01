import api from "../axios";
import { GetType } from "@/types/global";

export const getAllUsers = async (payload: GetType) => {
  const { data } = await api.get("/users", {
    params: {
      skip: payload.skip,
      limit: payload.limit,
    },
  });

  return data;
};
