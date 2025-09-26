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

   // While checking for a user, you can show nothing or a loader.
   if (isLoading || user) {
      return null; // Or a loader, but null is fine as redirect will happen quickly.
   }

   // If no user is found, render the public page (e.g., the login form).
   return <>{children}</>;
}