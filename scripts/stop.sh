#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping development servers...${NC}"

# Stop uvicorn
if pgrep -f uvicorn > /dev/null; then
    echo "Stopping uvicorn server..."
    pkill -f uvicorn
fi

# Stop vite
if pgrep -f vite > /dev/null; then
    echo "Stopping vite server..."
    pkill -f vite
fi

# Verify all processes are stopped
sleep 2
if pgrep -f "uvicorn|vite" > /dev/null; then
    echo -e "${RED}Some processes could not be stopped gracefully. Using force...${NC}"
    pkill -9 -f "uvicorn|vite"
else
    echo -e "${GREEN}All services stopped successfully${NC}"
fi
