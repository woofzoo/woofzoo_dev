import { PetPayload } from "@/types/pets";
import api from "../axios";
import { GetType } from "@/types/global";

export const addPet = async (payload: PetPayload) => {
  const { data } = await api.post(`/pets/`, payload);
  return data;
};

export const petTypes = async () => {
  const { data } = await api.get(`/pet-types`);
  return data;
};

export const getBreedTypeByPetCategory = async (pet_type: string) => {
  const { data } = await api.get(`/pet-types/${pet_type}/breeds`);

  return data;
};

export const getAllPets = async (payload: GetType) => {
  const { data } = await api.get(`/pets`);
  console.log(data);
  return data;
};

export default {
  addPet,
};
