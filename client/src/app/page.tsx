'use client'

import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

const page = () => {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (user) {
        router.replace(`/dashboard/${user.id}?loginSuccess=1`);
      } else {
        router.replace('/login');
      }
    }
  }, [user, isLoading, router]);
  return null;
}

export default page