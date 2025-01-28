import React from 'react';
import { Card } from '@/components/common/ui';
import { FileText } from 'lucide-react';

interface Stats {
  federal_count: number;
  state_count: number;
  executive_orders_count: number;
}

interface StatsOverviewProps {
  stats?: Stats;
}

export const StatsOverview: React.FC<StatsOverviewProps> = ({ stats }) => {
  if (!stats) return null;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <Card>
        <div className="p-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-blue-500" />
            <h3 className="font-semibold">Federal Bills</h3>
          </div>
          <p className="text-2xl font-bold mt-2">{stats.federal_count.toLocaleString()}</p>
        </div>
      </Card>
      <Card>
        <div className="p-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-green-500" />
            <h3 className="font-semibold">State Bills</h3>
          </div>
          <p className="text-2xl font-bold mt-2">{stats.state_count.toLocaleString()}</p>
        </div>
      </Card>
      <Card>
        <div className="p-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-purple-500" />
            <h3 className="font-semibold">Executive Orders</h3>
          </div>
          <p className="text-2xl font-bold mt-2">{stats.executive_orders_count.toLocaleString()}</p>
        </div>
      </Card>
    </div>
  );
};
