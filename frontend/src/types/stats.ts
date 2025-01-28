export interface LegislationStats {
  federal_count: number;
  state_count: number;
  executive_orders_count: number;
  recent_activity?: {
    date: string;
    type: LegislationType;
    description: string;
  }[];
}
