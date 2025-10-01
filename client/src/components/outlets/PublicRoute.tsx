'use client';

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function PublicRoute({ children }: { children: React.ReactNode }) {
   const { user, isLoading } = useAuth();
   const router = useRouter();

   useEffect(() => {
      if (!isLoading && user) {
         router.replace(`/dashboard/${user.id}?loginSuccess=1`);
      }
   }, [user, isLoading, router]);

   if (isLoading || user) {
      return null;
   }
   return <>{children}</>;
}