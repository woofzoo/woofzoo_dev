"use client";

import DashLayout from '@/components/layout/DashLayout'
import { getAllPets } from '@/lib/api/pets';
import React, { useEffect, useState } from 'react';
import { PlayfairDisplay } from '@/components/ui/Fonts/Font';
import { PlusCircle } from 'lucide-react';
import { useRouter } from 'next/navigation';

const Page: React.FC = () => {
   const router = useRouter();
   const [pets, setPets] = useState<any[]>([]);
   const [total, setTotal] = useState<number>(0);

   useEffect(() => {
      const fetchPets = async () => {
         try {
            const data = await getAllPets({ skip: 0, limit: 50 });
            // API may return { pets: [...], total: N } or an array
            if (data?.pets) {
               setPets(data.pets || []);
               setTotal(Number(data.total ?? data.pets.length ?? 0));
            } else if (Array.isArray(data)) {
               setPets(data);
               setTotal(data.length);
            } else if (data) {
               // fallback if API returns a wrapper object with pets inside another key
               const maybePets = data.pets || data.items || [];
               setPets(maybePets);
               setTotal(Number(data.total ?? maybePets.length ?? 0));
            }
         } catch (error) {
            console.error('Failed to fetch pets:', error);
         }
      };

      fetchPets();
   }, []);

   return (
      <DashLayout>
         <div className="p-8 min-h-screen text-text-primary">
            <header className="flex items-center justify-between pb-6 mb-8 border-b border-border-primary">
               <div>
                  <h1 className={`${PlayfairDisplay.className} text-3xl font-bold tracking-tight`}>Patients (Pets)</h1>
                  <p className="text-sm text-text-secondary mt-1">All pets registered in the clinic — total {total}</p>
               </div>

               <div>
                  <button
                     onClick={() => router.push('/patients-add')}
                     className={`${PlayfairDisplay.className} inline-flex items-center gap-2 px-4 py-2 bg-secondary/90 text-white rounded-md shadow-md hover:brightness-95 transition-all duration-300`}
                  >
                     <PlusCircle size={16} />
                     Add New Pet
                  </button>
               </div>
            </header>

            {pets.length === 0 ? (
               <div className="flex flex-col items-center justify-center h-56 rounded-lg bg-background-secondary border border-dashed border-border-secondary">
                  <p className="text-center text-text-muted">No pets yet. Click "Add New Pet" to create one.</p>
               </div>
            ) : (
               <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {pets.map((pet) => (
                     <div
                        key={pet.id}
                        onClick={() => router.push(`/patients/${pet.id}`)}
                        className="bg-background-secondary rounded-lg shadow-md border border-border-primary p-4 hover:shadow-xl transition-shadow cursor-pointer"
                     >
                        <div className="flex items-center">
                           <div className="w-16 h-16 rounded-lg overflow-hidden bg-white border mr-4 flex-shrink-0">
                              <img
                                 src={(Array.isArray(pet.photos) && pet.photos[0]) || '/next.svg'}
                                 alt={pet.name}
                                 className="w-full h-full object-cover"
                              />
                           </div>

                           <div className="flex-1 min-w-0">
                              <h3 className="text-lg font-semibold truncate">{pet.name}</h3>
                              <div className="text-sm text-text-secondary truncate">{pet.breed} • {pet.pet_type}</div>
                              <div className="mt-2 text-sm text-text-secondary">Age: {pet.age} yrs • {pet.weight} kg</div>
                           </div>

                           <div className="ml-3">
                              {pet.is_active ? (
                                 <span className="px-2 py-1 rounded-full bg-success/10 text-success text-xs font-medium">Active</span>
                              ) : (
                                 <span className="px-2 py-1 rounded-full bg-danger/10 text-danger text-xs font-medium">Inactive</span>
                              )}
                           </div>
                        </div>

                        <div className="mt-4 pt-3 border-t border-border-primary text-sm text-text-primary">
                           <div className="flex items-center justify-between">
                              <div className="truncate">
                                 <div className="text-xs text-text-secondary">Owner ID</div>
                                 <div className="font-medium truncate">{pet.owner_id}</div>
                              </div>
                              <div className="text-xs text-text-secondary">{new Date(pet.created_at).toLocaleDateString()}</div>
                           </div>
                        </div>
                     </div>
                  ))}
               </div>
            )}
         </div>
      </DashLayout>
   );
};

export default Page;