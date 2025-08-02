import { cn } from '@/utils/cn';
import React from 'react';

interface ParentLayoutProps {
  className?: string;
  children?: React.ReactNode;
}

const ParentLayout: React.FC<ParentLayoutProps> = ({ className, children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background-primary via-primary-pastel/20 to-secondary-pastel/30 relative overflow-hidden">
      {/* Animated Background Pattern */}
      <div className="absolute inset-0 opacity-40">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_2px_2px,theme(colors.primary/0.1)_2px,transparent_0)] bg-[size:32px_32px] animate-pulse" />
      </div>
      
      {/* Floating geometric shapes */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Orange accent orbs */}
        <div className="absolute top-10 left-10 w-72 h-72 bg-gradient-to-r from-primary/20 to-accent/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute top-1/3 right-20 w-96 h-96 bg-gradient-to-l from-primary-pastel/40 to-accent-pastel/30 rounded-full blur-2xl animate-pulse delay-700" />
        
        {/* Teal accent orbs */}
        <div className="absolute bottom-20 left-1/4 w-80 h-80 bg-gradient-to-tr from-secondary/15 to-secondary-pastel/25 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute bottom-10 right-10 w-64 h-64 bg-gradient-to-bl from-secondary-pastel/35 to-info/10 rounded-full blur-3xl animate-pulse delay-500" />
        
        {/* Subtle accent elements */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-to-r from-primary-pastel/10 via-accent-pastel/15 to-secondary-pastel/10 rounded-full blur-3xl animate-pulse delay-300" />
      </div>

      {/* Subtle grid overlay */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,105,51,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(33,160,160,0.03)_1px,transparent_1px)] bg-[size:60px_60px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,#000_60%,transparent_100%)]" />
      
      <main className={cn(
        'relative min-h-screen flex items-center justify-center px-4 py-8 z-10',
        'text-text-primary',
        className
      )}>
        <div className="w-full max-w-md">
          {/* Modern glassmorphism container */}
          <div className="relative group">
            {/* Subtle glow effect */}
            <div className="absolute -inset-1 bg-gradient-to-r from-primary/20 via-accent/20 to-secondary/20 rounded-3xl blur opacity-25 group-hover:opacity-40 transition duration-1000" />
            
            {/* Main container */}
            <div className="relative bg-white/90 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/30 p-8 hover:shadow-3xl transition-all duration-500">
              {/* Inner subtle gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-primary-pastel/5 via-transparent to-secondary-pastel/5 rounded-2xl pointer-events-none" />
              
              {/* Content */}
              <div className="relative z-10">
                {children}
              </div>
            </div>
          </div>
        </div>
      </main>
      
      {/* Animated particles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/3 w-2 h-2 bg-primary/30 rounded-full animate-bounce delay-100" />
        <div className="absolute top-3/4 left-2/3 w-1 h-1 bg-secondary/40 rounded-full animate-bounce delay-300" />
        <div className="absolute top-1/2 right-1/4 w-1.5 h-1.5 bg-accent/35 rounded-full animate-bounce delay-500" />
        <div className="absolute bottom-1/3 left-1/5 w-1 h-1 bg-primary/25 rounded-full animate-bounce delay-700" />
      </div>
    </div>
  );
};

export default ParentLayout;