# Dockerfile
# Production-ready Docker image for AI Platform (Railway - All-in-One)

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create plugins directory if it doesn't exist
RUN mkdir -p plugins

# Railway provides PORT environment variable
ENV PORT=8000
EXPOSE $PORT

# Run the unified server (API + Static UI)
CMD uvicorn serve_static:app --host 0.0.0.0 --port $PORT
