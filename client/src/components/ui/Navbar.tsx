'use client'

import React, { useState, useRef, useEffect } from 'react';
import {
   Search,
   Bell,
   Plus,
   ChevronDown,
   Calendar,
   Heart,
   FileText,
   User,
   Settings,
   LogOut,
   UserCheck,
   X
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';

interface Notification {
   id: string;
   type: 'appointment' | 'stock' | 'payment';
   title: string;
   message: string;
   time: string;
   isRead: boolean;
}

const Navbar: React.FC = () => {
   const { logout } = useAuth();
   const [isSearchFocused, setIsSearchFocused] = useState(false);
   const [searchQuery, setSearchQuery] = useState('');
   const [showNotifications, setShowNotifications] = useState(false);
   const [showUserDropdown, setShowUserDropdown] = useState(false);
   const [showQuickActions, setShowQuickActions] = useState(false);
   const [notifications, setNotifications] = useState<Notification[]>([
      {
         id: '1',
         type: 'appointment',
         title: 'Upcoming Appointment',
         message: 'Bella\'s checkup in 30 minutes',
         time: '2 min ago',
         isRead: false
      },
      {
         id: '2',
         type: 'stock',
         title: 'Low Stock Alert',
         message: 'Vaccination supplies running low',
         time: '1 hour ago',
         isRead: false
      },
      {
         id: '3',
         type: 'payment',
         title: 'Payment Received',
         message: 'Invoice #1234 has been paid',
         time: '3 hours ago',
         isRead: true
      }
   ]);

   const searchRef = useRef<HTMLDivElement>(null);
   const notificationsRef = useRef<HTMLDivElement>(null);
   const userDropdownRef = useRef<HTMLDivElement>(null);
   const quickActionsRef = useRef<HTMLDivElement>(null);

   // Close dropdowns when clicking outside
   useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
         if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
            setIsSearchFocused(false);
         }
         if (notificationsRef.current && !notificationsRef.current.contains(event.target as Node)) {
            setShowNotifications(false);
         }
         if (userDropdownRef.current && !userDropdownRef.current.contains(event.target as Node)) {
            setShowUserDropdown(false);
         }
         if (quickActionsRef.current && !quickActionsRef.current.contains(event.target as Node)) {
            setShowQuickActions(false);
         }
      };

      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
   }, []);

   const unreadCount = notifications.filter(n => !n.isRead).length;

   const markAsRead = (id: string) => {
      setNotifications(prev =>
         prev.map(notification =>
            notification.id === id
               ? { ...notification, isRead: true }
               : notification
         )
      );
   };

   const clearAllNotifications = () => {
      setNotifications([]);
   };

   const getNotificationIcon = (type: Notification['type']) => {
      switch (type) {
         case 'appointment':
            return <Calendar className="w-4 h-4" />;
         case 'stock':
            return <FileText className="w-4 h-4" />;
         case 'payment':
            return <Heart className="w-4 h-4" />;
         default:
            return <Bell className="w-4 h-4" />;
      }
   };

   const handleLogout = () => {
      logout();
   }

   const quickActionItems = [
      {
         id: 'appointment',
         label: 'Add Appointment',
         icon: Calendar,
         description: 'Schedule new visit'
      },
      {
         id: 'pet',
         label: 'Add Pet',
         icon: Heart,
         description: 'Register new patient'
      },
      {
         id: 'invoice',
         label: 'Add Invoice',
         icon: FileText,
         description: 'Create billing record'
      }
   ];

   return (
      <nav className="h-16 bg-background-secondary/80 backdrop-blur-md border-b border-border-primary flex items-center justify-between px-6 relative z-20">
         {/* Left Section - Search */}
         <div className="flex items-center flex-1 max-w-lg">
            <div
               ref={searchRef}
               className={`relative w-full transition-all duration-200 ${isSearchFocused ? 'transform scale-105' : ''
                  }`}
            >
               <div className="relative">
                  <Search
                     className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4"
                     style={{ color: 'var(--text-muted)' }}
                  />
                  <input
                     type="text"
                     placeholder="Search pets, owners, appointments..."
                     value={searchQuery}
                     onChange={(e) => setSearchQuery(e.target.value)}
                     onFocus={() => setIsSearchFocused(true)}
                     className={`w-full pl-10 pr-4 py-2.5 rounded-xl transition-all duration-200 border-2 focus:outline-none ${isSearchFocused
                        ? 'border-primary shadow-lg'
                        : 'border-transparent bg-background-primary/60'
                        }`}
                     style={{
                        backgroundColor: isSearchFocused
                           ? 'var(--background-primary)'
                           : 'var(--background-primary-60)',
                        color: 'var(--text-primary)'
                     }}
                  />
               </div>

               {/* Search Results Dropdown */}
               {isSearchFocused && searchQuery && (
                  <div
                     className="absolute top-full mt-2 w-full rounded-xl shadow-xl border border-border-primary overflow-hidden z-50"
                     style={{ backgroundColor: 'var(--background-secondary)' }}
                  >
                     <div className="p-3">
                        <div
                           className="text-xs font-medium mb-2"
                           style={{ color: 'var(--text-muted)' }}
                        >
                           Quick Results
                        </div>
                        <div className="space-y-2">
                           <div
                              className="p-2 rounded-lg hover:bg-primary-pastel/20 cursor-pointer transition-colors"
                           >
                              <div
                                 className="text-sm font-medium"
                                 style={{ color: 'var(--text-primary)' }}
                              >
                                 Bella (Golden Retriever)
                              </div>
                              <div
                                 className="text-xs"
                                 style={{ color: 'var(--text-secondary)' }}
                              >
                                 Owner: John Smith
                              </div>
                           </div>
                        </div>
                     </div>
                  </div>
               )}
            </div>
         </div>

         {/* Right Section - Actions */}
         <div className="flex items-center space-x-4">
            {/* Quick Actions */}
            <div className="relative" ref={quickActionsRef}>
               <button
                  onClick={() => setShowQuickActions(!showQuickActions)}
                  className={`p-2.5 rounded-xl transition-all duration-200 border-2 ${showQuickActions
                     ? 'border-primary bg-primary-pastel shadow-md'
                     : 'border-transparent bg-background-primary/60 hover:bg-primary-pastel/30'
                     }`}
                  title="Quick Actions"
               >
                  <Plus
                     className={`w-5 h-5 transition-transform duration-200 ${showQuickActions ? 'rotate-45' : ''
                        }`}
                     style={{ color: showQuickActions ? 'var(--primary-color)' : 'var(--text-secondary)' }}
                  />
               </button>

               {/* Quick Actions Dropdown */}
               {showQuickActions && (
                  <div
                     className="absolute right-0 top-full mt-2 w-64 rounded-xl shadow-xl border border-border-primary overflow-hidden z-50"
                     style={{ backgroundColor: 'var(--background-secondary)' }}
                  >
                     <div className="p-3">
                        <div
                           className="text-xs font-medium mb-3"
                           style={{ color: 'var(--text-muted)' }}
                        >
                           Quick Actions
                        </div>
                        <div className="space-y-1">
                           {quickActionItems.map((item) => (
                              <button
                                 key={item.id}
                                 className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-pastel/20 transition-colors text-left"
                                 onClick={() => setShowQuickActions(false)}
                              >
                                 <item.icon
                                    className="w-4 h-4"
                                    style={{ color: 'var(--primary-color)' }}
                                 />
                                 <div>
                                    <div
                                       className="text-sm font-medium"
                                       style={{ color: 'var(--text-primary)' }}
                                    >
                                       {item.label}
                                    </div>
                                    <div
                                       className="text-xs"
                                       style={{ color: 'var(--text-secondary)' }}
                                    >
                                       {item.description}
                                    </div>
                                 </div>
                              </button>
                           ))}
                        </div>
                     </div>
                  </div>
               )}
            </div>

            {/* Notifications */}
            <div className="relative" ref={notificationsRef}>
               <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className={`relative p-2.5 rounded-xl transition-all duration-200 border-2 ${showNotifications
                     ? 'border-accent bg-accent-pastel shadow-md'
                     : 'border-transparent bg-background-primary/60 hover:bg-accent-pastel/30'
                     }`}
                  title="Notifications"
               >
                  <Bell
                     className="w-5 h-5"
                     style={{ color: showNotifications ? 'var(--accent-color)' : 'var(--text-secondary)' }}
                  />
                  {unreadCount > 0 && (
                     <span
                        className="absolute -top-1 -right-1 w-5 h-5 rounded-full text-xs font-bold flex items-center justify-center text-white"
                        style={{ backgroundColor: 'var(--error-color)' }}
                     >
                        {unreadCount}
                     </span>
                  )}
               </button>

               {/* Notifications Dropdown */}
               {showNotifications && (
                  <div
                     className="absolute right-0 top-full mt-2 w-80 rounded-xl shadow-xl border border-border-primary overflow-hidden z-50"
                     style={{ backgroundColor: 'var(--background-secondary)' }}
                  >
                     <div className="p-4">
                        <div className="flex items-center justify-between mb-3">
                           <div
                              className="text-sm font-medium"
                              style={{ color: 'var(--text-primary)' }}
                           >
                              Notifications
                           </div>
                           {notifications.length > 0 && (
                              <button
                                 onClick={clearAllNotifications}
                                 className="text-xs hover:underline"
                                 style={{ color: 'var(--text-muted)' }}
                              >
                                 Clear all
                              </button>
                           )}
                        </div>

                        {notifications.length === 0 ? (
                           <div
                              className="text-center py-6 text-sm"
                              style={{ color: 'var(--text-muted)' }}
                           >
                              No notifications
                           </div>
                        ) : (
                           <div className="space-y-2 max-h-80 overflow-y-auto">
                              {notifications.map((notification) => (
                                 <div
                                    key={notification.id}
                                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${!notification.isRead
                                       ? 'bg-accent-pastel/30 border-accent/20'
                                       : 'bg-background-primary/30 border-transparent'
                                       }`}
                                    onClick={() => markAsRead(notification.id)}
                                 >
                                    <div className="flex items-start space-x-3">
                                       <div
                                          className="p-1.5 rounded-full"
                                          style={{ backgroundColor: 'var(--accent-color-pastel)' }}
                                       >
                                          {getNotificationIcon(notification.type)}
                                       </div>
                                       <div className="flex-1">
                                          <div
                                             className="text-sm font-medium"
                                             style={{ color: 'var(--text-primary)' }}
                                          >
                                             {notification.title}
                                          </div>
                                          <div
                                             className="text-xs mt-1"
                                             style={{ color: 'var(--text-secondary)' }}
                                          >
                                             {notification.message}
                                          </div>
                                          <div
                                             className="text-xs mt-2"
                                             style={{ color: 'var(--text-muted)' }}
                                          >
                                             {notification.time}
                                          </div>
                                       </div>
                                       {!notification.isRead && (
                                          <div
                                             className="w-2 h-2 rounded-full"
                                             style={{ backgroundColor: 'var(--accent-color)' }}
                                          />
                                       )}
                                    </div>
                                 </div>
                              ))}
                           </div>
                        )}
                     </div>
                  </div>
               )}
            </div>

            {/* User Dropdown */}
            <div className="relative" ref={userDropdownRef}>
               <button
                  onClick={() => setShowUserDropdown(!showUserDropdown)}
                  className={`flex items-center space-x-3 p-2 rounded-xl transition-all duration-200 border-2 ${showUserDropdown
                     ? 'border-secondary bg-secondary-pastel shadow-md'
                     : 'border-transparent bg-background-primary/60 hover:bg-secondary-pastel/30'
                     }`}
               >
                  <div
                     className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
                     style={{
                        backgroundColor: 'var(--secondary-color)',
                        color: 'var(--text-inverse)'
                     }}
                  >
                     DC
                  </div>
                  <ChevronDown
                     className={`w-4 h-4 transition-transform duration-200 ${showUserDropdown ? 'rotate-180' : ''
                        }`}
                     style={{ color: 'var(--text-secondary)' }}
                  />
               </button>

               {/* User Dropdown Menu */}
               {showUserDropdown && (
                  <div
                     className="absolute right-0 top-full mt-2 w-64 rounded-xl shadow-xl border border-border-primary overflow-hidden z-50"
                     style={{ backgroundColor: 'var(--background-secondary)' }}
                  >
                     {/* User Info */}
                     <div className="p-4 border-b border-border-primary">
                        <div className="flex items-center space-x-3">
                           <div
                              className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium"
                              style={{
                                 backgroundColor: 'var(--secondary-color)',
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

                     {/* Menu Items */}
                     <div className="p-2">
                        <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-pastel/20 transition-colors text-left">
                           <User className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                           <span
                              className="text-sm"
                              style={{ color: 'var(--text-primary)' }}
                           >
                              View Profile
                           </span>
                        </button>
                        <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-pastel/20 transition-colors text-left">
                           <UserCheck className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                           <span
                              className="text-sm"
                              style={{ color: 'var(--text-primary)' }}
                           >
                              Switch Role
                           </span>
                        </button>
                        <button className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-primary-pastel/20 transition-colors text-left">
                           <Settings className="w-4 h-4" style={{ color: 'var(--text-secondary)' }} />
                           <span
                              className="text-sm"
                              style={{ color: 'var(--text-primary)' }}
                           >
                              Settings
                           </span>
                        </button>

                        <div className="border-t border-border-primary my-2" />

                        <button
                           className="w-full flex items-center space-x-3 p-3 rounded-lg hover:bg-error-pastel/20 transition-colors text-left"
                           onClick={() => handleLogout()}
                        >
                           <LogOut className="w-4 h-4" style={{ color: 'var(--error-color)' }} />
                           <span
                              className="text-sm"
                              style={{ color: 'var(--error-color)' }}
                           >
                              Logout
                           </span>
                        </button>

                     </div>
                  </div>
               )}
            </div>
         </div>
      </nav>
   );
};

export default Navbar;