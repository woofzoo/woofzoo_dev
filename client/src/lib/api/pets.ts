import api from "../axios";

export type PetPayload = {
  name: string;
  age?: number;
  breed?: string;
  gender?: string;
  pet_type?: string;
  owner_id?: string;
  weight?: number;
  photos?: string[];
  emergency_contacts?: any;
  insurance_info?: any;
};

export const addPet = async (payload: PetPayload) => {
  const { data } = await api.post(`/pets/`, payload);
  return data;
};

export const petTypes = async () => {
  const { data } = await api.get(`/pet-types`);
  return data;
};

export default {
  addPet,
};
