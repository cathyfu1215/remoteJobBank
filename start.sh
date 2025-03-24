#!/bin/bash

# Print startup message
echo "Starting RemoteJobBank application..."

# Add the /app directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:/app

# Change to backend directory
cd /app/backend

# Run the scraper first
echo "Running initial data scraping..."
python -c "from scraper.scraper import scrape_jobs; scrape_jobs()"

# Start the backend API with Gunicorn in the background
echo "Starting backend API server..."
gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000 --daemon

# Change to frontend directory
cd /app/frontend

# Start the frontend server
echo "Starting frontend server..."
npx serve -s build -l 3000 