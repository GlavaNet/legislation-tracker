import { format, formatDistance, parseISO } from 'date-fns';
import config from '@/config';

export const formatDate = (date: string | Date): string => {
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return format(parsedDate, config.DATE_FORMAT);
  } catch {
    return 'Invalid date';
  }
};

export const getTimeAgo = (date: string | Date): string => {
  try {
    const parsedDate = typeof date === 'string' ? parseISO(date) : date;
    return formatDistance(parsedDate, new Date(), { addSuffix: true });
  } catch {
    return 'Unknown';
  }
};
