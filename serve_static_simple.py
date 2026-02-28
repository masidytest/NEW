"""
Unified server with SIMPLE AI (no PyTorch) - fast and lightweight
Use this for testing/debugging or if PyTorch is too slow
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
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

from simple_ai import SimpleAI

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Platform – Simple Mode",
    description="Fast lightweight AI without PyTorch",
    version="2.0.0-simple"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Per-user AI instances
user_ais: Dict[int, SimpleAI] = {}

def get_ai_for_user(user_id: int) -> SimpleAI:
    """Get or create AI instance for a user"""
    if user_id not in user_ais:
        user_ais[user_id] = SimpleAI()
    return user_ais[user_id]

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
    reasoning_passes: int = 1

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

# ============ Core Endpoints ============

@app.get("/api")
def root():
    return {
        "service": "AI Platform – Simple Mode (No PyTorch)",
        "version": "2.0.0-simple",
        "status": "operational",
        "mode": "simple-ai",
        "features": ["fast-responses", "pattern-matching", "memory"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(
    req: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Chat endpoint - simple AI (instant responses)"""
    try:
        ai = get_ai_for_user(current_user.id)
        reply = ai.respond(req.message)
        return ChatResponse(
            reply=reply,
            reasoning_passes=1
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/goals", response_model=GoalOut)
async def create_goal(
    req: GoalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a goal"""
    try:
        goal = Goal(
            description=req.description,
            priority=req.priority,
            owner_id=current_user.id,
        )
        db.add(goal)
        db.commit()
        db.refresh(goal)
        
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

@app.get("/capabilities")
def list_capabilities():
    """List capabilities"""
    return [
        {
            "name": "chat",
            "description": "Simple pattern-based chat",
            "tags": ["conversation", "fast"]
        },
        {
            "name": "memory",
            "description": "Remember conversation history",
            "tags": ["memory", "context"]
        }
    ]

@app.get("/health")
async def health_check(current_user: User = Depends(get_current_user)):
    """Health check endpoint"""
    ai = get_ai_for_user(current_user.id)
    return {
        "status": "healthy",
        "user_id": current_user.id,
        "user_email": current_user.email,
        "mode": "simple-ai",
        "memory_items": len(ai.get_memory())
    }

# ============ Static File Serving ============

@app.get("/")
async def serve_root():
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

app.mount("/static", StaticFiles(directory="web"), name="static")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
