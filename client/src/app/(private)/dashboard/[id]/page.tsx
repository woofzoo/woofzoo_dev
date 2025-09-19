'use client';

import DashLayout from '@/components/layout/DashLayout'
import Sidebar from '@/components/ui/Sidebar'
import { useAuth } from '@/context/AuthContext';
import React, { useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation';
import { useToast } from '@/components/toast/ToastProvider';

const DashPageById = () => {
   const { user, logout } = useAuth();
   const searchParams = useSearchParams();
   const router = useRouter();
   const { showSuccess } = useToast();

   useEffect(() => {
      const loginSuccess = searchParams.get('loginSuccess');
      console.log(loginSuccess);
      if (loginSuccess === "1") {
         showSuccess('Login Successful!', `Welcome back, ${user?.first_name || 'User'} 🎉`, 5000);
         const pathname = window.location.pathname;
         router.replace(pathname);
      }
   }, []);

   return (
      <DashLayout>

      </DashLayout>
   )
}

export default DashPageById