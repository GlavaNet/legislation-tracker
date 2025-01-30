import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchLegislation } from '../../utils/api';

const StatusBadge = ({ status }: { status: string }) => {
  const statusColors = {
    ACTIVE: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-100',
    PENDING: 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-100',
    PASSED: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100',
    FAILED: 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-100',
    SIGNED: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-100',
    VETOED: 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-100'
  };

  return (
    <span className={`px-2 py-1 rounded-full text-sm font-medium ${statusColors[status] || 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100'}`}>
      {status}
    </span>
  );
};

const FilterBar = ({ activeTab, onFilterChange }: { 
  activeTab: string;
  onFilterChange: (filters: any) => void;
}) => {
  const [filters, setFilters] = useState({
    status: '',
    year: '',
    congress: '',
    president: ''
  });

  const handleFilterChange = (key: string, value: string) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="flex flex-wrap gap-4 mb-6">
      <select 
        className="px-3 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        value={filters.status}
        onChange={(e) => handleFilterChange('status', e.target.value)}
      >
        <option value="">All Statuses</option>
        <option value="ACTIVE">Active</option>
        <option value="PENDING">Pending</option>
        <option value="PASSED">Passed</option>
        <option value="FAILED">Failed</option>
        <option value="SIGNED">Signed</option>
        <option value="VETOED">Vetoed</option>
      </select>

      <select
        className="px-3 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
        value={filters.year}
        onChange={(e) => handleFilterChange('year', e.target.value)}
      >
        <option value="">All Years</option>
        {Array.from({ length: 15 }, (_, i) => 2024 - i).map(year => (
          <option key={year} value={year}>{year}</option>
        ))}
      </select>

      {activeTab === 'federal' && (
        <select
          className="px-3 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          value={filters.congress}
          onChange={(e) => handleFilterChange('congress', e.target.value)}
        >
          <option value="">All Congresses</option>
          {['118', '117', '116'].map(congress => (
            <option key={congress} value={congress}>{congress}th Congress</option>
          ))}
        </select>
      )}

      {activeTab === 'executive' && (
        <select
          className="px-3 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          value={filters.president}
          onChange={(e) => handleFilterChange('president', e.target.value)}
        >
          <option value="">All Presidents</option>
          <option value="Joseph R. Biden">Biden</option>
          <option value="Donald J. Trump">Trump</option>
          <option value="Barack Obama">Obama</option>
        </select>
      )}
    </div>
  );
};

const Pagination = ({ 
  currentPage, 
  totalPages, 
  onPageChange 
}: { 
  currentPage: number; 
  totalPages: number; 
  onPageChange: (page: number) => void;
}) => (
  <div className="flex justify-center gap-2 mt-6">
    <button
      onClick={() => onPageChange(currentPage - 1)}
      disabled={currentPage === 1}
      className="px-4 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 disabled:opacity-50"
    >
      Previous
    </button>
    
    <div className="flex gap-1">
      {Array.from({ length: totalPages }, (_, i) => i + 1)
        .filter(page => (
          page === 1 || 
          page === totalPages || 
          Math.abs(page - currentPage) <= 2
        ))
        .map((page, i, arr) => (
          <React.Fragment key={page}>
            {i > 0 && arr[i - 1] !== page - 1 && (
              <span className="px-4 py-2 text-gray-600 dark:text-gray-400">...</span>
            )}
            <button
              onClick={() => onPageChange(page)}
              className={`px-4 py-2 border dark:border-gray-600 rounded-lg ${
                currentPage === page 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              {page}
            </button>
          </React.Fragment>
        ))}
    </div>

    <button
      onClick={() => onPageChange(currentPage + 1)}
      disabled={currentPage === totalPages}
      className="px-4 py-2 border dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 disabled:opacity-50"
    >
      Next
    </button>
  </div>
);

const LegislationItem = ({ item, onClick }: { item: any; onClick: (item: any) => void }) => (
  <div 
    className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700 
      transition-all border border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 hover:shadow-md" 
    onClick={() => onClick(item)}
  >
    <div className="space-y-2">
      <div className="flex justify-between items-start">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{item.title}</h3>
        <StatusBadge status={item.status} />
      </div>
      {item.summary && (
        <p className="text-gray-600 dark:text-gray-300 line-clamp-2">{item.summary}</p>
      )}
      <div className="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
        <span>
          {item.introduced_date && 
            `Introduced: ${new Date(item.introduced_date).toLocaleDateString()}`
          }
        </span>
        <span className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300">
          View Details →
        </span>
      </div>
    </div>
  </div>
);

const DetailedView = ({ item, onClose }: { item: any; onClose: () => void }) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-2xl w-full relative">
    <div className="absolute top-4 right-4 space-x-2">
      <StatusBadge status={item.status} />
      <button 
        onClick={onClose}
        className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 text-xl"
      >
        ×
      </button>
    </div>

    <div className="space-y-4 mt-2">
      <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">{item.title}</h2>

      <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 dark:text-gray-300">
        {item.introduced_date && (
          <div>
            <span className="font-medium">Introduced:</span>{' '}
            {new Date(item.introduced_date).toLocaleDateString()}
          </div>
        )}
        {item.last_action_date && (
          <div>
            <span className="font-medium">Last Action:</span>{' '}
            {new Date(item.last_action_date).toLocaleDateString()}
          </div>
        )}
      </div>

      {item.summary && (
        <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
          <h3 className="font-medium text-gray-900 dark:text-white mb-2">Summary</h3>
          <p className="text-gray-700 dark:text-gray-300">{item.summary}</p>
        </div>
      )}

      {item.extra_data && (
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
          <h3 className="font-medium text-gray-900 dark:text-white mb-2">Additional Information</h3>
          <dl className="grid grid-cols-2 gap-x-4 gap-y-2">
            {Object.entries(item.extra_data).map(([key, value]) => (
              <div key={key} className="col-span-1">
                <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">
                  {key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                </dt>
                <dd className="text-sm text-gray-900 dark:text-gray-100">{String(value)}</dd>
              </div>
            ))}
          </dl>
        </div>
      )}

      {item.source_url && (
        <div className="mt-6">
          <a
            href={item.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md 
              hover:bg-blue-700 dark:hover:bg-blue-500 transition-colors"
          >
            View Source
            <span className="ml-2">→</span>
          </a>
        </div>
      )}
    </div>
  </div>
);

export const LegislationDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('federal');
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState({});

  const { data, isLoading, error } = useQuery({
    queryKey: ['legislation', activeTab, currentPage, filters],
    queryFn: () => fetchLegislation(activeTab, currentPage, filters)
  });

  const handleTabChange = (tab: string) => {
    setActiveTab(tab);
    setCurrentPage(1);
    setFilters({});
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
    setCurrentPage(1);
  };

  if (isLoading) return (
    <div className="flex justify-center items-center p-8">
      <div className="text-blue-600 dark:text-blue-400">Loading...</div>
    </div>
  );

  if (error) return (
    <div className="p-4 bg-red-50 dark:bg-red-900 text-red-600 dark:text-red-100 rounded-lg">
      Error: {String(error)}
    </div>
  );

  return (
    <div>
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => handleTabChange('federal')}
          className={`px-6 py-2 rounded-lg transition-colors ${
            activeTab === 'federal' 
              ? 'bg-blue-600 text-white shadow-md' 
              : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Federal
        </button>
        <button
          onClick={() => handleTabChange('executive')}
          className={`px-6 py-2 rounded-lg transition-colors ${
            activeTab === 'executive' 
              ? 'bg-blue-600 text-white shadow-md' 
              : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
          }`}
        >
          Executive Orders
        </button>
      </div>

      <FilterBar activeTab={activeTab} onFilterChange={handleFilterChange} />

      <div className="space-y-4">
        {data?.data?.map((item: any) => (
          <LegislationItem
            key={item.id}
            item={item}
            onClick={setSelectedItem}
          />
        ))}
      </div>

      {data?.pages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={data.pages}
          onPageChange={setCurrentPage}
        />
      )}

      {selectedItem && (
        <div className="fixed inset-0 bg-black/50 dark:bg-black/70 flex items-center justify-center p-4 z-50">
          <DetailedView 
            item={selectedItem} 
            onClose={() => setSelectedItem(null)} 
          />
        </div>
      )}
    </div>
  );
};
