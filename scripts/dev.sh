#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Store PIDs for cleanup
declare -a PIDS

# Error handling
trap 'kill_processes' SIGINT SIGTERM EXIT

# Function to kill all background processes
kill_processes() {
    echo -e "\n${YELLOW}Shutting down development servers...${NC}"
    for pid in "${PIDS[@]}"; do
        if ps -p $pid > /dev/null; then
            kill $pid 2>/dev/null
        fi
    done
    exit 0
}

# Check if ports are available
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}Port 8000 is already in use${NC}"
    exit 1
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "${RED}Port 3000 is already in use${NC}"
    exit 1
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start backend server with logging
echo -e "${YELLOW}Starting backend server...${NC}"
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --log-level debug 2>&1 | tee ../logs/backend.log &
PIDS+=($!)

# Wait for backend to start
echo "Waiting for backend server..."
until curl -s http://localhost:8000/health > /dev/null; do
    sleep 1
done
echo -e "${GREEN}Backend server started successfully!${NC}"

# Start frontend server with logging
echo -e "${YELLOW}Starting frontend server...${NC}"
cd ../frontend
npm run dev -- --host 2>&1 | tee ../logs/frontend.log &
PIDS+=($!)

# Print development URLs
echo -e "\n${GREEN}Development servers started:${NC}"
echo -e "Frontend: ${YELLOW}http://$(hostname -I | awk '{print $1}'):3000${NC}"
echo -e "Backend API: ${YELLOW}http://$(hostname -I | awk '{print $1}'):8000${NC}"
echo -e "API Documentation: ${YELLOW}http://$(hostname -I | awk '{print $1}'):8000/docs${NC}"

# Show logs in real-time
echo -e "\n${YELLOW}Showing combined logs:${NC}"
tail -f ../logs/*.log

# Keep script running
wait
