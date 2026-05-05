#!/bin/bash

# Define colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Starting Hypertrophy Planner ===${NC}"

# 1. Define the cleanup function
cleanup() {
    echo -e "\n${RED}Shutting down servers...${NC}"
    # Kill the processes using their stored PIDs
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Cleanup complete. Goodbye!${NC}"
    exit 0
}

# 2. Trap SIGINT (Ctrl+C) and route it to the cleanup function
trap cleanup SIGINT

# 3. Start the Backend
echo -e "${BLUE}[1/2] Starting FastAPI Backend on port 5100...${NC}"
cd backend
uvicorn main:app --host 0.0.0.0 --port 5100 --reload &
BACKEND_PID=$! # Store the Process ID
cd ..

# 4. Start the Frontend
echo -e "${BLUE}[2/2] Starting Svelte Frontend...${NC}"
cd frontend
npm run dev &
FRONTEND_PID=$! # Store the Process ID
cd ..

echo -e "\n${GREEN}Servers are running!${NC}"
echo -e "➜ ${BLUE}Backend Docs:${NC} http://localhost:5100/docs"
echo -e "➜ ${BLUE}Frontend App:${NC} http://localhost:5173"
echo -e "Press ${RED}Ctrl+C${NC} to stop both servers."

# 5. Keep the script alive waiting for the background processes
wait
