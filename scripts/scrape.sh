#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting data scraping...${NC}"

cd backend
source venv/bin/activate

# Run the scrapers
if [ "$1" == "--clear" ]; then
    echo -e "${YELLOW}Clearing existing data...${NC}"
    python run_scrapers.py --clear
else
    python run_scrapers.py
fi

echo -e "${GREEN}Scraping complete!${NC}"
