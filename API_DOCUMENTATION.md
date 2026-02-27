# General AI Platform - API Documentation

## Overview

A public HTTP API exposing a self-expanding autonomous cognitive system with memory, planning, reasoning, and continuous learning capabilities.

**Base URL**: `http://localhost:8000`

**Interactive Docs**: `http://localhost:8000/docs`

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python app.py

# Test API
python test_api.py
```

## Endpoints

### 1. Service Information

#### `GET /`
Get service information and available endpoints.

**Response**:
```json
{
  "service": "General AI Platform",
  "version": "1.0.0",
  "status": "operational",
  "capabilities": 7,
  "endpoints": {
    "chat": "POST /chat",
    "goals": "POST /goals, GET /goals",
    "autonomous": "POST /autonomous",
    "capabilities": "GET /capabilities",
    "gaps": "GET /gaps",
    "plugins": "GET /plugins"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "device": "cpu",
  "capabilities": 7,
  "memory_items": 0,
  "goals": 0
}
```

---

### 2. Chat Interface

#### `POST /chat`
Main chat endpoint - runs full cognitive loop with multi-pass reasoning.

**Request**:
```json
{
  "user_id": "user123",
  "message": "what is 5 + 3"
}
```

**Response**:
```json
{
  "reply": "The answer is 8",
  "reasoning_passes": 3
}
```

**Features**:
- Full cognitive loop (encode → memory → plan → reason → evaluate → learn)
- Multi-pass reasoning (3 cycles by default)
- Automatic capability selection
- Memory integration
- Continuous learning

**Example**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "message": "what time is it"}'
```

---

### 3. Goals Management

#### `POST /goals`
Add a long-term goal to the autonomous system.

**Request**:
```json
{
  "user_id": "user123",
  "description": "Learn about quantum computing",
  "priority": 2.5,
  "tags": ["learning", "quantum"]
}
```

**Response**:
```json
{
  "goal_id": "goal-1234567890",
  "description": "Learn about quantum computing",
  "priority": 2.5
}
```

#### `GET /goals`
List all long-term goals.

**Query Parameters**:
- `status` (optional): Filter by status (PENDING, IN_PROGRESS, DONE, PAUSED, FAILED)

**Response**:
```json
[
  {
    "goal_id": "goal-1234567890",
    "description": "Learn about quantum computing",
    "status": "PENDING",
    "priority": 2.5,
    "score": 2.5,
    "created_at": 1234567890.0,
    "progress_notes": []
  }
]
```

**Example**:
```bash
# Add goal
curl -X POST "http://localhost:8000/goals" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "description": "Master machine learning",
    "priority": 3.0,
    "tags": ["learning", "ml"]
  }'

# List all goals
curl "http://localhost:8000/goals"

# List pending goals only
curl "http://localhost:8000/goals?status=PENDING"
```

---

### 4. Autonomous Execution

#### `POST /autonomous`
Run one autonomous cycle on the highest-priority goal.

**Response**:
```json
{
  "goal_id": "goal-1234567890",
  "goal_description": "Learn about quantum computing",
  "answer": "Quantum computing uses quantum mechanics...",
  "status": "completed"
}
```

**Status Values**:
- `completed`: Successfully executed a goal
- `no_active_goals`: No pending or in-progress goals

**Example**:
```bash
curl -X POST "http://localhost:8000/autonomous"
```

---

### 5. Capability System

#### `GET /capabilities`
List all registered capabilities.

**Response**:
```json
[
  {
    "name": "calc",
    "description": "Basic calculator for arithmetic operations",
    "tags": ["math", "utility"],
    "input_schema": {"expression": "str"},
    "output_schema": {"result": "float"}
  }
]
```

**Example**:
```bash
curl "http://localhost:8000/capabilities"
```

#### `GET /gaps`
Get detected capability gaps (missing capabilities that users requested).

**Response**:
```json
[
  {
    "missing_tags": ["image"],
    "count": 2
  },
  {
    "missing_tags": ["speech"],
    "count": 1
  }
]
```

**Example**:
```bash
curl "http://localhost:8000/gaps"
```

#### `GET /plugins`
Get proposed plugin specifications for missing capabilities.

**Response**:
```json
[
  {
    "name": "plugin_for_image",
    "tags": ["image"],
    "description": "Capability to handle tasks requiring tags ['image']",
    "count": 2
  }
]
```

**Example**:
```bash
curl "http://localhost:8000/plugins"
```

---

## Current Capabilities

The system currently has 7 registered capabilities:

| Capability | Tags | Description |
|------------|------|-------------|
| calc | math, utility | Basic calculator |
| now | time, utility | Current date/time |
| fetch_ai_papers | web, research, papers | Fetch AI papers |
| summarize_papers | nlp, summarization, research | Summarize papers |
| list_code_files | code, files, repo | List code files |
| read_file | code, files | Read file contents |
| analyze_code_snippet | code, analysis | Code analysis |

---

## Self-Expanding System

The system automatically:

1. **Detects capability gaps** when users request features it doesn't have
2. **Logs demand** for missing capabilities
3. **Proposes plugin specifications** for the most-requested gaps
4. **Prioritizes** by actual usage patterns

### Example Flow

```bash
# User requests image generation (not available)
curl -X POST "http://localhost:8000/chat" \
  -d '{"user_id": "user123", "message": "generate an image of a cat"}'

# System detects gap and logs it
curl "http://localhost:8000/gaps"
# → [{"missing_tags": ["image"], "count": 1}]

# System proposes plugin
curl "http://localhost:8000/plugins"
# → [{"name": "plugin_for_image", "tags": ["image"], ...}]
```

---

## Architecture

### Request Flow

```
Client Request
    ↓
FastAPI Endpoint
    ↓
Agent.engine.run()
    ↓
Cognitive Loop:
  1. Encode (neural embedding)
  2. Memory Query (retrieve relevant context)
  3. Plan (capability-aware planning)
  4. Reason (multi-pass reasoning)
  5. Evaluate (self-critique)
  6. Store (update memory)
  7. Learn (continuous learning)
    ↓
Response
```

### Components

- **Neural Core**: Bidirectional GRU + 4-head self-attention
- **Memory**: 3-tier hierarchical (short/mid/long-term)
- **Planner**: Meta-planner with pattern learning
- **Reasoner**: Multi-pass reasoning engine
- **Evaluator**: Self-critique and refinement
- **Learner**: Continuous learning with replay buffer
- **Capability Registry**: Tag-based capability management
- **Gap Analyzer**: Self-diagnosis and plugin proposals

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Internal server error

Error responses include details:
```json
{
  "detail": "Error description here"
}
```

---

## CORS Configuration

CORS is enabled for all origins by default (development mode).

For production, edit `app.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance

- **Device**: Auto-detects CUDA/CPU
- **Model Size**: ~2M parameters
- **Response Time**: 
  - Simple queries: ~1-2 seconds
  - Complex reasoning: ~3-5 seconds
- **Memory**: Hierarchical with automatic consolidation
- **Learning**: Continuous with gradient clipping and replay buffer

---

## Limitations (Current)

1. **Single agent instance**: All users share the same agent (Step 3 will add multi-user)
2. **No authentication**: Open API (add in production)
3. **No rate limiting**: Can be abused (add in production)
4. **No persistence**: Memory lost on restart (add database in future)
5. **Synchronous**: One request at a time (can add async processing)

---

## Next Steps

### Step 2: Web Chat UI
Build a minimal web interface that talks to this API.

### Step 3: Multi-User Support
- Per-user agent instances
- User authentication
- Isolated memory per user

### Step 4: Public Plugin System
- Plugin marketplace
- User-submitted capabilities
- Automatic plugin integration

### Step 5: Advanced Features
- Streaming responses
- WebSocket support
- Persistent storage
- Distributed deployment
- Advanced monitoring

---

## Testing

### Automated Tests
```bash
python test_api.py
```

### Interactive Testing
Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

### Manual Testing
```bash
# Health check
curl http://localhost:8000/health

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "hello"}'

# List capabilities
curl http://localhost:8000/capabilities
```

---

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export DEVICE=cuda  # or cpu
```

---

## Support

For issues, questions, or contributions, see the main README.md.

**Status**: ✅ Step 1 Complete - Public HTTP API operational
