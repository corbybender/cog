"""CogOS Web UI Backend - FastAPI server"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
from datetime import datetime
import uuid
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from cog.kernel import Kernel, KernelConfig

VERSION = "0.1.0"

app = FastAPI(title="CogOS Web UI", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections: Dict[str, WebSocket] = {}
tasks: Dict[str, Dict] = {}
analytics: Dict[str, Any] = {
    "tasks_completed": 0,
    "tokens_used": 0,
    "agents_used": [],
    "modules_used": [],
    "performance_metrics": []
}


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


def _make_kernel() -> Kernel:
    config = KernelConfig(
        modules_path=os.path.join(os.path.dirname(__file__), "..", "..", "cog", "modules"),
        memory_backend="sqlite",
    )
    return Kernel(config)


@app.get("/")
async def root():
    return {"message": "CogOS Web UI", "version": VERSION, "status": "operational"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/task")
async def create_task(request: TaskRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "id": task_id,
        "task": request.task,
        "modules": request.modules or [],
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None,
        "user_id": request.user_id,
    }
    asyncio.create_task(_execute_task(task_id, request))
    return {"task_id": task_id, "status": "pending"}


async def _execute_task(task_id: str, request: TaskRequest):
    try:
        tasks[task_id]["status"] = "running"
        kernel = _make_kernel()
        result = kernel.run(request.task)
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = {
            "summary": result.get("output", ""),
            "metadata": {
                "iterations": result.get("iterations", 0),
                "tokens_used": result.get("total_tokens", 0),
            },
        }
        analytics["tasks_completed"] += 1
        analytics["tokens_used"] += result.get("total_tokens", 0)
        kernel.stop()
        await _broadcast_task_update(task_id, tasks[task_id])
    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        await _broadcast_task_update(task_id, tasks[task_id])


@app.get("/api/task/{task_id}")
async def get_task(task_id: str):
    return tasks.get(task_id, {"error": "Task not found"})


@app.get("/api/tasks")
async def list_tasks():
    return {"tasks": list(tasks.values())}


@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    if task_id in tasks:
        del tasks[task_id]
        return {"status": "deleted"}
    return {"error": "Task not found"}


@app.post("/api/agent")
async def create_custom_agent(agent: CustomAgent):
    agent_id = agent.id or str(uuid.uuid4())
    return {"agent_id": agent_id, "status": "created", "agent": agent.dict()}


@app.get("/api/agent/{agent_id}")
async def get_agent(agent_id: str):
    return {"agent_id": agent_id, "status": "not_implemented"}


@app.get("/api/analytics")
async def get_analytics():
    return analytics


@app.get("/api/modules")
async def list_modules():
    kernel = _make_kernel()
    kernel.start()
    discovered = kernel.modules.discover()
    modules_list = []
    for m in discovered:
        desc = m.manifest.description if m.manifest else ""
        modules_list.append({"name": m.name, "description": desc})
    kernel.stop()
    return {"modules": modules_list}


@app.get("/api/performance")
async def get_performance():
    avg_tokens = analytics["tokens_used"] / analytics["tasks_completed"] if analytics["tasks_completed"] > 0 else 0
    return {
        "tasks_completed": analytics["tasks_completed"],
        "tokens_used": analytics["tokens_used"],
        "average_tokens_per_task": avg_tokens,
    }


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message["type"] == "subscribe_task":
                task_id = message.get("task_id")
                if task_id and task_id in tasks:
                    await websocket.send_json({"type": "task_update", "task_id": task_id, "data": tasks[task_id]})
            elif message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        active_connections.pop(client_id, None)


async def _broadcast_task_update(task_id: str, task_data: Dict):
    if not active_connections:
        return
    msg = {"type": "task_update", "task_id": task_id, "data": task_data}
    for conn in list(active_connections.values()):
        try:
            await conn.send_json(msg)
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
