import { cn } from '@/utils/cn';
import React from 'react';

interface ParentLayoutProps {
   className?: string;
   children?: React.ReactNode;
}

const ParentLayout: React.FC<ParentLayoutProps> = ({ className, children }) => {
   return (
      <main className={cn('text-lg', className)}>{children}</main>
   )
}

export default ParentLayout;