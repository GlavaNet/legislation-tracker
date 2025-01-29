import { useMemo } from 'react';

export const usePagination = ({
  totalItems,
  pageSize,
  currentPage
}: {
  totalItems: number;
  pageSize: number;
  currentPage: number;
}) => {
  return useMemo(() => {
    const totalPages = Math.ceil(totalItems / pageSize);
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }, [totalItems, pageSize, currentPage]);
};
