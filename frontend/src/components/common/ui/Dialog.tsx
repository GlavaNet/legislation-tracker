import React from 'react';

export const Dialog = ({ children, open = false }: { children: React.ReactNode; open?: boolean }) => (
  open ? <div className="fixed inset-0 bg-black/50 flex items-center justify-center">{children}</div> : null
);

export const DialogTitle = ({ children }: { children: React.ReactNode }) => (
  <h2 className="text-lg font-semibold">{children}</h2>
);

export const DialogContent = ({ children }: { children: React.ReactNode }) => (
  <div className="bg-white p-6 rounded-lg max-w-2xl w-full mx-4">{children}</div>
);

export const DialogHeader = ({ children }: { children: React.ReactNode }) => (
  <div className="mb-4">{children}</div>
);

export const DialogClose = ({ children }: { children: React.ReactNode }) => (
  <button className="absolute top-4 right-4">{children}</button>
);
