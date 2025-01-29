from datetime import datetime
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
from .base import BaseScraper, APIKeyMissingError

class StateLegislatureScraper(BaseScraper):
    def __init__(self, state: str):
        super().__init__()
        self.state = state.upper()
        self.api_key = self._get_state_api_key()
        self.config = self._get_state_config()

    def _get_state_api_key(self) -> Optional[str]:
        """Get API key for specific state if required"""
        key_mapping = {
            'NY': self.settings.NY_LEGISLATURE_API_KEY,
            'CA': self.settings.CA_LEGISLATURE_API_KEY,
            # Add more states as needed
        }
        return key_mapping.get(self.state)

    def _get_state_config(self) -> Dict[str, Any]:
        """Get configuration for specific state"""
        configs = {
            'NY': {
                'requires_key': True,
                'base_url': 'https://legislation.nysenate.gov/api/v1',
                'rate_limit': {'calls': 1000, 'period': 3600}
            },
            'CA': {
                'requires_key': False,
                'base_url': 'https://leginfo.legislature.ca.gov/faces/billSearchClient.xhtml',
                'rate_limit': {'calls': 100, 'period': 3600}
            }
            # Add more states as needed
        }
        
        config = configs.get(self.state)
        if not config:
            raise ValueError(f"State {self.state} not supported")
            
        if config['requires_key'] and not self.api_key:
            raise APIKeyMissingError(f"API key required for {self.state} legislature")
            
        return config

    @sleep_and_retry
    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """Make rate-limited API request"""
        url = f"{self.config['base_url']}/{endpoint}"
        headers = {}
        
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error making request to {self.state} legislature: {str(e)}")
            raise

    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape state legislation based on state-specific implementation"""
        try:
            if self.state == 'NY':
                return self._scrape_ny()
            elif self.state == 'CA':
                return self._scrape_ca()
            else:
                raise ValueError(f"Scraping not implemented for state: {self.state}")
        except Exception as e:
            self.logger.error(f"Error scraping {self.state} legislature: {str(e)}")
            raise

    def _scrape_ny(self) -> List[Dict[str, Any]]:
        """Scrape New York state legislation"""
        data = self._make_request("bills/current")
        legislation_list = []
        
        for item in data.get("bills", []):
            legislation = {
                "id": f"state_ny_{item['printNo']}",
                "type": "state",
                "title": item["title"],
                "summary": item.get("summary", ""),
                "status": item.get("status", ""),
                "introduced_date": datetime.strptime(
                    item["publishedDate"], "%Y-%m-%d"
                ),
                "source_url": item.get("url", ""),
               "extra_data": {  # Changed from metadata to extra_data
                    "state": "NY",
                    "bill_id": item.get("printNo"),
                    "session": item.get("session")
                }
            }
            legislation_list.append(legislation)
            self.save_legislation(legislation)
        
        return legislation_list

    def _scrape_ca(self) -> List[Dict[str, Any]]:
        """Scrape California state legislation"""
        # Implementation for California's web scraping approach
        pass
