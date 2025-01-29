#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting data scraping...${NC}"

cd backend
source venv/bin/activate

# Create a Python script to run scrapers
cat > run_scrapers.py << 'EOF'
from app.scrapers.congress import CongressScraper
from app.scrapers.federal_register import FederalRegisterScraper
from app.scrapers.state import StateLegislatureScraper
from app.scrapers.base import APIKeyMissingError
import sys

def main():
    clear_existing = "--clear" in sys.argv

    try:
        # Scrape federal legislation
        print("Scraping federal legislation...")
        try:
            with CongressScraper() as scraper:
                if clear_existing:
                    scraper.clear_existing_data()
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
                if clear_existing:
                    scraper.clear_existing_data()
                executive_data = scraper.scrape()
                print(f"Found {len(executive_data)} executive orders")
        except Exception as e:
            print(f"Error scraping executive orders: {e}")

        # Scrape state legislation (example with NY)
        print("\nScraping state legislation...")
        try:
            with StateLegislatureScraper('NY') as scraper:
                if clear_existing:
                    scraper.clear_existing_data()
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
EOF

# Run the scrapers
if [ "$1" == "--clear" ]; then
    echo -e "${YELLOW}Clearing existing data...${NC}"
    python run_scrapers.py --clear
else
    python run_scrapers.py
fi

echo -e "${GREEN}Scraping complete!${NC}"
