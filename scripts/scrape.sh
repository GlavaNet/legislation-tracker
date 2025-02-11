#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting data scraping...${NC}"

# Run scrapers through Docker with proper virtual environment activation
docker-compose exec web bash -c "source /app/app/venv/bin/activate && cd /app && python3 run_scrapers.py"

echo -e "${GREEN}Scraping complete!${NC}"
