#!/bin/bash

# Print startup message
echo "Starting RemoteJobBank application..."

# Change to backend directory
cd /app/backend

# Skip scraper due to architecture incompatibility
echo "⚠️ Skipping initial data scraping due to platform compatibility issues"
# python -c "from scraper.scraper import main; main()"

# Start the backend API - MODIFIED for better debugging
echo "Starting backend API server..."
echo "Current directory: $(pwd)"
echo "Contents of current directory:"
ls -la
echo "Starting uvicorn..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 &
sleep 3
echo "Backend status:"
ps aux | grep uvicorn

# Change to frontend directory and serve build files
cd /app/frontend
echo "Starting frontend server..."
npx serve -s build -l 3000 