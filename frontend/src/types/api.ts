export interface ApiError {
  status: number;
  message: string;
  details?: Record<string, any>;
}

export interface ApiResponse<T> {
  data: T;
  meta?: {
    timestamp: string;
    version: string;
  };
}
