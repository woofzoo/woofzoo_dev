'use client';

import DashLayout from '@/components/layout/DashLayout'
import Sidebar from '@/components/ui/Sidebar'
import { useAuth } from '@/context/AuthContext';
import React from 'react'

const DashPageById = () => {
   const { user, logout } = useAuth();

   return (
      <DashLayout>

      </DashLayout>
   )
}

export default DashPageById