from app.scrapers.congress import CongressScraper
from app.scrapers.federal_register import FederalRegisterScraper
from app.scrapers.state import StateLegislatureScraper
from app.scrapers.base import APIKeyMissingError
import sys

def main():
    clear_existing = "--clear" in sys.argv

    try:
        if clear_existing:
            print("Clearing existing data...")
            with CongressScraper() as scraper:
                scraper.clear_existing_data()
            with FederalRegisterScraper() as scraper:
                scraper.clear_existing_data()

        # Scrape federal legislation
        print("Scraping federal legislation...")
        try:
            with CongressScraper() as scraper:
                federal_data = scraper.scrape()
                print(f"Found {len(federal_data)} federal items")
        except APIKeyMissingError as e:
            print(f"Skipping federal legislation: {e}")
        except Exception as e:
            print(f"Error scraping federal legislation: {e}")

        # Scrape executive orders
        print("\nScraping executive orders...")
        try:
            with FederalRegisterScraper() as scraper:
                executive_data = scraper.scrape()
                print(f"Found {len(executive_data)} executive orders")
        except Exception as e:
            print(f"Error scraping executive orders: {e}")

        # Scrape state legislation
        print("\nScraping state legislation...")
        try:
            with StateLegislatureScraper('NY') as scraper:
                state_data = scraper.scrape()
                print(f"Found {len(state_data)} state items")
        except APIKeyMissingError as e:
            print(f"Skipping state legislation: {e}")
        except Exception as e:
            print(f"Error scraping state legislation: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
