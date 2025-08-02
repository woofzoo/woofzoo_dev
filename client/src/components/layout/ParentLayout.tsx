import { cn } from '@/utils/cn';
import React from 'react';

interface ParentLayoutProps {
  className?: string;
  children?: React.ReactNode;
}

const ParentLayout: React.FC<ParentLayoutProps> = ({ className, children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-grid-slate-200/50 dark:bg-grid-slate-700/25 bg-[size:20px_20px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />
      
      <main className={cn(
        'relative min-h-screen flex items-center justify-center px-4 py-8',
        'text-slate-900 dark:text-slate-100',
        className
      )}>
        <div className="w-full max-w-md">
          {/* Glass morphism container */}
          <div className="backdrop-blur-sm bg-white/80 dark:bg-slate-800/80 rounded-2xl shadow-xl border border-white/20 dark:border-slate-700/50 p-8">
            {children}
          </div>
        </div>
      </main>
      
      {/* Floating orbs for visual interest */}
      <div className="fixed top-10 left-10 w-72 h-72 bg-blue-400/20 rounded-full blur-3xl animate-pulse" />
      <div className="fixed bottom-10 right-10 w-96 h-96 bg-purple-400/20 rounded-full blur-3xl animate-pulse delay-1000" />
    </div>
  );
};

export default ParentLayout;