"""
Unified server that serves both API and static web UI
This allows deploying everything to a single Railway service
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, List, Any
import torch
import os

from sqlalchemy.orm import Session

from db import Base, engine, get_db
from models import User, Goal
from auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)

from next_system import Agent, train_core_on_text

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="General AI Platform – Multi-User",
    description="Self-expanding autonomous cognitive system with multi-user support",
    version="2.0.0"
)

# CORS for web clients (allow same origin since we're serving frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Same origin, so this is safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Per-user agent cache
user_agents: Dict[int, Agent] = {}

def get_agent_for_user(user_id: int) -> Agent:
    """Get or create agent instance for a user"""
    if user_id not in user_agents:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        agent = Agent(device=device)
        
        # Quick training for new agent
        demo_texts = [
            "hello, this is a new brain.",
            "this system has memory and planning.",
            "the goal is to become more advanced over time.",
        ]
        train_core_on_text(agent, demo_texts, epochs=3, max_len=80, lr=1e-3)
        
        user_agents[user_id] = agent
    
    return user_agents[user_id]

# ============ Request/Response Models ============

class RegisterRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_email: str

class UserInfo(BaseModel):
    id: int
    email: str
    created_at: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str
    reasoning_passes: int = 3

class GoalCreate(BaseModel):
    description: str
    priority: float = 1.0

class GoalOut(BaseModel):
    id: int
    description: str
    priority: float
    is_active: bool
    created_at: str
    
    model_config = {"from_attributes": True}

class CapabilityInfo(BaseModel):
    name: str
    description: str
    tags: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]

class CapabilityGap(BaseModel):
    missing_tags: List[str]
    count: int

class PluginSpec(BaseModel):
    name: str
    tags: List[str]
    description: str
    count: int

# ============ Auth Endpoints ============

@app.post("/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=req.email,
        hashed_password=get_password_hash(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=access_token,
        user_email=user.email
    )

@app.post("/auth/token", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Login with email and password"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=access_token,
        user_email=user.email
    )

@app.get("/auth/me", response_model=UserInfo)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return UserInfo(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at.isoformat()
    )

# ============ Core Endpoints (Per-User) ============

@app.get("/api")
def root():
    return {
        "service": "General AI Platform – Multi-User",
        "version": "2.0.0",
        "status": "operational",
        "features": ["multi-user", "authentication", "per-user-memory", "static-ui"],
        "endpoints": {
            "auth": "POST /auth/register, POST /auth/token, GET /auth/me",
            "chat": "POST /chat (requires auth)",
            "goals": "POST /goals, GET /goals (requires auth)",
            "capabilities": "GET /capabilities",
            "gaps": "GET /gaps (requires auth)",
            "plugins": "GET /plugins (requires auth)",
            "ui": "GET / (static web interface)"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Chat endpoint - per-user agent instance"""
    try:
        agent = get_agent_for_user(current_user.id)
        reply = agent.engine.run(req.message)
        return ChatResponse(
            reply=reply,
            reasoning_passes=agent.engine.passes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/goals", response_model=GoalOut)
async def create_goal(
    req: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a goal - stored in DB and user's agent"""
    try:
        # Store in database
        goal = Goal(
            description=req.description,
            priority=req.priority,
            owner_id=current_user.id,
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        
        # Also register in user's agent
        agent = get_agent_for_user(current_user.id)
        agent.add_long_term_goal(req.description, priority=req.priority, tags=[])
        
        return GoalOut(
            id=goal.id,
            description=goal.description,
            priority=goal.priority,
            is_active=goal.is_active,
            created_at=goal.created_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal creation error: {str(e)}")

@app.get("/goals", response_model=List[GoalOut])
async def list_goals(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List user's goals"""
    try:
        goals = (
            db.query(Goal)
            .filter(Goal.owner_id == current_user.id)
            .order_by(Goal.created_at.desc())
            .all()
        )
        return [
            GoalOut(
                id=g.id,
                description=g.description,
                priority=g.priority,
                is_active=g.is_active,
                created_at=g.created_at.isoformat()
            )
            for g in goals
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal listing error: {str(e)}")

@app.get("/capabilities", response_model=List[CapabilityInfo])
def list_capabilities():
    """List all registered capabilities (public endpoint)"""
    try:
        # Use a temporary agent to get capabilities
        device = "cuda" if torch.cuda.is_available() else "cpu"
        temp_agent = Agent(device=device)
        caps = temp_agent.capabilities.all()
        return [
            CapabilityInfo(
                name=cap.name,
                description=cap.description,
                tags=cap.tags,
                input_schema=cap.input_schema,
                output_schema=cap.output_schema
            )
            for cap in caps
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Capability listing error: {str(e)}")

@app.get("/gaps", response_model=List[CapabilityGap])
async def get_capability_gaps(current_user: User = Depends(get_current_user)):
    """Get detected capability gaps for current user"""
    try:
        agent = get_agent_for_user(current_user.id)
        gaps = agent.get_capability_gaps()
        return [
            CapabilityGap(
                missing_tags=gap["missing_tags"],
                count=gap["count"]
            )
            for gap in gaps
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap analysis error: {str(e)}")

@app.get("/plugins", response_model=List[PluginSpec])
async def get_plugin_proposals(current_user: User = Depends(get_current_user)):
    """Get proposed plugin specifications for current user"""
    try:
        agent = get_agent_for_user(current_user.id)
        specs = agent.propose_new_plugins()
        return [
            PluginSpec(
                name=spec["name"],
                tags=spec["tags"],
                description=spec["description"],
                count=spec["count"]
            )
            for spec in specs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plugin proposal error: {str(e)}")

@app.get("/health")
async def health_check(current_user: User = Depends(get_current_user)):
    """Health check endpoint (per-user stats)"""
    try:
        agent = get_agent_for_user(current_user.id)
        return {
            "status": "healthy",
            "user_id": current_user.id,
            "user_email": current_user.email,
            "device": str(agent.device),
            "capabilities": len(agent.capabilities.all()),
            "memory_items": len(agent.memory.items),
            "goals": len(agent.list_long_term_goals())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")

# ============ Static File Serving ============

# Mount static files (CSS, JS, images if any)
app.mount("/static", StaticFiles(directory="web"), name="static")

# Serve HTML pages
@app.get("/")
async def serve_index():
    return FileResponse("web/login.html")

@app.get("/login.html")
async def serve_login():
    return FileResponse("web/login.html")

@app.get("/index.html")
async def serve_dashboard():
    return FileResponse("web/index.html")

@app.get("/chat.html")
async def serve_chat():
    return FileResponse("web/chat.html")

@app.get("/goals.html")
async def serve_goals():
    return FileResponse("web/goals.html")

@app.get("/capabilities.html")
async def serve_capabilities():
    return FileResponse("web/capabilities.html")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
