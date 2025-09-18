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
         // remove the query param without adding a new history entry
         const pathname = window.location.pathname;
         router.replace(pathname);
      }
   // eslint-disable-next-line react-hooks/exhaustive-deps
   }, []);

   return (
      <DashLayout>

      </DashLayout>
   )
}

export default DashPageById