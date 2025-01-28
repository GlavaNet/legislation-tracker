const config = {
  API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  API_VERSION: 'v1',
  DATE_FORMAT: 'MMM dd, yyyy',
  STALE_TIME: 5 * 60 * 1000, // 5 minutes
  PAGE_SIZE: 20
} as const;

export default config;
