import { useState, useEffect } from 'react';
import { useDebounce } from './useDebounce';

interface UseSearchProps {
  onSearch: (query: string) => void;
  delay?: number;
}

export const useSearch = ({ onSearch, delay = 300 }: UseSearchProps) => {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearch = useDebounce(searchTerm, delay);

  useEffect(() => {
    if (debouncedSearch) {
      onSearch(debouncedSearch);
    }
  }, [debouncedSearch, onSearch]);

  return {
    searchTerm,
    setSearchTerm
  };
};
