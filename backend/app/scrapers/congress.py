import requests
from datetime import datetime
from typing import List, Dict, Any
from .base import BaseScraper, APIKeyMissingError, RateLimitError

class CongressScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.api_key = self.settings.CONGRESS_API_KEY
        self.base_url = self.settings.CONGRESS_API_BASE_URL
        self.validate_api_key(self.api_key, "Congress.gov")

    @sleep_and_retry
    @limits(calls=1000, period=3600)  # 1000 requests per hour
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make rate-limited API request"""
        url = f"{self.base_url}/{endpoint}"
        headers = {"X-API-Key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 429:
                raise RateLimitError("Congress.gov API rate limit exceeded")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to Congress.gov: {str(e)}")
            raise

    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape federal legislation"""
        try:
            data = self._make_request("bills")
            legislation_list = []
            
            for item in data.get("bills", []):
                legislation = {
                    "id": f"federal_{item['number']}",
                    "type": "federal",
                    "title": item["title"],
                    "summary": item.get("summary", ""),
                    "status": item.get("status", ""),
                    "introduced_date": datetime.strptime(
                        item["introducedDate"], "%Y-%m-%d"
                    ),
                    "last_action_date": datetime.strptime(
                        item["latestAction"]["actionDate"], "%Y-%m-%d"
                    ) if item.get("latestAction") else None,
                    "source_url": item.get("congressdotgov_url", ""),
                    "metadata": {
                        "congress": item.get("congress"),
                        "bill_type": item.get("type"),
                        "bill_number": item.get("number"),
                        "committees": item.get("committees", []),
                        "sponsors": item.get("sponsors", [])
                    }
                }
                legislation_list.append(legislation)
                self.save_legislation(legislation)
            
            return legislation_list
            
        except Exception as e:
            self.logger.error(f"Error scraping Congress.gov: {str(e)}")
            raise
