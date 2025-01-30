interface FilterParams {
  status?: string;
  year?: string;
  congress?: string;
  president?: string;
}

export const fetchLegislation = async (
  type: string,
  page: number = 1,
  filters: FilterParams = {}
) => {
  try {
    // Remove empty filter values
    const cleanFilters = Object.fromEntries(
      Object.entries(filters).filter(([_, value]) => value !== '')
    );

    // Build query parameters
    const params = new URLSearchParams({
      page: page.toString(),
      ...cleanFilters
    });

    const response = await fetch(`/api/v1/${type}?${params}`);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`API Error: ${errorText}`);
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log(`Fetched ${type} data:`, data);
    return data;
  } catch (error) {
    console.error(`Error fetching ${type} legislation:`, error);
    throw error;
  }
};
