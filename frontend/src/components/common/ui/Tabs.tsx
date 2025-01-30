import React from 'react';

interface TabsProps {
  children: React.ReactNode;
  value?: string;
  onChange: (value: string) => void;
  defaultValue?: string;
}

export const Tabs: React.FC<TabsProps> = ({ children, value, onChange, defaultValue }) => (
  <div className="tabs">{children}</div>
);

export const TabsList: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <div className="flex space-x-2 mb-4 border-b">{children}</div>
);

interface TabsTriggerProps {
  children: React.ReactNode;
  value: string;
  onClick?: () => void;
}

export const TabsTrigger: React.FC<TabsTriggerProps> = ({ children, value, onClick }) => (
  <button
    className="px-4 py-2 hover:bg-gray-100 border-b-2 border-transparent hover:border-gray-300 focus:outline-none focus:border-blue-500"
    onClick={onClick}
  >
    {children}
  </button>
);

interface TabsContentProps {
  children: React.ReactNode;
  value: string;
}

export const TabsContent: React.FC<TabsContentProps> = ({ children, value }) => (
  <div className="py-4">{children}</div>
);
