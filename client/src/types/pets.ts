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