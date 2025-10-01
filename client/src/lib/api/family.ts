import { familyPayload } from "@/types/family";
import api from "../axios";

export const addFamily = async (
  payload: familyPayload,
  admin_owner_id: string
) => {
  const url = `/families?admin_owner_id=${admin_owner_id}`;
  const { data } = await api.post(url, payload);
  return data;
};

export const getFamily = async () => {
  const { data } = await api.get(`/families`);
  return data;
};
