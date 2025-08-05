'use client'

import { menuItems } from '@/utils/content';
import {
   ChevronDown,
   ChevronRight
} from 'lucide-react';
import React, { useState } from 'react';

interface ExpandedSections {
   [key: string]: boolean;
}

const Sidebar: React.FC = () => {
   const [activeItem, setActiveItem] = useState<string>('dashboard');
   const [expandedSections, setExpandedSections] = useState<ExpandedSections>({
      patients: false,
      medical: false
   });

   const toggleSection = (section: string): void => {
      setExpandedSections(prev => ({
         ...prev,
         [section]: !prev[section]
      }));
   };


   const handleItemClick = (itemId: string): void => {
      setActiveItem(itemId);
   };

   return (
      <div
         className="h-screen w-80 bg-background-secondary border-r border-border-primary flex flex-col"
      >
         {/* Header */}
         <div className="p-3 border-b border-border-primary mt-3">
            <div className="w-[13rem] rounded-2xl mb-4 flex items-center justify-center">
               <img
                  src="/tm-logo.svg"
                  alt="TM Logo"
                  className=" object-contain"
               />
            </div>
         </div>

         {/* Navigation */}
         <nav className="flex-1 overflow-y-auto p-4">
            <div className="space-y-1">
               {menuItems.map((item) => (
                  <div key={item.id}>
                     <button
                        onClick={() => {
                           if (item.expandable) {
                              toggleSection(item.id);
                           } else {
                              handleItemClick(item.id);
                           }
                        }}
                        className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-200 group ${activeItem === item.id
                           ? 'shadow-md bg-primary-pastel border-l-[3px] border-solid border-primary'
                           : 'hover:shadow-sm bg-transparent border-l-[3px] border-solid border-transparent'
                           }`}
                     >
                        <div className="flex items-center space-x-3">
                           <item.icon
                              className={`w-5 h-5 transition-colors ${activeItem === item.id
                                 ? 'text-primary'
                                 : 'text-text-secondary group-hover:text-primary'
                                 }`}
                              style={{
                                 color: activeItem === item.id
                                    ? 'var(--primary-color)'
                                    : undefined
                              }}
                           />
                           <div className="text-left">
                              <div
                                 className={`font-medium ${activeItem === item.id
                                    ? 'text-primary'
                                    : 'text-text-primary'
                                    }`}
                                 style={{
                                    color: activeItem === item.id
                                       ? 'var(--primary-color)'
                                       : 'var(--text-primary)'
                                 }}
                              >
                                 {item.label}
                              </div>
                              <div
                                 className="text-xs"
                                 style={{ color: 'var(--text-muted)' }}
                              >
                                 {item.description}
                              </div>
                           </div>
                        </div>
                        {item.expandable && (
                           <div>
                              {expandedSections[item.id] ? (
                                 <ChevronDown className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                              ) : (
                                 <ChevronRight className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                              )}
                           </div>
                        )}
                     </button>

                     {/* Sub-items */}
                     {item.expandable && expandedSections[item.id] && (
                        <div className="ml-4 mt-1 space-y-1">
                           {item.subItems?.map((subItem) => (
                              <button
                                 key={subItem.id}
                                 onClick={() => handleItemClick(subItem.id)}
                                 className={`w-full flex items-center space-x-3 px-4 py-2 rounded-md transition-all duration-200 ${activeItem === subItem.id
                                    ? 'shadow-sm'
                                    : 'hover:shadow-sm'
                                    }`}
                                 style={{
                                    backgroundColor: activeItem === subItem.id
                                       ? 'var(--secondary-color-pastel)'
                                       : 'transparent',
                                    borderLeft: activeItem === subItem.id
                                       ? '2px solid var(--secondary-color)'
                                       : '2px solid transparent'
                                 }}
                              >
                                 <subItem.icon
                                    className="w-4 h-4"
                                    style={{
                                       color: activeItem === subItem.id
                                          ? 'var(--secondary-color)'
                                          : 'var(--text-muted)'
                                    }}
                                 />
                                 <span
                                    className="text-sm font-medium"
                                    style={{
                                       color: activeItem === subItem.id
                                          ? 'var(--secondary-color)'
                                          : 'var(--text-secondary)'
                                    }}
                                 >
                                    {subItem.label}
                                 </span>
                              </button>
                           ))}
                        </div>
                     )}

                  </div>
               ))}
            </div>
         </nav>

         {/* Footer */}
         <div className="p-4 border-t border-border-primary">
            <div
               className="p-3 rounded-lg"
               style={{ backgroundColor: 'var(--accent-color-pastel)' }}
            >
               <div className="flex items-center space-x-3">
                  <div
                     className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                     style={{
                        backgroundColor: 'var(--accent-color)',
                        color: 'var(--text-inverse)'
                     }}
                  >
                     DC
                  </div>
                  <div>
                     <div
                        className="text-sm font-medium"
                        style={{ color: 'var(--text-primary)' }}
                     >
                        Dr. Sarah Chen
                     </div>
                     <div
                        className="text-xs"
                        style={{ color: 'var(--text-secondary)' }}
                     >
                        Lead Veterinarian
                     </div>
                  </div>
               </div>
            </div>
         </div>
      </div>
   );
};

export default Sidebar;