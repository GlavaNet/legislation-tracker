import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any
from ratelimit import limits, sleep_and_retry
from .base import BaseScraper, RateLimitError
from ..models import Status, LegislationType, Legislation

class FederalRegisterScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.federalregister.gov/api/v1"
        # Define date ranges for each administration
        self.date_ranges = [
            # Biden Administration
            {
                "start": "2021-01-20",
                "end": datetime.now().strftime("%Y-%m-%d"),
                "president": "Joseph R. Biden"
            },
            # Trump Administration
            {
                "start": "2017-01-20",
                "end": "2021-01-19",
                "president": "Donald J. Trump"
            },
            # Obama Administration (Second Term)
            {
                "start": "2013-01-20",
                "end": "2017-01-19",
                "president": "Barack Obama"
            },
            # Obama Administration (First Term)
            {
                "start": "2009-01-20",
                "end": "2013-01-19",
                "president": "Barack Obama"
            }
        ]

    @sleep_and_retry
    @limits(calls=1000, period=3600)  # 1000 requests per hour
    def _make_request(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make rate-limited API request"""
        url = f"{self.base_url}/documents"
        
        try:
            print(f"Making request to Federal Register API...")
            print(f"Parameters: {params}")
            
            response = requests.get(url, params=params)
            
            if response.status_code == 429:
                raise RateLimitError("Federal Register API rate limit exceeded")
                
            response.raise_for_status()
            data = response.json()
            
            print(f"Received {len(data.get('results', []))} executive orders")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Federal Register: {str(e)}")
            if response is not None:
                print(f"Response content: {response.text[:500]}")
            raise

    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape executive orders from multiple administrations"""
        try:
            total_processed = 0
            current_page = 1

            for date_range in self.date_ranges:
                print(f"\nScraping executive orders from {date_range['start']} to {date_range['end']}...")
                print(f"President: {date_range['president']}")
                
                while True:  # Handle pagination
                    params = {
                        "conditions[type][]": "PRESDOCU",
                        "conditions[presidential_document_type][]": "executive_order",
                        "conditions[publication_date][gte]": date_range['start'],
                        "conditions[publication_date][lte]": date_range['end'],
                        "per_page": 100,
                        "page": current_page,
                        "order": "oldest"
                    }
                    
                    try:
                        data = self._make_request(params)
                        results = data.get("results", [])
                        
                        if not results:
                            break  # No more results for this date range
                        
                        for item in results:
                            try:
                                doc_number = item.get('document_number', '')
                                eo_number = ''.join(filter(str.isdigit, doc_number))
                                
                                # Extract signing date if available, otherwise use publication date
                                signing_date = item.get('signing_date')
                                if signing_date:
                                    try:
                                        date = datetime.strptime(signing_date, "%Y-%m-%d")
                                    except ValueError:
                                        date = datetime.strptime(item['publication_date'], "%Y-%m-%d")
                                else:
                                    date = datetime.strptime(item['publication_date'], "%Y-%m-%d")

                                legislation = Legislation(
                                    id=f"executive_{eo_number}" if eo_number else f"executive_{doc_number}",
                                    type=LegislationType.EXECUTIVE.value,
                                    title=item.get("title", ""),
                                    summary=item.get("abstract", ""),
                                    status=Status.SIGNED.value,
                                    introduced_date=date,
                                    last_action_date=date,  # For EOs, signing date is the last action
                                    source_url=item.get("html_url", ""),
                                    extra_data={
                                        "document_number": doc_number,
                                        "executive_order_number": eo_number,
                                        "president": date_range['president'],
                                        "full_text": item.get("body_html", ""),
                                        "citation": item.get("citation", ""),
                                        "pdf_url": item.get("pdf_url", ""),
                                        "publication_date": item['publication_date'],
                                        "signing_date": signing_date,
                                        "executive_order_notes": item.get("executive_order_notes", []),
                                        "cfr_references": item.get("cfr_references", [])
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
                                    print(f"Updated EO {eo_number}")
                                else:
                                    # Add new record
                                    self.db.add(legislation)
                                    print(f"Added new EO {eo_number}")

                                total_processed += 1
                                if total_processed % 10 == 0:
                                    print(f"Processed {total_processed} executive orders...")
                                    self.db.commit()  # Periodic commit

                            except Exception as e:
                                print(f"Error processing executive order {doc_number}: {str(e)}")
                                continue

                        current_page += 1
                        
                    except Exception as e:
                        print(f"Error processing page {current_page} of {date_range['start']}-{date_range['end']}: {str(e)}")
                        break
                
                current_page = 1  # Reset page counter for next date range
                self.db.commit()  # Commit after each administration

            final_count = self.db.query(Legislation).filter(
                Legislation.type == LegislationType.EXECUTIVE.value
            ).count()
            print(f"\nFinal executive order count: {final_count}")
            
            return self.db.query(Legislation).filter(
                Legislation.type == LegislationType.EXECUTIVE.value
            ).all()
            
        except Exception as e:
            print(f"Error in scrape: {str(e)}")
            self.db.rollback()
            raise
