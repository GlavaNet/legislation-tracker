import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../common/ui/Tabs';
import { Card } from '../common/ui/Card';
import { fetchLegislation } from '../../utils/api';

export const LegislationDashboard: React.FC = () => {
  const [activeView, setActiveView] = useState<'federal' | 'state' | 'executive'>('federal');

  const { data, isLoading, error } = useQuery({
    queryKey: ['legislation', activeView],
    queryFn: () => fetchLegislation(activeView)
  });

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
        Error loading data. Please try again later.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Tabs value={activeView} onChange={(value) => setActiveView(value as typeof activeView)}>
        <TabsList>
          <TabsTrigger value="federal">Federal</TabsTrigger>
          <TabsTrigger value="state">State</TabsTrigger>
          <TabsTrigger value="executive">Executive Orders</TabsTrigger>
        </TabsList>

        <TabsContent value="federal">
          <div className="space-y-4">
            {data?.data?.map((item: any) => (
              <Card key={item.id} className="p-4">
                <h3 className="text-lg font-semibold">{item.title}</h3>
                {item.summary && <p className="mt-2 text-gray-600">{item.summary}</p>}
              </Card>
            )) || <div>No federal legislation found.</div>}
          </div>
        </TabsContent>

        <TabsContent value="state">
          <div>State legislation coming soon...</div>
        </TabsContent>

        <TabsContent value="executive">
          <div>Executive orders coming soon...</div>
        </TabsContent>
      </Tabs>
    </div>
  );
};
