"use client";

import React from 'react';

export interface SidebarItem {
   id: string;
   label: string;
   icon: React.ElementType;
}

interface SettingsSidebarProps {
   items: SidebarItem[];
   activeTab: string;
   onTabChange: (tab: string) => void;
}

const SettingsSidebar: React.FC<SettingsSidebarProps> = ({ items, activeTab, onTabChange }) => {
   return (
      <div className="w-64 min-h-screen bg-background-secondary border-r border-border-primary">
         <div className="p-6">
            <h1 className="text-xl font-semibold text-text-primary mb-1">Settings</h1>
            <p className="text-sm text-text-secondary">Manage your account</p>
         </div>

         <nav className="px-3 pb-6">
            {items.map((item) => {
               const Icon = item.icon;
               return (
                  <button
                     key={item.id}
                     onClick={() => onTabChange(item.id)}
                     className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-all ${activeTab === item.id
                           ? 'bg-primary-pastel text-primary font-medium'
                           : 'text-text-secondary hover:bg-background-muted hover:text-text-primary'
                        }`}
                  >
                     <Icon size={20} />
                     <span className="text-sm">{item.label}</span>
                  </button>
               );
            })}
         </nav>
      </div>
   );
};

export default SettingsSidebar;