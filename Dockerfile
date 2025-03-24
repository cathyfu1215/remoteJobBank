FROM node:16-alpine as frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

FROM python:3.8-slim

# Install Node.js for serving the frontend
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -sL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn gunicorn

# Copy frontend build from builder stage
COPY --from=frontend-builder /app/frontend/build /app/frontend/build
COPY frontend/package*.json /app/frontend/

# Copy backend code
COPY backend /app/backend

# Copy root files including .env
COPY .env ./
COPY start.sh ./
RUN chmod 755 start.sh

EXPOSE 8000 3000

# Run the start script
CMD ["/bin/bash", "./start.sh"] 