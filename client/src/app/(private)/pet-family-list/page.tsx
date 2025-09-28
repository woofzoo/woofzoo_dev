'use client';

import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Users, Calendar, MoreVertical, UserPlus, Eye, Trash2 } from 'lucide-react';
import DashLayout from '@/components/layout/DashLayout';

// TypeScript interfaces
interface Family {
   id: string;
   name: string;
   description: string;
   owner_id: string;
   created_at: string;
   updated_at: string;
   members_count: number;
   pets_count: number;
}

interface FamilyFormData {
   name: string;
   description: string;
}

interface MemberFormData {
   name: string;
   email: string;
   phone: string;
   relationship: string;
}

interface FamilyModalProps {
   isOpen: boolean;
   onClose: () => void;
   family?: Family | null;
   onSubmit: (data: FamilyFormData | Family) => void;
   title: string;
   submitText: string;
}

interface AddMemberModalProps {
   isOpen: boolean;
   onClose: () => void;
   family: Family | null;
}

interface ActionDropdownProps {
   family: Family;
   onClose: () => void;
}

// Mock data based on your API response
const initialFamilies: Family[] = [
   {
      id: "123e4567-e89b-12d3-a456-426614174000",
      name: "Smith Family",
      description: "Our beloved pets family",
      owner_id: "123e4567-e89b-12d3-a456-426614174001",
      created_at: "2024-01-01T12:00:00Z",
      updated_at: "2024-01-01T12:00:00Z",
      members_count: 3,
      pets_count: 5
   },
   {
      id: "123e4567-e89b-12d3-a456-426614174002",
      name: "Johnson Family",
      description: "Long-time clients with multiple pets",
      owner_id: "123e4567-e89b-12d3-a456-426614174003",
      created_at: "2024-01-15T10:30:00Z",
      updated_at: "2024-02-10T14:20:00Z",
      members_count: 4,
      pets_count: 2
   },
   {
      id: "123e4567-e89b-12d3-a456-426614174004",
      name: "Williams Household",
      description: "Emergency contact family",
      owner_id: "123e4567-e89b-12d3-a456-426614174005",
      created_at: "2024-02-01T09:15:00Z",
      updated_at: "2024-02-01T09:15:00Z",
      members_count: 2,
      pets_count: 8
   }
];

const FamilyListingPage: React.FC = () => {
   const [families, setFamilies] = useState<Family[]>(initialFamilies);
   const [searchTerm, setSearchTerm] = useState<string>('');
   const [selectedFamily, setSelectedFamily] = useState<Family | null>(null);
   const [showAddModal, setShowAddModal] = useState<boolean>(false);
   const [showEditModal, setShowEditModal] = useState<boolean>(false);
   const [showAddMemberModal, setShowAddMemberModal] = useState<boolean>(false);
   const [activeDropdown, setActiveDropdown] = useState<string | null>(null);

   // Filter families based on search term
   const filteredFamilies = families.filter(family =>
      family.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      family.description.toLowerCase().includes(searchTerm.toLowerCase())
   );

   const formatDate = (dateString: string): string => {
      return new Date(dateString).toLocaleDateString('en-US', {
         year: 'numeric',
         month: 'short',
         day: 'numeric'
      });
   };

   const handleAddFamily = (data: Family | FamilyFormData): void => {
      // The modal can return either a Family (when editing) or FamilyFormData (when adding)
      if ('id' in data) {
         // If a full Family was passed, treat as an update
         const updatedFamily = data as Family;
         setFamilies([...families, { ...updatedFamily, created_at: updatedFamily.created_at || new Date().toISOString(), updated_at: new Date().toISOString() }]);
      } else {
         const newFamily = data as FamilyFormData;
         const family: Family = {
            id: Date.now().toString(),
            ...newFamily,
            owner_id: 'temp-owner-id',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            members_count: 1,
            pets_count: 0
         };
         setFamilies([...families, family]);
      }
      setShowAddModal(false);
   };

   const handleUpdateFamily = (data: Family | FamilyFormData): void => {
      // When called from the modal, we might receive a Family (with id) or a partial FamilyFormData
      if ('id' in data) {
         const updatedFamily = data as Family;
         setFamilies(families.map(family =>
            family.id === updatedFamily.id
               ? { ...family, ...updatedFamily, updated_at: new Date().toISOString() }
               : family
         ));
      } else {
         // No id provided; nothing to update. Could be treated as a no-op or add
         console.warn('handleUpdateFamily called without an id; ignoring.');
      }
      setShowEditModal(false);
      setSelectedFamily(null);
   };

   const handleDeleteFamily = (familyId: string): void => {
      if (window.confirm('Are you sure you want to delete this family?')) {
         setFamilies(families.filter(family => family.id !== familyId));
         setActiveDropdown(null);
      }
   };

   const ActionDropdown: React.FC<ActionDropdownProps> = ({ family, onClose }) => (
      <div className="absolute right-0 top-8 w-48 bg-background-primary border border-border-primary rounded-lg shadow-lg z-50">
         <div className="py-1">
            <button
               onClick={() => {
                  setSelectedFamily(family);
                  setShowEditModal(true);
                  onClose();
               }}
               className="w-full text-left px-4 py-2 text-sm text-text-primary hover:bg-background-secondary flex items-center gap-2"
               type="button"
            >
               <Edit2 size={16} />
               Edit Family
            </button>
            <button
               onClick={() => {
                  setSelectedFamily(family);
                  setShowAddMemberModal(true);
                  onClose();
               }}
               className="w-full text-left px-4 py-2 text-sm text-text-primary hover:bg-background-secondary flex items-center gap-2"
               type="button"
            >
               <UserPlus size={16} />
               Add Member
            </button>
            <button
               onClick={() => {
                  console.log('View details for:', family.name);
                  onClose();
               }}
               className="w-full text-left px-4 py-2 text-sm text-text-primary hover:bg-background-secondary flex items-center gap-2"
               type="button"
            >
               <Eye size={16} />
               View Details
            </button>
            <hr className="my-1 border-border-secondary" />
            <button
               onClick={() => {
                  handleDeleteFamily(family.id);
                  onClose();
               }}
               className="w-full text-left px-4 py-2 text-sm text-danger hover:bg-danger-pastel flex items-center gap-2"
               type="button"
            >
               <Trash2 size={16} />
               Delete Family
            </button>
         </div>
      </div>
   );

   const FamilyModal: React.FC<FamilyModalProps> = ({ isOpen, onClose, family, onSubmit, title, submitText }) => {
      const [formData, setFormData] = useState<FamilyFormData>({
         name: '',
         description: ''
      });

      useEffect(() => {
         if (family) {
            setFormData({
               name: family.name || '',
               description: family.description || ''
            });
         } else {
            setFormData({ name: '', description: '' });
         }
      }, [family, isOpen]);

      if (!isOpen) return null;

      const handleSubmit = (): void => {
         if (!formData.name.trim()) return;
         onSubmit(family ? { ...family, ...formData } : formData);
         if (!family) {
            setFormData({ name: '', description: '' });
         }
      };

      const handleClose = (): void => {
         setFormData({ name: '', description: '' });
         onClose();
      };

      return (
         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-background-primary border border-border-primary rounded-xl shadow-xl max-w-md w-full">
               <div className="p-6">
                  <h2 className="text-xl font-semibold text-text-primary mb-4">{title}</h2>
                  <div>
                     <div className="mb-4">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Family Name
                        </label>
                        <input
                           type="text"
                           value={formData.name}
                           onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus"
                           placeholder="Enter family name"
                        />
                     </div>
                     <div className="mb-6">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Description
                        </label>
                        <textarea
                           value={formData.description}
                           onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                           rows={3}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus resize-none"
                           placeholder="Enter family description"
                        />
                     </div>
                     <div className="flex gap-3 justify-end">
                        <button
                           type="button"
                           onClick={handleClose}
                           className="px-4 py-2 text-text-secondary hover:text-text-primary transition-colors"
                        >
                           Cancel
                        </button>
                        <button
                           onClick={handleSubmit}
                           disabled={!formData.name.trim()}
                           className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                           type="button"
                        >
                           {submitText}
                        </button>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      );
   };

   const AddMemberModal: React.FC<AddMemberModalProps> = ({ isOpen, onClose, family }) => {
      const [memberData, setMemberData] = useState<MemberFormData>({
         name: '',
         email: '',
         phone: '',
         relationship: ''
      });

      useEffect(() => {
         if (!isOpen) {
            setMemberData({ name: '', email: '', phone: '', relationship: '' });
         }
      }, [isOpen]);

      if (!isOpen) return null;

      const handleSubmit = (): void => {
         if (!memberData.name.trim() || !memberData.relationship) return;
         console.log('Adding member to family:', family?.name, memberData);
         // Here you would call your API to add the member
         setMemberData({ name: '', email: '', phone: '', relationship: '' });
         onClose();
      };

      const handleClose = (): void => {
         setMemberData({ name: '', email: '', phone: '', relationship: '' });
         onClose();
      };

      return (
         <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
            <div className="bg-background-primary border border-border-primary rounded-xl shadow-xl max-w-md w-full">
               <div className="p-6">
                  <h2 className="text-xl font-semibold text-text-primary mb-4">
                     Add Member to {family?.name || 'Family'}
                  </h2>
                  <div>
                     <div className="mb-4">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Full Name
                        </label>
                        <input
                           type="text"
                           value={memberData.name}
                           onChange={(e) => setMemberData({ ...memberData, name: e.target.value })}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus"
                           placeholder="Enter full name"
                        />
                     </div>
                     <div className="mb-4">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Email
                        </label>
                        <input
                           type="email"
                           value={memberData.email}
                           onChange={(e) => setMemberData({ ...memberData, email: e.target.value })}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus"
                           placeholder="Enter email address"
                        />
                     </div>
                     <div className="mb-4">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Phone Number
                        </label>
                        <input
                           type="tel"
                           value={memberData.phone}
                           onChange={(e) => setMemberData({ ...memberData, phone: e.target.value })}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus"
                           placeholder="Enter phone number"
                        />
                     </div>
                     <div className="mb-6">
                        <label className="block text-text-secondary text-sm font-medium mb-2">
                           Relationship
                        </label>
                        <select
                           value={memberData.relationship}
                           onChange={(e) => setMemberData({ ...memberData, relationship: e.target.value })}
                           className="w-full px-3 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary focus:outline-none focus:border-border-focus"
                        >
                           <option value="">Select relationship</option>
                           <option value="owner">Primary Owner</option>
                           <option value="family">Family Member</option>
                           <option value="caregiver">Caregiver</option>
                           <option value="emergency">Emergency Contact</option>
                        </select>
                     </div>
                     <div className="flex gap-3 justify-end">
                        <button
                           type="button"
                           onClick={handleClose}
                           className="px-4 py-2 text-text-secondary hover:text-text-primary transition-colors"
                        >
                           Cancel
                        </button>
                        <button
                           onClick={handleSubmit}
                           disabled={!memberData.name.trim() || !memberData.relationship}
                           className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                           type="button"
                        >
                           Add Member
                        </button>
                     </div>
                  </div>
               </div>
            </div>
         </div>
      );
   };

   return (
      <DashLayout className="p-6">
         {/* Header */}
         <div className="mb-8">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
               <div>
                  <h1 className="text-3xl font-bold text-text-primary">Families</h1>
                  <p className="text-text-secondary mt-1">
                     Manage pet families and their information
                  </p>
               </div>
               <button
                  onClick={() => setShowAddModal(true)}
                  className="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2 self-start sm:self-auto"
                  type="button"
               >
                  <Plus size={20} />
                  Add Family
               </button>
            </div>
         </div>

         {/* Search and Filters */}
         <div className="mb-6">
            <div className="flex flex-col sm:flex-row gap-4">
               <div className="flex-1">
                  <input
                     type="text"
                     placeholder="Search families..."
                     value={searchTerm}
                     onChange={(e) => setSearchTerm(e.target.value)}
                     className="w-full px-4 py-2 border border-border-primary rounded-lg bg-background-secondary text-text-primary placeholder-text-muted focus:outline-none focus:border-border-focus"
                  />
               </div>
            </div>
         </div>

         {/* Stats Cards */}
         <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-background-primary border border-border-primary rounded-lg p-6">
               <div className="flex items-center justify-between">
                  <div>
                     <p className="text-text-secondary text-sm">Total Families</p>
                     <p className="text-2xl font-bold text-text-primary">{families.length}</p>
                  </div>
                  <Users className="text-primary" size={24} />
               </div>
            </div>
            <div className="bg-background-primary border border-border-primary rounded-lg p-6">
               <div className="flex items-center justify-between">
                  <div>
                     <p className="text-text-secondary text-sm">Total Members</p>
                     <p className="text-2xl font-bold text-text-primary">
                        {families.reduce((sum, family) => sum + family.members_count, 0)}
                     </p>
                  </div>
                  <UserPlus className="text-secondary" size={24} />
               </div>
            </div>
            <div className="bg-background-primary border border-border-primary rounded-lg p-6">
               <div className="flex items-center justify-between">
                  <div>
                     <p className="text-text-secondary text-sm">Total Pets</p>
                     <p className="text-2xl font-bold text-text-primary">
                        {families.reduce((sum, family) => sum + family.pets_count, 0)}
                     </p>
                  </div>
                  <Users className="text-accent" size={24} />
               </div>
            </div>
            <div className="bg-background-primary border border-border-primary rounded-lg p-6">
               <div className="flex items-center justify-between">
                  <div>
                     <p className="text-text-secondary text-sm">Active This Month</p>
                     <p className="text-2xl font-bold text-text-primary">
                        {families.filter(f => new Date(f.updated_at) > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)).length}
                     </p>
                  </div>
                  <Calendar className="text-success" size={24} />
               </div>
            </div>
         </div>

         {/* Family Cards */}
         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredFamilies.map((family) => (
               <div
                  key={family.id}
                  className="bg-background-primary border border-border-primary rounded-lg hover:shadow-lg transition-shadow duration-200"
               >
                  <div className="p-6">
                     <div className="flex items-start justify-between mb-4">
                        <div>
                           <h3 className="text-lg font-semibold text-text-primary mb-1">
                              {family.name}
                           </h3>
                           <p className="text-text-secondary text-sm line-clamp-2">
                              {family.description}
                           </p>
                        </div>
                        <div className="relative">
                           <button
                              onClick={() => setActiveDropdown(activeDropdown === family.id ? null : family.id)}
                              className="p-2 hover:bg-background-secondary rounded-lg transition-colors"
                              type="button"
                           >
                              <MoreVertical size={16} className="text-text-secondary" />
                           </button>
                           {activeDropdown === family.id && (
                              <>
                                 <ActionDropdown
                                    family={family}
                                    onClose={() => setActiveDropdown(null)}
                                 />
                                 <div
                                    className="fixed inset-0 z-40"
                                    onClick={() => setActiveDropdown(null)}
                                    role="button"
                                    tabIndex={0}
                                    onKeyDown={(e) => {
                                       if (e.key === 'Escape') {
                                          setActiveDropdown(null);
                                       }
                                    }}
                                    aria-label="Close dropdown"
                                 />
                              </>
                           )}
                        </div>
                     </div>

                     <div className="grid grid-cols-2 gap-4 mb-4">
                        <div className="text-center">
                           <p className="text-2xl font-bold text-primary">{family.members_count}</p>
                           <p className="text-text-secondary text-xs">Members</p>
                        </div>
                        <div className="text-center">
                           <p className="text-2xl font-bold text-secondary">{family.pets_count}</p>
                           <p className="text-text-secondary text-xs">Pets</p>
                        </div>
                     </div>

                     <div className="flex items-center justify-between text-xs text-text-muted">
                        <span>Created: {formatDate(family.created_at)}</span>
                        <span>Updated: {formatDate(family.updated_at)}</span>
                     </div>
                  </div>

                  <div className="border-t border-border-secondary px-6 py-3">
                     <div className="flex gap-2">
                        <button
                           onClick={() => {
                              setSelectedFamily(family);
                              setShowEditModal(true);
                           }}
                           className="flex-1 bg-background-secondary hover:bg-primary/10 text-text-primary px-3 py-2 rounded text-sm transition-colors flex items-center justify-center gap-2"
                           type="button"
                        >
                           <Edit2 size={14} />
                           Edit
                        </button>
                        <button
                           onClick={() => {
                              setSelectedFamily(family);
                              setShowAddMemberModal(true);
                           }}
                           className="flex-1 bg-primary/10 hover:bg-primary/20 text-primary px-3 py-2 rounded text-sm transition-colors flex items-center justify-center gap-2"
                           type="button"
                        >
                           <UserPlus size={14} />
                           Add Member
                        </button>
                     </div>
                  </div>
               </div>
            ))}
         </div>

         {filteredFamilies.length === 0 && (
            <div className="text-center py-12">
               <Users size={48} className="text-text-muted mx-auto mb-4" />
               <h3 className="text-lg font-medium text-text-secondary mb-2">No families found</h3>
               <p className="text-text-muted mb-6">
                  {searchTerm ? 'Try adjusting your search terms.' : 'Get started by adding your first family.'}
               </p>
               {!searchTerm && (
                  <button
                     onClick={() => setShowAddModal(true)}
                     className="bg-primary hover:bg-primary/90 text-white px-6 py-3 rounded-lg transition-colors inline-flex items-center gap-2"
                     type="button"
                  >
                     <Plus size={20} />
                     Add First Family
                  </button>
               )}
            </div>
         )}

         {/* Modals */}
         <FamilyModal
            isOpen={showAddModal}
            onClose={() => setShowAddModal(false)}
            onSubmit={handleAddFamily}
            title="Add New Family"
            submitText="Add Family"
         />

         <FamilyModal
            isOpen={showEditModal}
            onClose={() => {
               setShowEditModal(false);
               setSelectedFamily(null);
            }}
            family={selectedFamily}
            onSubmit={handleUpdateFamily}
            title="Edit Family"
            submitText="Update Family"
         />

         <AddMemberModal
            isOpen={showAddMemberModal}
            onClose={() => {
               setShowAddMemberModal(false);
               setSelectedFamily(null);
            }}
            family={selectedFamily}
         />
      </DashLayout>
   );
};

export default FamilyListingPage;