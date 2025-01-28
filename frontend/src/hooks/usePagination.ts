import { useMemo } from 'react';

interface UsePaginationProps {
  totalItems: number;
  pageSize: number;
  currentPage: number;
  siblingCount?: number;
}

export const usePagination = ({
  totalItems,
  pageSize,
  currentPage,
  siblingCount = 1
}: UsePaginationProps) => {
  return useMemo(() => {
    const totalPages = Math.ceil(totalItems / pageSize);
    const pages = generatePaginationArray(totalPages, currentPage, siblingCount);
    return pages;
  }, [totalItems, pageSize, currentPage, siblingCount]);
};
