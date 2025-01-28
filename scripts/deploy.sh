#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Deployment configuration
DEPLOY_ENV=${1:-production}
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups/${TIMESTAMP}"

# Error handling
set -e
trap 'handle_error $? $LINENO' ERR

handle_error() {
    echo -e "${RED}Error occurred in deployment script on line $2${NC}"
    cleanup_failed_deploy
    exit 1
}

cleanup_failed_deploy() {
    echo -e "${YELLOW}Cleaning up failed deployment...${NC}"
    # Add cleanup logic here
}

# Create backup
mkdir -p "$BACKUP_DIR"
echo "Creating backup in ${BACKUP_DIR}"

# Build and test frontend
echo -e "${YELLOW}Building frontend...${NC}"
cd frontend
npm ci
npm run test -- --watchAll=false
npm run build

# Build and test backend
echo -e "${YELLOW}Building backend...${NC}"
cd ../backend
python -m pytest
python -m build

# Deploy using Docker
echo -e "${YELLOW}Deploying with Docker...${NC}"
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Health checks
echo -e "${YELLOW}Performing health checks...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        echo -e "${GREEN}Backend health check passed${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Backend health check failed${NC}"
        exit 1
    fi
    sleep 1
done

echo -e "${GREEN}Deployment completed successfully!${NC}"
