"use client";

import DashLayout from "@/components/layout/DashLayout";
import { ChevronLeft } from "lucide-react";
import React, { useEffect, useState } from "react";
import { useRouter, useParams, usePathname } from "next/navigation";
import { getPetOwnerById } from "@/lib/api/owners";

type Owner = {
   id: string;
   name: string;
   email: string;
   phone_number: string;
   address: string;
   is_active?: boolean;
   created_at?: string;
   updated_at?: string;
};

const Page: React.FC = () => {
   const router = useRouter();
   const pathname = usePathname();
   const [owner, setOwner] = useState<Owner | null>(null);
   const [loading, setLoading] = useState<boolean>(true);
   const [error, setError] = useState<string | null>(null);

   const id = pathname.split("/")[2];
   const handleBack = () => {
      if (window.history.length > 1) {
         router.back();
      } else {
         router.push("/owners");
      }
   };

   useEffect(() => {
      const fetchOwner = async () => {
         setLoading(true);
         setError(null);
         try {
            const data = await getPetOwnerById(id);
            const owner = data?.owner || data || null;
            setOwner(owner);
         } catch (err) {
            setError("Failed to load owner details. Please try again.");
         } finally {
            setLoading(false);
         }
      };

      fetchOwner();
   }, []);

   const formatDate = (iso?: string) => {
      if (!iso) return "-";
      try {
         return new Date(iso).toLocaleString();
      } catch {
         return iso;
      }
   };

   return (
      <DashLayout>
         <div className="p-8 min-h-screen text-text-primary">
            <button
               onClick={handleBack}
               className="flex items-center gap-2 text-gray-700 hover:text-gray-900 mb-6 cursor-pointer"
            >
               <ChevronLeft size={24} />
               <span>Back to owners</span>
            </button>

            {loading ? (
               <div className="p-6 bg-background-secondary rounded-lg shadow-sm">
                  Loading owner...
               </div>
            ) : error ? (
               <div className="p-6 bg-red-50 text-red-700 rounded-lg border border-red-100">
                  {error}
               </div>
            ) : owner ? (
               <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Left: summary */}
                  <div className="bg-background-secondary rounded-lg shadow-md border border-border-primary p-6">
                     <div className="flex items-center space-x-4">
                        <div className="w-20 h-20 rounded-full bg-primary-pastel text-primary flex items-center justify-center font-bold text-2xl">
                           {owner.name
                              .split(" ")
                              .map((n) => n[0])
                              .slice(0, 2)
                              .join("")
                              .toUpperCase()}
                        </div>
                        <div>
                           <h2 className="text-2xl font-semibold">{owner.name}</h2>
                           <p className="text-sm text-text-secondary">{owner.email}</p>
                        </div>
                     </div>

                     <div className="mt-6 space-y-3 text-sm">
                        <div>
                           <div className="text-xs text-text-secondary">Phone</div>
                           <div className="text-text-primary">{owner.phone_number || '-'}</div>
                        </div>
                        <div>
                           <div className="text-xs text-text-secondary">Address</div>
                           <div className="text-text-primary">{owner.address || '-'}</div>
                        </div>
                        <div>
                           <div className="text-xs text-text-secondary">Status</div>
                           <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${owner.is_active ? 'bg-accent-pastel text-accent' : 'bg-red-100 text-red-700'}`}>
                              {owner.is_active ? 'Active' : 'Inactive'}
                           </div>
                        </div>
                     </div>
                  </div>

                  {/* Right: metadata and activity */}
                  <div className="lg:col-span-2 space-y-6">
                     <div className="bg-background-secondary rounded-lg shadow-md border border-border-primary p-6">
                        <h3 className="text-lg font-semibold mb-4">Metadata</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                           <div>
                              <div className="text-xs text-text-secondary">ID</div>
                              <div className="text-text-primary break-all">{owner.id}</div>
                           </div>
                           <div>
                              <div className="text-xs text-text-secondary">Created</div>
                              <div className="text-text-primary">{formatDate(owner.created_at)}</div>
                           </div>
                           <div>
                              <div className="text-xs text-text-secondary">Last Updated</div>
                              <div className="text-text-primary">{formatDate(owner.updated_at)}</div>
                           </div>
                           <div>
                              <div className="text-xs text-text-secondary">Email</div>
                              <div className="text-text-primary">{owner.email}</div>
                           </div>
                        </div>
                     </div>

                     {/* Placeholder for future pet list or actions */}
                     <div className="bg-background-secondary rounded-lg shadow-md border border-border-primary p-6">
                        <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                        <p className="text-sm text-text-secondary">No recent activity to show.</p>
                     </div>
                  </div>
               </div>
            ) : (
               <div className="p-6 bg-background-secondary rounded-lg shadow-sm">Owner not found.</div>
            )}
         </div>
      </DashLayout>
   );
};

export default Page;
