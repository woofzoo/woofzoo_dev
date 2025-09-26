import { cn } from '@/utils/cn';
import React from 'react';

interface ParentLayoutProps {
  className?: string;
  children?: React.ReactNode;
}

const ParentLayout: React.FC<ParentLayoutProps> = ({ className, children }) => {
  return (
    <div className="min-h-screen bg-white relative overflow-hidden">
      {/* Subtle background elements for the right side only */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Geometric shapes positioned on the right half */}
        <div className="absolute top-20 right-20 w-64 h-64 bg-gradient-to-r from-orange-100/40 to-orange-200/40 rounded-full blur-3xl" />
        <div className="absolute bottom-32 right-32 w-80 h-80 bg-gradient-to-l from-teal-100/30 to-teal-200/30 rounded-full blur-2xl" />
        <div className="absolute top-1/2 right-10 w-48 h-48 bg-gradient-to-tr from-orange-50/50 to-orange-100/50 rounded-full blur-2xl" />
      </div>

      {/* Main content */}
      <main className={cn(
        'relative min-h-screen z-10',
        className
      )}>
        {children}
      </main>

      {/* Subtle animated elements for the form side */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Small floating elements on right side only */}
        <div className="absolute top-1/4 right-1/3 w-2 h-2 bg-orange-300/40 rounded-full animate-bounce delay-100" />
        <div className="absolute top-3/4 right-1/4 w-1 h-1 bg-teal-400/40 rounded-full animate-bounce delay-300" />
        <div className="absolute top-1/2 right-1/2 w-1.5 h-1.5 bg-orange-400/35 rounded-full animate-bounce delay-500" />
        <div className="absolute bottom-1/3 right-2/5 w-1 h-1 bg-orange-300/40 rounded-full animate-bounce delay-700" />
      </div>
    </div>
  );
};

export default ParentLayout;