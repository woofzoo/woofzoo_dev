import { familyPayload } from "@/types/family";
import api from "../axios";

export const addFamily = async (payload: familyPayload, owner_id: string) => {
  const { data } = await api.post(`/families/?owner_id=${owner_id}`, payload);
  return data;
};

export const getFamily = async () => {
  const { data } = await api.get(`/families`);
  return data;
};
