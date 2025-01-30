import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../common/ui/Tabs';
import { Card, CardHeader, CardTitle, CardContent } from '../common/ui/Card';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../common/ui/Dialog';
import { fetchLegislation } from '../../utils/api';

export const LegislationDashboard: React.FC = () => {
  const [activeView, setActiveView] = useState<'federal' | 'state' | 'executive'>('federal');
  const [selectedLegislation, setSelectedLegislation] = useState<any>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['legislation', activeView],
    queryFn: () => fetchLegislation(activeView)
  });

  const handleTabChange = (value: string) => {
    console.log('Changing tab to:', value);
    setActiveView(value as typeof activeView);
  };

  const handleLegislationClick = (item: any) => {
    console.log('Selected legislation:', item);
    setSelectedLegislation(item);
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-red-500">
        Error loading data: {error instanceof Error ? error.message : 'Unknown error'}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Tabs value={activeView} onChange={handleTabChange}>
        <TabsList>
          <TabsTrigger value="federal" onClick={() => handleTabChange('federal')}>
            Federal
          </TabsTrigger>
          <TabsTrigger value="state" onClick={() => handleTabChange('state')}>
            State
          </TabsTrigger>
          <TabsTrigger value="executive" onClick={() => handleTabChange('executive')}>
            Executive Orders
          </TabsTrigger>
        </TabsList>

        <TabsContent value={activeView === 'federal' ? 'federal' : ''}>
          <div className="space-y-4">
            {activeView === 'federal' && data?.data?.map((item: any) => (
              <Card 
                key={item.id} 
                className="p-4 cursor-pointer hover:bg-gray-50"
                onClick={() => handleLegislationClick(item)}
              >
                <CardHeader>
                  <CardTitle>{item.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-gray-500">
                    Status: {item.status}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value={activeView === 'state' ? 'state' : ''}>
          <div className="space-y-4">
            {activeView === 'state' && (
              <div>State legislation coming soon...</div>
            )}
          </div>
        </TabsContent>

        <TabsContent value={activeView === 'executive' ? 'executive' : ''}>
          <div className="space-y-4">
            {activeView === 'executive' && data?.data?.map((item: any) => (
              <Card 
                key={item.id} 
                className="p-4 cursor-pointer hover:bg-gray-50"
                onClick={() => handleLegislationClick(item)}
              >
                <CardHeader>
                  <CardTitle>{item.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-gray-500">
                    Status: {item.status}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      <Dialog open={!!selectedLegislation}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{selectedLegislation?.title}</DialogTitle>
            <button 
              onClick={() => setSelectedLegislation(null)}
              className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
            >
              Close
            </button>
          </DialogHeader>
          <div className="mt-4">
            <p className="text-sm text-gray-600">{selectedLegislation?.summary}</p>
            {selectedLegislation?.source_url && (
              <a 
                href={selectedLegislation.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 text-blue-500 hover:underline block"
              >
                View Source
              </a>
            )}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};
