'use client'

import { useAuth } from '@/context/AuthContext';
import { menuItems } from '@/utils/content';
import {
   ChevronDown,
   ChevronRight
} from 'lucide-react';
import { usePathname, useRouter } from 'next/navigation';
import React, { useState } from 'react';

interface ExpandedSections {
   [key: string]: boolean;
}

interface SidebarProps {
   isCollapsed?: boolean;
   onToggle?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed = false, onToggle }) => {
   const router = useRouter();
   const pathname = usePathname();
   const { user } = useAuth();
   const [activeItem, setActiveItem] = useState<string>(pathname.split("/")[1]);
   const [expandedSections, setExpandedSections] = useState<ExpandedSections>({
      patients: false,
      medical: false
   });

   const toggleSection = (section: string): void => {
      if (isCollapsed) return; // Don't allow section toggle when collapsed
      setExpandedSections(prev => ({
         ...prev,
         [section]: !prev[section]
      }));
   };

   const handleItemClick = (itemId: string): void => {
      if (user) {
         if (itemId == 'dashboard') {
            router.replace(`/${itemId}/${user.id}`);
         } else {
            router.replace(`/${itemId}`);
         }
      }
   };

   return (
      <div
         className={`h-screen bg-background-secondary/95 backdrop-blur-sm border-r border-border-primary flex flex-col transition-all duration-300 ease-in-out ${isCollapsed ? 'w-16' : 'w-80'
            }`}
      >
         {/* Header */}
         <div className="p-3 border-b border-border-primary mt-4">
            <div className={`rounded-2xl mb-4 flex items-center justify-center transition-all duration-300 ${isCollapsed ? 'w-10 h-10' : 'w-[13rem]'
               }`}>
               <img
                  src="/tm-logo.svg"
                  alt="TM Logo"
                  className="object-contain"
                  style={{
                     width: isCollapsed ? '40px' : 'auto',
                     height: isCollapsed ? '40px' : 'auto'
                  }}
               />
            </div>
         </div>

         {/* Navigation */}
         <nav className="flex-1 overflow-y-auto p-4 sidebar-scroll">
            <div className="space-y-1">
               {menuItems.map((item) => (
                  <div key={item.id}>
                     {/* Main Item */}
                     <button
                        onClick={() => {
                           if (item.expandable && !isCollapsed) {
                              toggleSection(item.id);
                           } else {
                              handleItemClick(item.id);
                           }
                        }}
                        className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-all duration-200 group relative ${activeItem === item.id
                           ? 'shadow-md bg-primary-pastel border-l-[3px] border-solid border-primary'
                           : 'hover:shadow-sm bg-transparent border-l-[3px] border-solid border-transparent hover:bg-background-primary/30'
                           }`}
                        title={isCollapsed ? item.label : undefined}
                     >
                        <div className={`flex items-center transition-all duration-300 ${isCollapsed ? 'justify-center w-full' : 'space-x-3'
                           }`}>
                           <item.icon
                              className={`transition-colors ${isCollapsed ? 'w-6 h-6' : 'w-5 h-5'
                                 } ${activeItem === item.id
                                    ? 'text-primary'
                                    : 'text-text-secondary group-hover:text-primary'
                                 }`}
                              style={{
                                 color: activeItem === item.id
                                    ? 'var(--primary-color)'
                                    : undefined
                              }}
                           />
                           {!isCollapsed && (
                              <div className="text-left">
                                 <div
                                    className={`font-medium cursor-pointer ${activeItem === item.id
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
                           )}
                        </div>
                        {item.expandable && !isCollapsed && (
                           <div>
                              {expandedSections[item.id] ? (
                                 <ChevronDown className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                              ) : (
                                 <ChevronRight className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                              )}
                           </div>
                        )}

                        {/* Tooltip for collapsed state */}
                        {isCollapsed && (
                           <div className="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50 pointer-events-none">
                              <div className="font-medium">{item.label}</div>
                              <div className="text-xs text-gray-300 mt-1">{item.description}</div>
                              {/* Tooltip arrow */}
                              <div className="absolute left-0 top-1/2 transform -translate-x-1 -translate-y-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
                           </div>
                        )}
                     </button>

                     {/* Sub-items - Show when expanded and not collapsed */}
                     {item.expandable && expandedSections[item.id] && !isCollapsed && (
                        <div className="ml-4 mt-1 space-y-1">
                           {item.subItems?.map((subItem) => (
                              <button
                                 key={subItem.id}
                                 onClick={() => handleItemClick(subItem.id)}
                                 className={`w-full flex items-center space-x-3 px-4 py-2 rounded-md transition-all duration-200 group cursor-pointer ${activeItem === subItem.id
                                    ? 'shadow-sm'
                                    : 'hover:shadow-sm hover:bg-background-primary/30'
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
                                    className="w-4 h-4 flex-shrink-0"
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

                     {/* Sub-items icons for collapsed state */}
                     {item.expandable && isCollapsed && item.subItems && (
                        <div className="mt-1 space-y-1">
                           {/* Show parent/main icon as a small header above sub-items so users can identify the group when collapsed */}
                           <div className="flex items-center justify-center p-1">
                              <item.icon className="w-4 h-4 text-text-secondary" />
                           </div>
                           <div className="space-y-1">
                              {item.subItems.map((subItem) => (
                                 <button
                                    key={`collapsed-${subItem.id}`}
                                    onClick={() => handleItemClick(subItem.id)}
                                    className={`w-full flex items-center justify-center p-2 rounded-lg transition-all duration-200 group relative ${activeItem === subItem.id
                                       ? 'bg-secondary-pastel border-l-[3px] border-solid border-secondary'
                                       : 'hover:bg-background-primary/30 border-l-[3px] border-solid border-transparent'
                                       }`}
                                    title={subItem.label}
                                 >
                                    <subItem.icon
                                       className="w-4 h-4"
                                       style={{
                                          color: activeItem === subItem.id
                                             ? 'var(--secondary-color)'
                                             : 'var(--text-muted)'
                                       }}
                                    />

                                    {/* Sub-item tooltip for collapsed state */}
                                    <div className="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50 pointer-events-none">
                                       <div className="font-medium">{subItem.label}</div>
                                       {/* Tooltip arrow */}
                                       <div className="absolute left-0 top-1/2 transform -translate-x-1 -translate-y-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
                                    </div>
                                 </button>
                              ))}
                           </div>
                        </div>
                     )}
                  </div>
               ))}
            </div>
         </nav>

         {/* Footer - only show when not collapsed */}
         {!isCollapsed && (
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
         )}

         {/* Collapsed footer - show avatar only */}
         {isCollapsed && (
            <div className="p-4 border-t border-border-primary flex justify-center">
               <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium group cursor-pointer relative"
                  style={{
                     backgroundColor: 'var(--accent-color)',
                     color: 'var(--text-inverse)'
                  }}
                  title="Dr. Sarah Chen"
               >
                  DC
                  {/* Tooltip */}
                  <div className="absolute left-full ml-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 whitespace-nowrap z-50 pointer-events-none">
                     <div className="font-medium">Dr. Sarah Chen</div>
                     <div className="text-xs text-gray-300 mt-1">Lead Veterinarian</div>
                     {/* Tooltip arrow */}
                     <div className="absolute left-0 top-1/2 transform -translate-x-1 -translate-y-1/2 w-2 h-2 bg-gray-900 rotate-45"></div>
                  </div>
               </div>
            </div>
         )}
      </div>
   );
};

export default Sidebar;