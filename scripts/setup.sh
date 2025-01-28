#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error handling
set -e
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
trap 'echo -e "${RED}\"${last_command}\" command failed with exit code $?.${NC}"' EXIT

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print section header
print_section() {
    echo -e "\n${YELLOW}=== $1 ===${NC}\n"
}

# Check system requirements
print_section "Checking System Requirements"

# Check Python version
if command_exists python3; then
    python3 --version
else
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Node.js version
if command_exists node; then
    node --version
else
    echo -e "${RED}Node.js is not installed. Please install Node.js 14 or higher.${NC}"
    exit 1
fi

# Check if pip is installed
if command_exists pip3; then
    pip3 --version
else
    echo -e "${RED}pip3 is not installed. Please install pip3.${NC}"
    exit 1
fi

# Check if npm is installed
if command_exists npm; then
    npm --version
else
    echo -e "${RED}npm is not installed. Please install npm.${NC}"
    exit 1
fi

# Create and activate virtual environment
print_section "Setting up Python Virtual Environment"
if [ ! -d "backend/venv" ]; then
    python3 -m venv backend/venv
fi
source backend/venv/bin/activate

# Install backend dependencies
print_section "Installing Backend Dependencies"
cd backend
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
print_section "Initializing Database"
alembic upgrade head

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}Created .env file. Please update it with your configurations.${NC}"
fi

# Install frontend dependencies
print_section "Installing Frontend Dependencies"
cd ../frontend
npm install

# Create frontend environment file
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo "REACT_APP_API_URL=http://localhost:8000" > .env
    echo "REACT_APP_API_VERSION=v1" >> .env
    echo -e "${GREEN}Created frontend .env file.${NC}"
fi

# Install git hooks
print_section "Setting up Git Hooks"
cd ..
if [ -d ".git" ]; then
    if [ ! -f ".git/hooks/pre-commit" ]; then
        cp scripts/git-hooks/pre-commit .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
        echo -e "${GREEN}Installed git pre-commit hook.${NC}"
    fi
fi

# Setup development tools
print_section "Setting up Development Tools"

# Install global development tools
npm install -g prettier eslint typescript

# Run initial tests
print_section "Running Initial Tests"

# Backend tests
cd backend
python -m pytest

# Frontend tests
cd ../frontend
npm test -- --watchAll=false

# Final setup steps
print_section "Final Setup Steps"

# Create necessary directories
mkdir -p backend/logs
mkdir -p backend/data

# Set permissions
chmod -R 755 backend/logs
chmod -R 755 backend/data

# Print setup completion message
print_section "Setup Complete"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "\nTo start the development servers:"
echo -e "1. Backend: ${YELLOW}cd backend && python -m uvicorn main:app --reload${NC}"
echo -e "2. Frontend: ${YELLOW}cd frontend && npm start${NC}"
echo -e "\nTo access the application:"
echo -e "- Frontend: ${YELLOW}http://localhost:3000${NC}"
echo -e "- Backend API: ${YELLOW}http://localhost:8000${NC}"
echo -e "- API Documentation: ${YELLOW}http://localhost:8000/docs${NC}"

# Remove error handling trap
trap - EXIT

exit 0
