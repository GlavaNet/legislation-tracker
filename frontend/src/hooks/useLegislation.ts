import { useQuery } from '@tanstack/react-query';
import { fetchLegislation } from '@/utils/api';
import type { Legislation } from '@/types/legislation';

interface UseLegislationParams {
  type: 'federal' | 'state' | 'executive';
  page?: number;
  filters?: Record<string, any>;
}

export const useLegislation = ({ type, page = 1, filters = {} }: UseLegislationParams) => {
  return useQuery({
    queryKey: ['legislation', type, page, filters],
    queryFn: () => fetchLegislation(type, page, filters),
    keepPreviousData: true,
  });
};
