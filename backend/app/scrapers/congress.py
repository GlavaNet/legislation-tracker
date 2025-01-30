from datetime import datetime
from typing import List, Dict, Any
import requests
from sqlalchemy import text
from .base import BaseScraper, APIKeyMissingError
from ..models import Status, LegislationType, Legislation

class CongressScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.api_key = self.settings.CONGRESS_API_KEY
        self.base_url = self.settings.CONGRESS_API_BASE_URL
        self.validate_api_key(self.api_key, "Congress.gov")
        # Congress numbers to scrape (starting from 116th Congress in 2019)
        self.congresses = ["118", "117", "116"]

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint}"
        try:
            print(f"Making request to: {url}")
            response = requests.get(url, params={
                "api_key": self.api_key,
                "format": "json",
                "limit": 250,  # Request more items per page
                "offset": 0
            })
            response.raise_for_status()
            data = response.json()
            print(f"Received response with {len(data.get('bills', []))} bills")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {str(e)}")
            if response is not None:
                print(f"Response content: {response.text[:500]}")
            raise

    def _determine_status(self, item: Dict[str, Any]) -> Status:
        """Determine the current status of a bill based on its history"""
        status_text = item.get('status', '').lower()
        latest_action = item.get('latestAction', {}).get('text', '').lower()
        
        # Check for final statuses first
        if any(term in status_text or term in latest_action for term in ['enacted', 'became law']):
            return Status.SIGNED
        elif 'vetoed' in status_text or 'vetoed' in latest_action:
            return Status.VETOED
        elif any(term in status_text or term in latest_action for term in ['failed', 'rejected']):
            return Status.FAILED
        
        # Check for in-progress statuses
        elif any(term in latest_action for term in ['passed', 'agreed to in']):
            return Status.PASSED
        elif any(term in latest_action for term in ['introduced', 'referred to committee']):
            return Status.ACTIVE
        else:
            return Status.PENDING

    def scrape(self) -> List[Dict[str, Any]]:
        try:
            print("Starting federal legislation scrape...")
            total_processed = 0

            for congress in self.congresses:
                print(f"\nScraping {congress}th Congress...")
                try:
                    data = self._make_request(f"bill/{congress}")
                    bills = data.get('bills', [])
                    
                    for item in bills:
                        try:
                            bill_type = item.get('type', '').lower()
                            bill_number = item.get('number', '')
                            
                            # Construct source URL for Congress.gov
                            source_url = f"https://www.congress.gov/bill/{congress}th-congress/{bill_type}/{bill_number}"
                            
                            # Process dates
                            introduced_date = None
                            if "introducedDate" in item:
                                try:
                                    introduced_date = datetime.strptime(item["introducedDate"], "%Y-%m-%d")
                                except ValueError:
                                    print(f"Invalid introduced date format for bill {bill_number}")
                            
                            # Process latest action date
                            last_action_date = None
                            if item.get("latestAction", {}).get("actionDate"):
                                try:
                                    last_action_date = datetime.strptime(
                                        item["latestAction"]["actionDate"], 
                                        "%Y-%m-%d"
                                    )
                                except ValueError:
                                    print(f"Invalid action date format for bill {bill_number}")

                            legislation = Legislation(
                                id=f"federal_{congress}_{bill_type}_{bill_number}",
                                type=LegislationType.FEDERAL.value,
                                title=item["title"],
                                summary=item.get("summary", ""),
                                status=self._determine_status(item).value,
                                introduced_date=introduced_date,
                                last_action_date=last_action_date,
                                source_url=source_url,
                                extra_data={
                                    "congress": congress,
                                    "bill_type": bill_type,
                                    "bill_number": bill_number,
                                    "sponsors": item.get("sponsors", []),
                                    "committees": item.get("committees", []),
                                    "latest_action": item.get("latestAction", {}),
                                    "related_bills": item.get("relatedBills", []),
                                    "subjects": item.get("subjects", [])
                                }
                            )
                            
                            # Check for existing record
                            existing = self.db.query(Legislation).filter(
                                Legislation.id == legislation.id
                            ).first()
                            
                            if existing:
                                # Update existing record
                                for key, value in legislation.__dict__.items():
                                    if key != '_sa_instance_state':
                                        setattr(existing, key, value)
                                print(f"Updated bill {congress} {bill_type} {bill_number}")
                            else:
                                # Add new record
                                self.db.add(legislation)
                                print(f"Added new bill {congress} {bill_type} {bill_number}")
                            
                            total_processed += 1
                            if total_processed % 10 == 0:
                                print(f"Processed {total_processed} bills...")
                                self.db.commit()  # Periodic commit
                            
                        except Exception as e:
                            print(f"Error processing bill {bill_number}: {str(e)}")
                            continue
                    
                    self.db.commit()
                    print(f"Completed {congress}th Congress")
                    
                except Exception as e:
                    print(f"Error processing {congress}th Congress: {str(e)}")
                    continue

            final_count = self.db.query(Legislation).filter(
                Legislation.type == LegislationType.FEDERAL.value
            ).count()
            print(f"\nFinal federal bill count: {final_count}")
            
            return self.db.query(Legislation).filter(
                Legislation.type == LegislationType.FEDERAL.value
            ).all()
            
        except Exception as e:
            print(f"Error in scrape: {str(e)}")
            self.db.rollback()
            raise
