"""
CogOS Web UI Backend
FastAPI server for CogOS web interface
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
from datetime import datetime
import uuid

# Import CogOS
import sys
sys.path.insert(0, '/home/corbybender/Projects/cog')
from cog.cogos import CogOS

app = FastAPI(title="CogOS Web UI", version="1.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
active_connections: Dict[str, WebSocket] = {}
tasks: Dict[str, Dict] = {}
analytics: Dict[str, Any] = {
    "tasks_completed": 0,
    "tokens_used": 0,
    "agents_used": [],
    "modules_used": [],
    "performance_metrics": []
}

# Pydantic models
class TaskRequest(BaseModel):
    task: str
    modules: Optional[List[str]] = None
    safety_level: Optional[str] = "STANDARD"
    user_id: Optional[str] = None

class AgentConfig(BaseModel):
    name: str
    role: str
    prompt_template: str
    tools: List[str]
    temperature: Optional[float] = 0.7
    max_iterations: Optional[int] = 3

class CustomAgent(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    agents: List[AgentConfig]
    workflow: Dict[str, Any]

# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "CogOS Web UI",
        "version": "1.1.0",
        "status": "operational"
    }

@app.get("/api/health")
async def health():
    """Health check."""
    return {"status": "healthy"}

@app.post("/api/task")
async def create_task(request: TaskRequest):
    """Create and execute a task."""
    task_id = str(uuid.uuid4())

    # Initialize CogOS
    cogos = CogOS()

    # Store task
    tasks[task_id] = {
        "id": task_id,
        "task": request.task,
        "modules": request.modules or [],
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None,
        "user_id": request.user_id
    }

    # Execute task asynchronously
    asyncio.create_task(execute_task(task_id, cogos, request))

    return {"task_id": task_id, "status": "pending"}

async def execute_task(task_id: str, cogos: CogOS, request: TaskRequest):
    """Execute task in background."""
    try:
        tasks[task_id]["status"] = "running"

        # Execute task
        result = cogos.think(
            request.task,
            modules=request.modules,
            safety_level=request.safety_level
        )

        # Store result
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = {
            "summary": result.summary,
            "code": result.code,
            "metadata": result.metadata if hasattr(result, 'metadata') else {}
        }

        # Update analytics
        analytics["tasks_completed"] += 1
        if hasattr(result, 'metadata'):
            analytics["tokens_used"] += result.metadata.get('tokens_used', 0)
            analytics["agents_used"].extend(result.metadata.get('agents_used', []))
            analytics["modules_used"].extend(request.modules or [])

        # Notify connected clients
        await broadcast_task_update(task_id, tasks[task_id])

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        await broadcast_task_update(task_id, tasks[task_id])

@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    """Get task status and result."""
    return tasks.get(task_id, {"error": "Task not found"})

@app.get("/api/tasks")
async def list_tasks():
    """List all tasks."""
    return {"tasks": list(tasks.values())}

@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    if task_id in tasks:
        del tasks[task_id]
        return {"status": "deleted"}
    return {"error": "Task not found"}

@app.post("/api/agent")
async def create_custom_agent(agent: CustomAgent):
    """Create a custom agent."""
    agent_id = agent.id or str(uuid.uuid4())

    # Store custom agent
    # In a real implementation, this would be saved to a database
    return {
        "agent_id": agent_id,
        "status": "created",
        "agent": agent.dict()
    }

@app.get("/api/agent/{agent_id}")
async def get_agent(agent_id: str):
    """Get custom agent."""
    # In a real implementation, this would query a database
    return {"agent_id": agent_id, "status": "not_implemented"}

@app.get("/api/analytics")
async def get_analytics():
    """Get performance analytics."""
    return analytics

@app.get("/api/modules")
async def list_modules():
    """List available modules."""
    cogos = CogOS()
    modules = cogos.list_modules()

    return {
        "modules": [
            {
                "name": m.name,
                "description": m.description,
                "category": m.category,
                "tools": m.tool_count,
                "prompts": m.prompt_count
            }
            for m in modules
        ]
    }

@app.get("/api/performance")
async def get_performance():
    """Get performance metrics."""
    # Calculate performance metrics
    if analytics["tasks_completed"] > 0:
        avg_tokens = analytics["tokens_used"] / analytics["tasks_completed"]
    else:
        avg_tokens = 0

    # Agent usage
    agent_counts = {}
    for agent in analytics["agents_used"]:
        agent_counts[agent] = agent_counts.get(agent, 0) + 1

    # Module usage
    module_counts = {}
    for module in analytics["modules_used"]:
        module_counts[module] = module_counts.get(module, 0) + 1

    return {
        "tasks_completed": analytics["tasks_completed"],
        "tokens_used": analytics["tokens_used"],
        "average_tokens_per_task": avg_tokens,
        "agent_usage": agent_counts,
        "module_usage": module_counts,
        "performance_over_time": analytics["performance_metrics"]
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections[client_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            # Handle different message types
            if message["type"] == "subscribe_task":
                # Subscribe to task updates
                task_id = message["task_id"]
                if task_id in tasks:
                    await websocket.send_json({
                        "type": "task_update",
                        "task_id": task_id,
                        "data": tasks[task_id]
                    })

            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        del active_connections[client_id]

async def broadcast_task_update(task_id: str, task_data: Dict):
    """Broadcast task update to all connected clients."""
    if active_connections:
        message = {
            "type": "task_update",
            "task_id": task_id,
            "data": task_data
        }

        # Send to all connected clients
        for connection in active_connections.values():
            try:
                await connection.send_json(message)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
