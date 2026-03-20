#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Web Scraper & Summarizer - Startup Script${NC}\n"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env and add your API keys:${NC}"
    echo "  - NVIDIA_API_KEY"
    echo "  - BRAVE_SEARCH_API_KEY"
    echo ""
    exit 1
fi

# Start backend
echo -e "${GREEN}Starting backend...${NC}"
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing backend dependencies...${NC}"
pip install -q -r requirements.txt

# Start backend in background
echo -e "${GREEN}Backend starting on http://localhost:8000${NC}"
python main.py &
BACKEND_PID=$!

cd ..

# Start frontend
echo -e "${GREEN}Starting frontend...${NC}"
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing frontend dependencies...${NC}"
    npm install -q
fi

# Create .env.local if it doesn't exist
if [ ! -f ".env.local" ]; then
    cp .env.local.example .env.local
fi

echo -e "${GREEN}Frontend starting on http://localhost:3000${NC}"
npm run dev &
FRONTEND_PID=$!

cd ..

echo -e "\n${GREEN}✓ Both services started!${NC}"
echo -e "Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "Frontend: ${GREEN}http://localhost:3000${NC}"
echo -e "\nPress Ctrl+C to stop both services\n"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
