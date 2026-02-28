#!/bin/bash
# Startup script for Railway deployment

# Use Railway's PORT or default to 8000
PORT=${PORT:-8000}

echo "Starting server on port $PORT"

# Use simple AI version (no PyTorch) for faster responses
# Change to serve_static:app to use full PyTorch version
uvicorn serve_static_simple:app --host 0.0.0.0 --port $PORT
