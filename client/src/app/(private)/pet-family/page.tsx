'use client';

import { useEffect, useState } from 'react';
import DashLayout from '@/components/layout/DashLayout';
import Input from '@/components/ui/Input'; // Your existing Input component
import { CustomSelect } from '@/components/ui/CustomSelect'; // Import your CustomSelect component
import { PlayfairDisplay } from '@/components/ui/Fonts/Font';
import { addFamily, getFamily } from '@/lib/api/family';
import { useAuth } from '@/context/AuthContext';
import { getPetOwners } from '@/lib/api/owners';

interface FormData {
   name: string;
   description: string;
   owner_id: string; // Added owner_id field
}

interface FormErrors {
   name?: string;
   description?: string;
   owner_id?: string; // Added owner_id error field
}

interface CreatedFamily {
   created_at: string;
   description: string;
   id: string;
   name: string;
   owner_id: string;
   updated_at: string;
}

interface PetOwner {
   id: string;
   name: string;
   email: string;
   phone_number: string;
   address: string;
   is_active: boolean;
   created_at: string;
   updated_at: string;
}

const Page: React.FC = () => {
   const [formData, setFormData] = useState<FormData>({
      name: '',
      description: '',
      owner_id: '' // Initialize owner_id
   });
   const [errors, setErrors] = useState<FormErrors>({});
   const [isLoading, setIsLoading] = useState(false);
   const [isSubmitted, setIsSubmitted] = useState(false);
   const [createdFamily, setCreatedFamily] = useState<CreatedFamily | null>(null);
   const [petOwners, setPetOwners] = useState<PetOwner[]>([]);

   const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
      const { name, value } = e.target;
      setFormData(prev => ({
         ...prev,
         [name]: value
      }));

      // Clear error when user starts typing
      if (errors[name as keyof FormErrors]) {
         setErrors(prev => ({
            ...prev,
            [name]: ''
         }));
      }
   };

   // Handle select change for owner selection
   const handleSelectChange = (e: { target: { name: string; value: string } }) => {
      const { name, value } = e.target;
      setFormData(prev => ({
         ...prev,
         [name]: value
      }));

      // Clear error when user selects an option
      if (errors[name as keyof FormErrors]) {
         setErrors(prev => ({
            ...prev,
            [name]: ''
         }));
      }
   };

   const validateForm = (): boolean => {
      const newErrors: FormErrors = {};

      if (!formData.name.trim()) {
         newErrors.name = 'Family name is required';
      } else if (formData.name.trim().length < 2) {
         newErrors.name = 'Family name must be at least 2 characters';
      }

      if (!formData.description.trim()) {
         newErrors.description = 'Description is required';
      } else if (formData.description.trim().length < 10) {
         newErrors.description = 'Description must be at least 10 characters';
      }

      if (!formData.owner_id.trim()) {
         newErrors.owner_id = 'Please select a pet owner';
      }

      setErrors(newErrors);
      return Object.keys(newErrors).length === 0;
   };

   const simulateAPICall = (): Promise<CreatedFamily> => {
      return new Promise((resolve) => {
         setTimeout(() => {
            const mockResponse: CreatedFamily = {
               created_at: new Date().toISOString(),
               description: formData.description,
               id: '123e4567-e89b-12d3-a456-426614174000',
               name: formData.name,
               owner_id: formData.owner_id,
               updated_at: new Date().toISOString()
            };
            resolve(mockResponse);
         }, 2000);
      });
   };

   const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();

      if (!validateForm()) {
         return;
      }

      setIsLoading(true);

      try {
         const { owner_id, ...bodyData } = formData;
         const response = await addFamily(bodyData, owner_id);
         setCreatedFamily(response);
         setIsSubmitted(true);
         setFormData({ name: '', description: '', owner_id: '' });
      } catch (error) {
         console.error('Error creating family:', error);
      } finally {
         setIsLoading(false);
      }
   };

   const handleCreateAnother = () => {
      setIsSubmitted(false);
      setCreatedFamily(null);
      setErrors({});
   };

   const handleReset = () => {
      setFormData({ name: '', description: '', owner_id: '' });
      setErrors({});
   };

   useEffect(() => {
      const getFamilyIfCreated = async () => {
         const data = await getFamily();
         console.log(data);
         setCreatedFamily(data);
      };
      const getOwners = async () => {
         const data = await getPetOwners({ skip: 0, limit: 10 });
         setPetOwners(data?.owners || []);
      }
      getFamilyIfCreated();
      getOwners();
   }, []);

   // Transform petOwners data for CustomSelect component
   const ownerOptions = petOwners.map(owner => ({
      value: owner.id,
      label: owner.name
   }));

   // Get selected owner's name for display in success screen
   const selectedOwnerName = petOwners.find(owner => owner.id === createdFamily?.owner_id)?.name || '';

   if (isSubmitted && createdFamily) {
      return (
         <DashLayout>
            <div className="p-6">
               <div className="max-w-2xl mx-auto">
                  <div className="bg-background-primary rounded-xl shadow-xl border border-border-primary overflow-hidden">
                     {/* Success Header */}
                     <div className="bg-gradient-to-r from-success to-success/80 px-8 py-6">
                        <div className="flex items-center gap-3">
                           <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                              </svg>
                           </div>
                           <div>
                              <h2 className={`${PlayfairDisplay.className} text-2xl font-bold text-white`}>
                                 Family Created Successfully!
                              </h2>
                              <p className="text-white/90 mt-1">
                                 Your family profile has been created and is ready to use.
                              </p>
                           </div>
                        </div>
                     </div>

                     {/* Family Details */}
                     <div className="p-8">
                        <div className="bg-background-secondary rounded-lg p-6 border border-border-secondary">
                           <h3 className={`${PlayfairDisplay.className} text-xl font-semibold text-text-primary mb-4`}>
                              Family Details
                           </h3>

                           <div className="space-y-4">
                              <div>
                                 <label className="text-sm font-medium text-text-secondary">Family Name</label>
                                 <p className="text-text-primary font-semibold mt-1">{createdFamily.name}</p>
                              </div>

                              <div>
                                 <label className="text-sm font-medium text-text-secondary">Description</label>
                                 <p className="text-text-primary mt-1">{createdFamily.description}</p>
                              </div>

                              <div>
                                 <label className="text-sm font-medium text-text-secondary">Pet Owner</label>
                                 <p className="text-text-primary font-semibold mt-1">{selectedOwnerName}</p>
                              </div>

                              <div>
                                 <label className="text-sm font-medium text-text-secondary">Family ID</label>
                                 <p className="text-text-muted font-mono text-sm mt-1">{createdFamily.id}</p>
                              </div>

                              <div>
                                 <label className="text-sm font-medium text-text-secondary">Created</label>
                                 <p className="text-text-muted text-sm mt-1">
                                    {new Date(createdFamily.created_at).toLocaleString()}
                                 </p>
                              </div>
                           </div>
                        </div>

                        <div className="flex gap-4 mt-8">
                           <button
                              onClick={handleCreateAnother}
                              className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-md bg-primary text-text-inverse hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 shadow-md hover:shadow-lg transition-all duration-200"
                           >
                              Create Another Family
                           </button>
                           <button
                              className="inline-flex items-center justify-center px-6 py-3 text-base font-medium rounded-md border-2 border-primary text-primary hover:bg-primary hover:text-text-inverse focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-all duration-200"
                           >
                              View All Families
                           </button>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </DashLayout>
      );
   }

   return (
      <DashLayout>
         <div className="p-6">
            <div className="max-w-2xl mx-auto">
               <div className="bg-background-primary rounded-xl shadow-xl border border-border-primary overflow-hidden">
                  {/* Header */}
                  <div className="bg-primary/80 px-8 py-6">
                     <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center">
                           <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                           </svg>
                        </div>
                        <div>
                           <h1 className={`${PlayfairDisplay.className} text-3xl font-bold text-white`}>
                              Create New Family
                           </h1>
                           <p className="text-white/90 mt-1">
                              Set up a new family profile for your veterinary practice
                           </p>
                        </div>
                     </div>
                  </div>

                  {/* Form */}
                  <div className="p-8">
                     <div className="space-y-6">
                        <Input
                           label="Family Name"
                           buttonType="text"
                           name="name"
                           value={formData.name}
                           onChange={handleInputChange}
                           placeholder="Enter family name (e.g., Smith Family)"
                           required
                        />
                        {errors.name && (
                           <p className="text-sm text-error font-medium -mt-4">{errors.name}</p>
                        )}

                        <div className="flex flex-col gap-2">
                           <label className={`${PlayfairDisplay.className} text-sm font-medium text-gray-900`}>
                              Description
                           </label>
                           <textarea
                              name="description"
                              value={formData.description}
                              onChange={handleInputChange}
                              placeholder="Describe this family (e.g., Our beloved pets family)"
                              rows={4}
                              className="w-full border border-border-primary rounded-md focus:outline-none focus:ring-2 focus:ring-primary-pastel bg-background-primary text-text-primary placeholder-text-muted px-4 py-2 text-base transition-all duration-200 resize-none"
                              required
                           />
                           {errors.description && (
                              <p className="text-sm text-error font-medium">{errors.description}</p>
                           )}
                        </div>

                        {/* Pet Owner Selection */}
                        <CustomSelect
                           label="Select Pet Owner"
                           name="owner_id"
                           value={formData.owner_id}
                           options={ownerOptions}
                           onChange={handleSelectChange}
                           placeholder="Choose a pet owner..."
                           className="bg-background-primary text-text-primary"
                        />
                        {errors.owner_id && (
                           <p className="text-sm text-error font-medium -mt-4">{errors.owner_id}</p>
                        )}

                        <div className="bg-info/10 rounded-lg p-4 border border-info/20">
                           <div className="flex gap-3">
                              <svg className="w-5 h-5 text-info flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              <div className="text-sm text-text-primary">
                                 <p className="font-medium mb-1">Family Profile Information</p>
                                 <p className="text-text-secondary">
                                    This family profile will be used to organize pet records and appointments.
                                    You can add pets to this family after creation.
                                 </p>
                              </div>
                           </div>
                        </div>

                        <div className="flex gap-4 pt-4">
                           <button
                              onClick={handleSubmit}
                              disabled={isLoading}
                              className="flex-1 inline-flex items-center justify-center px-8 py-4 text-lg font-medium rounded-md bg-secondary text-text-inverse hover:bg-secondary/90 focus:outline-none focus:ring-2 focus:ring-secondary focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-md hover:shadow-lg transition-all duration-200 cursor-pointer"
                           >
                              {isLoading && (
                                 <svg className="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                 </svg>
                              )}
                              {isLoading ? 'Creating Family...' : 'Create Family'}
                           </button>
                           <button
                              type="button"
                              onClick={handleReset}
                              className="inline-flex items-center justify-center px-8 py-4 text-lg font-medium rounded-md border-2 border-primary text-primary hover:bg-primary hover:text-text-inverse focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2 transition-all duration-200"
                           >
                              Reset
                           </button>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </DashLayout>
   );
};

export default Page;