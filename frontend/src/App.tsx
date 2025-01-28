import React from 'react';
import { LegislationDashboard } from '@components/features/LegislationDashboard';
import { ErrorBoundary } from '@components/common/ErrorBoundary';

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold">Legislation Tracker</h1>
          </div>
        </header>
        <main className="container mx-auto px-4 py-8">
          <LegislationDashboard />
        </main>
      </div>
    </ErrorBoundary>
  );
};

export default App;
