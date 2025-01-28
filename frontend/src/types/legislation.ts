export type LegislationType = 'federal' | 'state' | 'executive';

export type LegislationStatus =
  | 'active'
  | 'pending'
  | 'passed'
  | 'failed'
  | 'signed'
  | 'vetoed';

export interface Legislation {
  id: string;
  type: LegislationType;
  title: string;
  summary?: string;
  status?: LegislationStatus;
  introduced_date?: string;
  last_action_date?: string;
  source_url?: string;
  metadata: Record<string, any>;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

export interface LegislationFilters {
  search?: string;
  status?: LegislationStatus;
  startDate?: string;
  endDate?: string;
  type?: LegislationType;
}
