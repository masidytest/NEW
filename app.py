# app.py
# FastAPI backend exposing the autonomous cognitive system as a public service

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import torch

from next_system import Agent, train_core_on_text

app = FastAPI(
    title="General AI Platform",
    description="Self-expanding autonomous cognitive system with public API",
    version="1.0.0"
)

# CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
device = "cuda" if torch.cuda.is_available() else "cpu"
agent = Agent(device=device)

# Quick training on startup
demo_texts = [
    "hello, this is a new brain.",
    "this system has memory and planning.",
    "the goal is to become more advanced over time.",
    "it can remember previous goals and answers.",
]
print("Initializing cognitive system...")
train_core_on_text(agent, demo_texts, epochs=5, max_len=80, lr=1e-3)
print("System ready.")

# ============ Request/Response Models ============

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    reasoning_passes: int = 3

class GoalRequest(BaseModel):
    user_id: str
    description: str
    priority: float = 1.0
    tags: Optional[List[str]] = None

class GoalResponse(BaseModel):
    goal_id: str
    description: str
    priority: float

class GoalInfo(BaseModel):
    goal_id: str
    description: str
    status: str
    priority: float
    score: float
    created_at: float
    progress_notes: List[str]

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

class AutonomousCycleResponse(BaseModel):
    goal_id: Optional[str]
    goal_description: Optional[str]
    answer: str
    status: str

# ============ Endpoints ============

@app.get("/")
def root():
    return {
        "service": "General AI Platform",
        "version": "1.0.0",
        "status": "operational",
        "capabilities": len(agent.capabilities.all()),
        "endpoints": {
            "chat": "POST /chat",
            "goals": "POST /goals, GET /goals",
            "autonomous": "POST /autonomous",
            "capabilities": "GET /capabilities",
            "gaps": "GET /gaps",
            "plugins": "GET /plugins"
        }
    }

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Main chat endpoint - runs full cognitive loop
    """
    try:
        # TODO: Route by user_id to per-user agent instance
        reply = agent.engine.run(req.message)
        return ChatResponse(
            reply=reply,
            reasoning_passes=agent.engine.passes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/goals", response_model=GoalResponse)
def add_goal(req: GoalRequest):
    """
    Add a long-term goal to the autonomous system
    """
    try:
        goal_id = agent.add_long_term_goal(
            req.description,
            priority=req.priority,
            tags=req.tags or []
        )
        return GoalResponse(
            goal_id=goal_id,
            description=req.description,
            priority=req.priority
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal creation error: {str(e)}")

@app.get("/goals", response_model=List[GoalInfo])
def list_goals(status: Optional[str] = None):
    """
    List all long-term goals, optionally filtered by status
    """
    try:
        from next_system import GoalStatus
        
        status_filter = None
        if status:
            try:
                status_filter = GoalStatus[status.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")
        
        goals = agent.list_long_term_goals()
        if status_filter:
            goals = [g for g in goals if g.status == status_filter]
        
        return [
            GoalInfo(
                goal_id=g.id,
                description=g.description,
                status=g.status.name,
                priority=g.priority,
                score=g.score,
                created_at=g.created_at,
                progress_notes=g.progress_notes
            )
            for g in goals
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Goal listing error: {str(e)}")

@app.post("/autonomous", response_model=AutonomousCycleResponse)
def run_autonomous_cycle():
    """
    Run one autonomous cycle on long-term goals
    """
    try:
        goal, answer = agent.run_autonomous_cycle()
        
        if goal is None:
            return AutonomousCycleResponse(
                goal_id=None,
                goal_description=None,
                answer=answer,
                status="no_active_goals"
            )
        
        return AutonomousCycleResponse(
            goal_id=goal.id,
            goal_description=goal.description,
            answer=answer,
            status="completed"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autonomous cycle error: {str(e)}")

@app.get("/capabilities", response_model=List[CapabilityInfo])
def list_capabilities():
    """
    List all registered capabilities
    """
    try:
        caps = agent.capabilities.all()
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
def get_capability_gaps():
    """
    Get detected capability gaps
    """
    try:
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
def get_plugin_proposals():
    """
    Get proposed plugin specifications for missing capabilities
    """
    try:
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
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "device": str(agent.device),
        "capabilities": len(agent.capabilities.all()),
        "memory_items": len(agent.memory.items),
        "goals": len(agent.list_long_term_goals())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
