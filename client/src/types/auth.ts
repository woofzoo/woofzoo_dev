export interface LoginPayload {
  email: string;
  password: string;
}

export interface ResetPasswordPayload {
  email: string;
}

export interface PetOwnerPayload {
  name: string;
  email: string;
  phone_number: string;
  address: string;
}
