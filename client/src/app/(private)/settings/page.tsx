'use client';

import React, { useState } from 'react';
import { Building2, UserPlus, User, Bell, Lock, CreditCard, Globe, Shield } from 'lucide-react';
import DashLayout from '@/components/layout/DashLayout';
import ProfileSettings from '@/components/ui/ProfileSettings';
import AddClinicForm from '@/components/ui/AddClinicForm';
import AddDoctorForm from '@/components/ui/AddDoctorForm';
import DoctorClinicAssociation from '@/components/ui/DoctorClinicAssociation';
import ComingSoon from '@/components/ui/ComingSoon';
import SettingsSidebar from '@/components/ui/SettingSidebar';

export interface SidebarItem {
   id: string;
   label: string;
   icon: React.ElementType;
}

const SettingsPage: React.FC = () => {
   const [activeTab, setActiveTab] = useState<string>('profile');

   const sidebarItems: SidebarItem[] = [
      { id: 'profile', label: 'Profile Settings', icon: User },
      { id: 'clinic', label: 'Add Clinic', icon: Building2 },
      { id: 'doctor', label: 'Add Doctor', icon: UserPlus },
      { id: 'association', label: 'Doctor-Clinic Link', icon: Building2 },
      { id: 'notifications', label: 'Notifications', icon: Bell },
      { id: 'security', label: 'Security', icon: Lock },
      { id: 'billing', label: 'Billing', icon: CreditCard },
      { id: 'preferences', label: 'Preferences', icon: Globe },
      { id: 'privacy', label: 'Privacy', icon: Shield },
   ];

   const renderContent = () => {
      switch (activeTab) {
         case 'profile':
            return <ProfileSettings />;
         case 'clinic':
            return <AddClinicForm />;
         case 'doctor':
            return <AddDoctorForm />;
         case 'association':
            return <DoctorClinicAssociation />;
         default:
            const currentItem = sidebarItems.find(item => item.id === activeTab);
            return <ComingSoon item={currentItem} />;
      }
   };

   return (
      <DashLayout>
         <div className="flex">
            <SettingsSidebar
               items={sidebarItems}
               activeTab={activeTab}
               onTabChange={setActiveTab}
            />
            <div className="flex-1 p-8">
               <div className="max-w-4xl mx-auto">
                  {renderContent()}
               </div>
            </div>
         </div>
      </DashLayout>
   );
};

export default SettingsPage;