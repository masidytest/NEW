# Starting the API Server

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start the Server

### Option A: Using uvicorn directly
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Option B: Using Python
```bash
python app.py
```

## Step 3: Verify Server is Running

Open your browser and go to:
- **API Root**: http://localhost:8000/
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Step 4: Test the API

In a new terminal:
```bash
python test_api.py
```

## Available Endpoints

### Core Endpoints
- `GET /` - Service information
- `GET /health` - Health check
- `POST /chat` - Main chat interface (full cognitive loop)

### Goals Management
- `POST /goals` - Add a long-term goal
- `GET /goals` - List all goals (optional: ?status=PENDING)
- `POST /autonomous` - Run one autonomous cycle

### Capability System
- `GET /capabilities` - List all registered capabilities
- `GET /gaps` - Get detected capability gaps
- `GET /plugins` - Get proposed plugin specifications

## Example API Calls

### Chat
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "what is 5 + 3"}'
```

### Add Goal
```bash
curl -X POST "http://localhost:8000/goals" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "description": "Learn about quantum computing",
    "priority": 2.5,
    "tags": ["learning", "quantum"]
  }'
```

### List Capabilities
```bash
curl "http://localhost:8000/capabilities"
```

### Get Capability Gaps
```bash
curl "http://localhost:8000/gaps"
```

## Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

## Server Configuration

Default settings:
- Host: 0.0.0.0 (accessible from network)
- Port: 8000
- CORS: Enabled for all origins (change in production)
- Device: Auto-detect (CUDA if available, else CPU)

## Production Deployment

For production, consider:

1. **Use a production ASGI server**:
   ```bash
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Configure CORS properly**:
   Edit `app.py` and set specific origins instead of `["*"]`

3. **Add authentication**:
   Implement API keys or OAuth2

4. **Use environment variables**:
   For configuration (port, host, etc.)

5. **Add rate limiting**:
   Prevent abuse

6. **Set up monitoring**:
   Log requests, errors, performance metrics

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
uvicorn app:app --port 8001
```

### Import errors
```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Verify next_system.py is in the same directory
ls next_system.py
```

### CUDA/GPU issues
The system will automatically fall back to CPU if CUDA is not available.

## Next Steps

Once the server is running:
1. Test with `python test_api.py`
2. Explore the interactive docs at http://localhost:8000/docs
3. Build a frontend (Step 2)
4. Add multi-user support (Step 3)
5. Implement public plugin system (Step 4)
