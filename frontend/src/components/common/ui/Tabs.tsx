import React from 'react';

export const Tabs = ({ children, value, onChange }: { children: React.ReactNode; value?: string; onChange?: (value: string) => void }) => (
  <div>{children}</div>
);

export const TabsList = ({ children }: { children: React.ReactNode }) => (
  <div className="flex space-x-2 mb-4">{children}</div>
);

export const TabsTrigger = ({ children, value }: { children: React.ReactNode; value: string }) => (
  <button className="px-4 py-2 rounded-lg hover:bg-gray-100">{children}</button>
);

export const TabsContent = ({ children, value }: { children: React.ReactNode; value: string }) => (
  <div>{children}</div>
);
