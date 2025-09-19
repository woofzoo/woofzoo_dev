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
    // If loading is finished and there's no user, redirect to login.
    if (!isLoading && !user) {
      router.replace('/login');
    }
  }, [user, isLoading, router]);

  // While checking for the user, show a loader.
  if (isLoading) {
    return <FullScreenLoader />;
  }

  // If a user is found, render the page.
  if (user) {
    return <>{children}</>;
  }

  // If no user and not loading (redirect is imminent), return null.
  return null;
}