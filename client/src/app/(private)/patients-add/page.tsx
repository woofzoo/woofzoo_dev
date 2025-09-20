"use client";

import DashLayout from '@/components/layout/DashLayout';
import Input from '@/components/ui/Input';
import { PlayfairDisplay } from '@/components/ui/Fonts/Font';
import { useToast } from '@/components/toast/ToastProvider';
import React, { FormEvent, useEffect, useState } from 'react';
import { addPet, petTypes } from '@/lib/api/pets';
import { useRouter } from 'next/navigation';

const Page: React.FC = () => {
   const router = useRouter();
   const { showSuccess, showError } = useToast();

   const [form, setForm] = useState({
      name: '',
      age: '',
      breed: '',
      gender: '',
      pet_type: '',
      owner_id: '',
      photos: [''],
      weight: '',
      emergency_contacts: {
         owner: { name: '', phone: '' },
         vet: { name: '', phone: '' },
      },
      insurance_info: { policy_number: '', provider: '' },
   });

   const handleChange = (
      e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
   ) => {
      const { name, value } = e.target;
      setForm((prev) => ({ ...prev, [name]: value }));
   };

   const handleSubmit = async (e: FormEvent) => {
      e.preventDefault();
      try {
         // Basic validation
         if (!form.name || !form.pet_type) {
            showError('Missing fields', 'Please provide a name and type for the pet', 4000);
            return;
         }

         const payload = {
            name: form.name,
            age: Number(form.age) || 0,
            breed: form.breed,
            gender: form.gender,
            pet_type: form.pet_type,
            owner_id: form.owner_id,
            weight: Number(form.weight) || 0,
            photos: Array.isArray(form.photos) ? form.photos.filter(p => p.trim()) : [String(form.photos)].filter(p => p.trim()),
            emergency_contacts: form.emergency_contacts,
            insurance_info: form.insurance_info,
         };

         const res = await addPet(payload as any);
         if (res?.id) {
            showSuccess('Pet added', `${res.name || form.name} was added successfully`, 5000);
            router.push(`/patients-list`);
         } else {
            showSuccess('Pet added', `Saved locally`, 3000);
         }
      } catch (err: any) {
         console.error(err);
         showError('Failed', err?.message || 'Could not add pet', 5000);
      }
   };

   useEffect(() => {
      console.log(petTypes());
   }, []);

   return (
      <DashLayout>
         <div className="p-4 md:p-8 min-h-screen">
            {/* Header */}
            <div className="mb-8">
               <div className="bg-background-secondary rounded-2xl p-6 border border-border-primary shadow-sm">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                     <div>
                        <h1 className={`${PlayfairDisplay.className} text-3xl md:text-4xl font-bold text-primary`}>
                           Add New Patient
                        </h1>
                        <p className="text-text-secondary mt-2 text-base">
                           Create a comprehensive pet profile for clinic records and care management
                        </p>
                     </div>
                     <div className="flex items-center gap-3">
                        <div className="flex items-center gap-2 px-4 py-2 bg-background-primary rounded-xl border border-border-primary">
                           <div className="w-2 h-2 bg-success rounded-full"></div>
                           <span className="text-sm font-medium text-text-primary">Ready to Register</span>
                        </div>
                     </div>
                  </div>
               </div>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
               {/* Main Form */}
               <div className="xl:col-span-2">
                  <form onSubmit={handleSubmit} className="space-y-8">
                     {/* Basic Information Section */}
                     <div className="bg-background-secondary rounded-2xl p-6 md:p-8 border border-border-primary shadow-md">
                        <div className="flex items-center gap-3 mb-6">
                           <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
                              <span className="text-white font-bold">1</span>
                           </div>
                           <h2 className={`${PlayfairDisplay.className} text-2xl font-bold text-text-primary`}>
                              Basic Information
                           </h2>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                           <div className="md:col-span-2">
                              <Input
                                 label="Pet Name *"
                                 buttonType="text"
                                 name="name"
                                 value={form.name}
                                 onChange={handleChange}
                                 placeholder="Enter pet's name"
                                 className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                              />
                           </div>
                           <Input
                              label="Pet Type *"
                              buttonType="text"
                              name="pet_type"
                              value={form.pet_type}
                              onChange={handleChange}
                              placeholder="e.g., Dog, Cat, Bird"
                              className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                           />
                           <Input
                              label="Breed"
                              buttonType="text"
                              name="breed"
                              value={form.breed}
                              onChange={handleChange}
                              placeholder="e.g., Golden Retriever"
                              className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                           />
                           <Input
                              label="Age (years)"
                              buttonType="number"
                              name="age"
                              value={form.age}
                              onChange={handleChange}
                              placeholder="0"
                              min="0"
                              step="0.1"
                              className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                           />
                           <Input
                              label="Weight (kg)"
                              buttonType="number"
                              name="weight"
                              value={form.weight}
                              onChange={handleChange}
                              placeholder="0.0"
                              min="0"
                              step="0.1"
                              className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                           />
                           <Input
                              label="Gender"
                              buttonType="text"
                              name="gender"
                              value={form.gender}
                              onChange={handleChange}
                              placeholder="Male/Female/Other"
                              className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                           />
                           <div className="md:col-span-2">
                              <Input
                                 label="Owner ID"
                                 buttonType="text"
                                 name="owner_id"
                                 value={form.owner_id}
                                 onChange={handleChange}
                                 placeholder="Unique owner identifier"
                                 className='w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all'
                              />
                           </div>
                        </div>
                     </div>

                     {/* Photos Section */}
                     <div className="bg-background-secondary rounded-2xl p-6 md:p-8 border border-border-primary shadow-md">
                        <div className="flex items-center gap-3 mb-6">
                           <div className="w-10 h-10 rounded-xl bg-accent flex items-center justify-center">
                              <span className="text-white font-bold">2</span>
                           </div>
                           <h2 className={`${PlayfairDisplay.className} text-2xl font-bold text-text-primary`}>
                              Photos
                           </h2>
                        </div>

                        <div>
                           <label className={`${PlayfairDisplay.className} text-base font-medium text-text-primary mb-2 block`}>
                              Photo URLs
                           </label>
                           <p className="text-sm text-text-secondary mb-4">
                              Add photo URLs separated by commas for multiple images
                           </p>
                           <textarea
                              name="photos"
                              rows={3}
                              value={Array.isArray(form.photos) ? form.photos.join(',') : String(form.photos)}
                              onChange={(e) => setForm((prev) => ({ ...prev, photos: e.target.value.split(',').map(s => s.trim()).filter(Boolean) }))}
                              className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel resize-none transition-all"
                              placeholder="https://example.com/photo1.jpg, https://example.com/photo2.jpg"
                           />

                           {/* Photo Preview */}
                           {Array.isArray(form.photos) && form.photos.length > 0 && form.photos[0] && (
                              <div className="mt-6">
                                 <h4 className="text-sm font-medium text-text-primary mb-3">Photo Preview</h4>
                                 <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                                    {form.photos.map((photo: string, index: number) => (
                                       photo && (
                                          <div key={index} className="group relative rounded-xl overflow-hidden border-2 border-border-primary bg-background-primary shadow-md hover:shadow-lg transition-all">
                                             <div className="aspect-square">
                                                <img
                                                   src={photo}
                                                   alt={`${form.name || 'Pet'} ${index + 1}`}
                                                   className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                                                   onError={(e) => {
                                                      const target = e.target as HTMLImageElement;
                                                      target.style.display = 'none';
                                                      target.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center bg-background-muted text-text-secondary text-sm">Invalid URL</div>';
                                                   }}
                                                />
                                             </div>
                                             <div className="absolute inset-x-0 bottom-0 bg-black/50 p-2">
                                                <span className="text-white text-xs font-medium">Photo {index + 1}</span>
                                             </div>
                                          </div>
                                       )
                                    ))}
                                 </div>
                              </div>
                           )}
                        </div>
                     </div>

                     {/* Emergency Contacts Section */}
                     <div className="bg-background-secondary rounded-2xl p-6 md:p-8 border border-border-primary shadow-md">
                        <div className="flex items-center gap-3 mb-6">
                           <div className="w-10 h-10 rounded-xl bg-danger flex items-center justify-center">
                              <span className="text-white font-bold">3</span>
                           </div>
                           <h2 className={`${PlayfairDisplay.className} text-2xl font-bold text-text-primary`}>
                              Emergency Contacts
                           </h2>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                           <div className="space-y-4">
                              <h3 className="text-lg font-semibold text-text-primary flex items-center gap-2">
                                 <div className="w-2 h-2 rounded-full bg-primary"></div>
                                 Owner Contact
                              </h3>
                              <div className="space-y-4">
                                 <input
                                    name="emergency_owner_name"
                                    value={form.emergency_contacts?.owner?.name || ''}
                                    onChange={(e) => setForm((prev) => ({
                                       ...prev,
                                       emergency_contacts: {
                                          ...(prev.emergency_contacts || {}),
                                          owner: {
                                             ...(prev.emergency_contacts?.owner || {}),
                                             name: e.target.value
                                          }
                                       }
                                    }))}
                                    placeholder="Owner's full name"
                                    className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all"
                                 />
                                 <input
                                    name="emergency_owner_phone"
                                    value={form.emergency_contacts?.owner?.phone || ''}
                                    onChange={(e) => setForm((prev) => ({
                                       ...prev,
                                       emergency_contacts: {
                                          ...(prev.emergency_contacts || {}),
                                          owner: {
                                             ...(prev.emergency_contacts?.owner || {}),
                                             phone: e.target.value
                                          }
                                       }
                                    }))}
                                    placeholder="Phone number with country code"
                                    className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all"
                                 />
                              </div>
                           </div>

                           <div className="space-y-4">
                              <h3 className="text-lg font-semibold text-text-primary flex items-center gap-2">
                                 <div className="w-2 h-2 rounded-full bg-secondary"></div>
                                 Veterinarian Contact
                              </h3>
                              <div className="space-y-4">
                                 <input
                                    name="emergency_vet_name"
                                    value={form.emergency_contacts?.vet?.name || ''}
                                    onChange={(e) => setForm((prev) => ({
                                       ...prev,
                                       emergency_contacts: {
                                          ...(prev.emergency_contacts || {}),
                                          vet: {
                                             ...(prev.emergency_contacts?.vet || {}),
                                             name: e.target.value
                                          }
                                       }
                                    }))}
                                    placeholder="Veterinarian's name"
                                    className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-secondary-pastel focus:border-secondary-pastel transition-all"
                                 />
                                 <input
                                    name="emergency_vet_phone"
                                    value={form.emergency_contacts?.vet?.phone || ''}
                                    onChange={(e) => setForm((prev) => ({
                                       ...prev,
                                       emergency_contacts: {
                                          ...(prev.emergency_contacts || {}),
                                          vet: {
                                             ...(prev.emergency_contacts?.vet || {}),
                                             phone: e.target.value
                                          }
                                       }
                                    }))}
                                    placeholder="Clinic phone number"
                                    className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-secondary-pastel focus:border-secondary-pastel transition-all"
                                 />
                              </div>
                           </div>
                        </div>
                     </div>

                     {/* Insurance Section */}
                     <div className="bg-background-secondary rounded-2xl p-6 md:p-8 border border-border-primary shadow-md">
                        <div className="flex items-center gap-3 mb-6">
                           <div className="w-10 h-10 rounded-xl bg-info flex items-center justify-center">
                              <span className="text-white font-bold">4</span>
                           </div>
                           <h2 className={`${PlayfairDisplay.className} text-2xl font-bold text-text-primary`}>
                              Insurance Information
                           </h2>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                           <input
                              name="policy_number"
                              value={form.insurance_info?.policy_number || ''}
                              onChange={(e) => setForm((prev) => ({
                                 ...prev,
                                 insurance_info: {
                                    ...(prev.insurance_info || {}),
                                    policy_number: e.target.value
                                 }
                              }))}
                              placeholder="Policy number"
                              className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-info focus:border-info transition-all"
                           />
                           <input
                              name="provider"
                              value={form.insurance_info?.provider || ''}
                              onChange={(e) => setForm((prev) => ({
                                 ...prev,
                                 insurance_info: {
                                    ...(prev.insurance_info || {}),
                                    provider: e.target.value
                                 }
                              }))}
                              placeholder="Insurance provider"
                              className="w-full border border-border-primary rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-info focus:border-info transition-all"
                           />
                        </div>
                     </div>

                     {/* Action Buttons */}
                     <div className="flex flex-col sm:flex-row justify-end gap-4 pt-6">
                        <button
                           type="button"
                           onClick={() => router.back()}
                           className="px-8 py-3 rounded-xl border-2 border-border-primary text-text-secondary font-semibold hover:bg-background-muted hover:border-primary-pastel transition-all duration-200 shadow-md hover:shadow-lg"
                        >
                           Cancel
                        </button>
                        <button
                           type="submit"
                           className="px-8 py-3 bg-secondary text-white font-semibold rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-secondary-pastel focus:ring-offset-2 cursor-pointer"
                        >
                           Create Patient Profile
                        </button>
                     </div>
                  </form>
               </div>

               {/* Live Preview Sidebar */}
               <aside className="xl:col-span-1">
                  <div className="sticky top-8 bg-background-secondary rounded-2xl p-6 border border-border-primary shadow-xl">
                     <div className="flex items-center gap-3 mb-6">
                        <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center">
                           <span className="text-white text-sm font-bold">👁</span>
                        </div>
                        <h3 className={`${PlayfairDisplay.className} text-xl font-bold text-text-primary`}>
                           Live Preview
                        </h3>
                     </div>

                     {/* Pet Card Preview */}
                     <div className="bg-primary-pastel/20 rounded-2xl p-5 border border-border-primary mb-6">
                        <div className="flex items-start gap-4">
                           <div className="w-16 h-16 rounded-xl overflow-hidden bg-background-primary border-2 border-border-primary flex-shrink-0">
                              {Array.isArray(form.photos) && form.photos[0] && form.photos[0].trim() ? (
                                 <img
                                    src={form.photos[0]}
                                    alt="pet preview"
                                    className="w-full h-full object-cover"
                                    onError={(e) => {
                                       const target = e.target as HTMLImageElement;
                                       target.style.display = 'none';
                                       target.parentElement!.innerHTML = '<div class="w-full h-full flex items-center justify-center bg-background-muted text-text-secondary text-2xl">🐾</div>';
                                    }}
                                 />
                              ) : (
                                 <div className="w-full h-full flex items-center justify-center bg-background-muted text-text-secondary text-2xl">
                                    🐾
                                 </div>
                              )}
                           </div>
                           <div className="flex-1 min-w-0">
                              <h3 className="text-lg font-bold text-text-primary truncate">
                                 {form.name || 'Pet Name'}
                              </h3>
                              <div className="text-sm text-text-secondary">
                                 {form.breed && form.pet_type ? `${form.breed} • ${form.pet_type}` : form.pet_type || 'Type not specified'}
                              </div>
                              {(form.age || form.weight) && (
                                 <div className="text-sm text-text-secondary mt-1">
                                    {form.age && `${form.age} yrs`}{form.age && form.weight && ' • '}{form.weight && `${form.weight} kg`}
                                 </div>
                              )}
                           </div>
                        </div>
                     </div>

                     {/* Emergency Contacts Preview */}
                     <div className="space-y-4">
                        <h4 className="font-semibold text-text-primary flex items-center gap-2">
                           <span className="text-danger">🚨</span>
                           Emergency Contacts
                        </h4>

                        <div className="space-y-3 text-sm">
                           <div className="bg-background-primary rounded-xl p-3 border border-border-primary">
                              <div className="text-xs text-text-secondary font-medium mb-1">OWNER</div>
                              <div className="text-text-primary">
                                 {form.emergency_contacts?.owner?.name || 'Not specified'}
                              </div>
                              <div className="text-text-secondary">
                                 {form.emergency_contacts?.owner?.phone || 'No phone number'}
                              </div>
                           </div>

                           <div className="bg-background-primary rounded-xl p-3 border border-border-primary">
                              <div className="text-xs text-text-secondary font-medium mb-1">VETERINARIAN</div>
                              <div className="text-text-primary">
                                 {form.emergency_contacts?.vet?.name || 'Not specified'}
                              </div>
                              <div className="text-text-secondary">
                                 {form.emergency_contacts?.vet?.phone || 'No phone number'}
                              </div>
                           </div>
                        </div>
                     </div>

                     {/* Insurance Preview */}
                     <div className="mt-6">
                        <h4 className="font-semibold text-text-primary flex items-center gap-2 mb-3">
                           <span className="text-info">🛡️</span>
                           Insurance
                        </h4>

                        <div className="bg-background-primary rounded-xl p-3 border border-border-primary">
                           {form.insurance_info?.provider || form.insurance_info?.policy_number ? (
                              <>
                                 <div className="font-medium text-text-primary">
                                    {form.insurance_info?.provider || 'Insurance Provider'}
                                 </div>
                                 <div className="text-sm text-text-secondary">
                                    {form.insurance_info?.policy_number || 'Policy number not provided'}
                                 </div>
                              </>
                           ) : (
                              <div className="text-text-secondary text-sm">No insurance information</div>
                           )}
                        </div>
                     </div>
                  </div>
               </aside>
            </div>
         </div>
      </DashLayout>
   );
};

export default Page;