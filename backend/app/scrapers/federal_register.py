import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .base import BaseScraper, RateLimitError

class FederalRegisterScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.federalregister.gov/api/v1"

    @sleep_and_retry
    @limits(calls=1000, period=3600)  # 1000 requests per hour
    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make rate-limited API request"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 429:
                raise RateLimitError("Federal Register API rate limit exceeded")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to Federal Register: {str(e)}")
            raise

    def scrape(self, days: int = 30) -> List[Dict[str, Any]]:
        """Scrape executive orders"""
        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            params = {
                "conditions[type]": "PRESDOCU",
                "conditions[presidential_document_type]": "executive_order",
                "conditions[publication_date][gte]": start_date,
                "per_page": 100,
                "order": "newest"
            }
            
            data = self._make_request("documents", params)
            legislation_list = []
            
            for item in data.get("results", []):
                legislation = {
                    "id": f"executive_{item['executive_order_number']}",
                    "type": "executive",
                    "title": item["title"],
                    "summary": item.get("abstract", ""),
                    "status": "signed",
                    "introduced_date": datetime.strptime(
                        item["signing_date"], "%Y-%m-%d"
                    ),
                    "source_url": item["html_url"],
                    "metadata": {
                        "executive_order_number": item["executive_order_number"],
                        "president": item.get("president"),
                        "full_text": item.get("body_html"),
                        "citation": item.get("citation")
                    }
                }
                legislation_list.append(legislation)
                self.save_legislation(legislation)
            
            return legislation_list
            
        except Exception as e:
            self.logger.error(f"Error scraping Federal Register: {str(e)}")
            raise
