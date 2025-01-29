export const fetchLegislation = async (type: string) => {
  try {
    console.log(`Fetching from: /api/v1/${type}`);
    const response = await fetch(`/api/v1/${type}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const text = await response.text(); // Get raw response
    console.log('Raw response:', text);
    const data = JSON.parse(text);
    return data;
  } catch (error) {
    console.error('Error fetching legislation:', error);
    return { data: [], total: 0, page: 1, limit: 20 };
  }
};
