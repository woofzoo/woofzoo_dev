import React from 'react';

interface ComingSoonProps {
  item?: SidebarItem;
}

interface SidebarItem {
  id: string;
  label: string;
  icon: React.ElementType;
}

const ComingSoon: React.FC<ComingSoonProps> = ({ item }) => {
  if (!item) return null;

  const Icon = item.icon;

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">{item.label}</h2>
        <p className="text-text-secondary">This section is under development</p>
      </div>
      
      <div className="bg-background-secondary border border-border-primary rounded-lg p-8 text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-pastel rounded-full mb-4">
          <Icon size={32} className="text-primary" />
        </div>
        <h3 className="text-lg font-medium text-text-primary mb-2">Coming Soon</h3>
        <p className="text-text-secondary">This feature will be available soon</p>
      </div>
    </div>
  );
};

export default ComingSoon;