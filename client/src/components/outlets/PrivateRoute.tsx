'use client';

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

// A simple loading spinner component
const FullScreenLoader = () => (
   <div className="flex items-center justify-center h-screen">
      <div className="w-16 h-16 border-4 border-dashed rounded-full animate-spin border-primary"></div>
   </div>
);

export default function PrivateRoute({ children }: { children: React.ReactNode }) {
   const { user, isLoading } = useAuth();
   const router = useRouter();

   useEffect(() => {
      if (!isLoading && !user) {
         router.replace('/login');
      }
   }, [user, isLoading, router]);

   if (isLoading) {
      return <FullScreenLoader />;
   }
   if (user) {
      return <>{children}</>;
   }
   return null;
}