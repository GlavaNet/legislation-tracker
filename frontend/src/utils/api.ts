import config from '@/config';
import type { Legislation, PaginatedResponse } from '@/types/legislation';

export const fetchLegislation = async (
  type: string,
  page: number = 1,
  filters: Record<string, any> = {}
): Promise<PaginatedResponse<Legislation>> => {
  const params = new URLSearchParams({
    page: page.toString(),
    limit: config.PAGE_SIZE.toString(),
    ...filters
  });

  const response = await fetch(
    `${config.API_URL}/api/${config.API_VERSION}/${type}?${params}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch legislation: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

export const searchLegislation = async (
  query: string,
  type?: string
): Promise<PaginatedResponse<Legislation>> => {
  if (!query.trim()) {
    throw new Error('Search query cannot be empty');
  }

  const params = new URLSearchParams({
    q: query,
    ...(type && { type })
  });

  const response = await fetch(
    `${config.API_URL}/api/${config.API_VERSION}/search?${params}`
  );

  if (!response.ok) {
    throw new Error(`Search failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
};

