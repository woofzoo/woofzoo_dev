import { PetOwnerPayload } from "@/types/auth";
import api from "../axios";
import { GetType } from "@/types/global";

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

  return data;
};

export const getPetOwnerById = async (id: string) => {
  const { data } = await api.get(`/owners/${id}`);
  return data;
};
