import { cn } from '@/utils/cn';
import React from 'react';

interface DashLayoutProps {
   className?: string;
   children?: React.ReactNode;
}

const DashLayout: React.FC<DashLayoutProps> = ({ className, children }) => {
   return (
      <div className="min-h-screen bg-gradient-to-br from-background-primary via-primary-pastel/20 to-secondary-pastel/30 relative overflow-hidden">
         {/* Animated Background Pattern */}
         <div className="absolute inset-0 opacity-40 z-0">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_2px_2px,theme(colors.primary/0.1)_2px,transparent_0)] bg-[size:32px_32px] animate-pulse" />
         </div>

         {/* Floating geometric shapes */}
         <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
            <div className="absolute top-10 left-10 w-72 h-72 bg-gradient-to-r from-primary/20 to-accent/20 rounded-full blur-3xl animate-pulse" />
            <div className="absolute top-1/3 right-20 w-96 h-96 bg-gradient-to-l from-primary-pastel/40 to-accent-pastel/30 rounded-full blur-2xl animate-pulse delay-700" />
            <div className="absolute bottom-20 left-1/4 w-80 h-80 bg-gradient-to-tr from-secondary/15 to-secondary-pastel/25 rounded-full blur-3xl animate-pulse delay-1000" />
            <div className="absolute bottom-10 right-10 w-64 h-64 bg-gradient-to-bl from-secondary-pastel/35 to-info/10 rounded-full blur-3xl animate-pulse delay-500" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-primary-pastel/10 via-accent-pastel/15 to-secondary-pastel/10 rounded-full blur-3xl animate-pulse delay-300" />
         </div>

         {/* Subtle grid overlay */}
         <div className="absolute inset-0 bg-[linear-gradient(rgba(255,105,51,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(33,160,160,0.03)_1px,transparent_1px)] bg-[size:60px_60px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,#000_60%,transparent_100%)] z-0" />

         {/* Animated particles */}
         <div className="absolute inset-0 overflow-hidden pointer-events-none z-0">
            <div className="absolute top-1/4 left-1/3 w-2 h-2 bg-primary/30 rounded-full animate-bounce delay-100" />
            <div className="absolute top-3/4 left-2/3 w-1 h-1 bg-secondary/40 rounded-full animate-bounce delay-300" />
            <div className="absolute top-1/2 right-1/4 w-1.5 h-1.5 bg-accent/35 rounded-full animate-bounce delay-500" />
            <div className="absolute bottom-1/3 left-1/5 w-1 h-1 bg-primary/25 rounded-full animate-bounce delay-700" />
         </div>

         {/* Main Content */}
         <main className={cn(
            'relative z-10 text-text-primary min-h-screen',
            className
         )}>
            {children}
         </main>
      </div>
   );
};

export default DashLayout;
