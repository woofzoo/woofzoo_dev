import { GetType, PetOwnerPayload } from "@/types/auth";
import api from "../axios";

export const addPetOwner = async (payload: PetOwnerPayload) => {
  const { data } = await api.post("/owners", payload);
  return data;
};

export const getPetOwners = async (payload: GetType) => {
  const { data } = await api.get("/owners", {
    params: {
      skip: payload.skip,
      limit: payload.limit,
    },
  });
  console.log(data);
  return data;
};
