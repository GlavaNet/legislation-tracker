import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from .base import BaseScraper
from ..config import get_settings
from ..models import LegislationType

settings = get_settings()

class CongressScraper(BaseScraper):
    @sleep_and_retry
    @limits(calls=10, period=60)
    def scrape(self) -> List[Dict[str, Any]]:
        url = f"{settings.CONGRESS_API_BASE_URL}/bills"
        headers = {"X-API-Key": settings.CONGRESS_API_KEY} if settings.CONGRESS_API_KEY else {}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        legislation_list = []
        for item in data.get("bills", []):
            legislation = {
                "id": f"federal_{item['number']}",
                "type": LegislationType.FEDERAL,
                "title": item["title"],
                "summary": item.get("summary", ""),
                "status": item.get("status", ""),
                "introduced_date": datetime.strptime(item["introducedDate"], "%Y-%m-%d"),
                "source_url": item.get("congressdotgov_url", ""),
                "metadata": {
                    "congress": item.get("congress"),
                    "bill_type": item.get("type"),
                    "bill_number": item.get("number")
                }
            }
            legislation_list.append(legislation)
            self.save_legislation(legislation)

        return legislation_list

class StateLegislatureScraper(BaseScraper):
    def __init__(self, state: str):
        super().__init__()
        self.state = state

    @sleep_and_retry
    @limits(calls=5, period=60)
    def scrape(self) -> List[Dict[str, Any]]:
        # Implementation specific to state legislature websites
        pass

class FederalRegisterScraper(BaseScraper):
    @sleep_and_retry
    @limits(calls=10, period=60)
    def scrape(self) -> List[Dict[str, Any]]:
        url = "https://www.federalregister.gov/api/v1/documents"
        params = {
            "conditions[type]": "PRESDOCU",
            "conditions[presidential_document_type]": "executive_order",
            "per_page": 100
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        legislation_list = []
        for item in data.get("results", []):
            legislation = {
                "id": f"executive_{item['executive_order_number']}",
                "type": LegislationType.EXECUTIVE,
                "title": item["title"],
                "summary": item.get("abstract", ""),
                "status": "signed",
                "introduced_date": datetime.strptime(item["signing_date"], "%Y-%m-%d"),
                "source_url": item["html_url"],
                "metadata": {
                    "executive_order_number": item["executive_order_number"],
                    "president": item.get("president")
                }
            }
            legislation_list.append(legislation)
            self.save_legislation(legislation)

        return legislation_list
