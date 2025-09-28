import { familyPayload } from "@/types/family";
import api from "../axios";

export const addFamily = async (payload: familyPayload, owner_id: string) => {
  const url = `/families?owner_id=${owner_id}`;
  console.log("API URL:", url); // This will show you the exact endpoint
  console.log(
    "Full URL:",
    `${process.env.NEXT_PUBLIC_APP_URL || "http://localhost:8000/api"}${url}`
  );

  const { data } = await api.post(url, payload);
  return data;
};

export const getFamily = async () => {
  const { data } = await api.get(`/families`);
  return data;
};
