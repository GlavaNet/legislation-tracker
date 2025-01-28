import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Tabs, TabsList, TabsTrigger } from '@/components/common/ui';
import { LegislationCard } from './LegislationCard';
import { DetailedView } from './DetailedView';
import { FilterBar } from './FilterBar';
import { StatsOverview } from './StatsOverview';
import { Pagination } from './Pagination';
import { fetchLegislation } from '@/utils/api';
import type { Legislation } from '@/types/legislation';

export const LegislationDashboard: React.FC = () => {
  const [activeView, setActiveView] = useState<'federal' | 'state' | 'executive'>('federal');
  const [page, setPage] = useState(1);
  const [selectedLegislation, setSelectedLegislation] = useState<Legislation | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');

  const { data, isLoading, error } = useQuery({
    queryKey: ['legislation', activeView, page, searchTerm, filterType],
    queryFn: () => fetchLegislation(activeView, page, {
      search: searchTerm,
      type: filterType !== 'all' ? filterType : undefined
    })
  });

  if (isLoading) return <div className="flex justify-center p-8">Loading...</div>;
  if (error) return <div className="text-red-500 p-4">Error loading data</div>;

  return (
    <div className="space-y-6">
      <StatsOverview stats={data?.stats} />
      
      <FilterBar
        searchTerm={searchTerm}
        onSearchChange={setSearchTerm}
        filterType={filterType}
        onFilterChange={setFilterType}
      />

      <Tabs value={activeView} onValueChange={(value) => setActiveView(value as typeof activeView)}>
        <TabsList>
          <TabsTrigger value="federal">Federal</TabsTrigger>
          <TabsTrigger value="state">State</TabsTrigger>
          <TabsTrigger value="executive">Executive Orders</TabsTrigger>
        </TabsList>
      </Tabs>

      <div className="grid gap-4">
        {data?.data.map((item) => (
          <LegislationCard
            key={item.id}
            legislation={item}
            onClick={() => setSelectedLegislation(item)}
          />
        ))}
      </div>

      {data && (
        <Pagination
          currentPage={page}
          totalPages={Math.ceil(data.total / data.limit)}
          onPageChange={setPage}
        />
      )}

      {selectedLegislation && (
        <DetailedView
          legislation={selectedLegislation}
          isOpen={true}
          onClose={() => setSelectedLegislation(null)}
        />
      )}
    </div>
  );
};
