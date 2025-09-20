import { PetOwnerPayload } from "@/types/auth";
import api from "../axios";

export const addPetOwner = async (payload: PetOwnerPayload) => {
  const { data } = await api.post("/owners", payload);
  console.log(data);
  return data;
};
