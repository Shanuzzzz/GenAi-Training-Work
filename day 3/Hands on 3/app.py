from datetime import datetime
from enum import Enum
from typing import Callable, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Moderation Workflow")
templates = Jinja2Templates(directory="templates")

FLAG_WORDS = {"spam", "attack", "hate", "illegal", "scam", "bomb", "drugs", "terror"}

pending_items: Dict[str, "TaskData"] = {}
history: Dict[str, "TaskData"] = {}


class TaskStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class TaskData(BaseModel):
    id: str
    content: str
    status: TaskStatus
    decision: str
    created_at: datetime


class DecisionPayload(BaseModel):
    decision: str


class WorkflowNode:
    def __init__(self, name: str, handler: Callable[[dict], dict]):
        self.name = name
        self.handler = handler


class ConditionalEdge:
    def __init__(self, source: str, target: str, predicate: Callable[[dict], bool]):
        self.source = source
        self.target = target
        self.predicate = predicate


class Workflow:
    def __init__(self, nodes: List[WorkflowNode], edges: List[ConditionalEdge]):
        self.nodes = {node.name: node for node in nodes}
        self.edges = edges

    def run(self, state: dict) -> dict:
        current = "input"
        while current:
            node = self.nodes[current]
            state = node.handler(state)
            next_edge = next(
                (edge for edge in self.edges if edge.source == current and edge.predicate(state)),
                None,
            )
            current = next_edge.target if next_edge else None
        return state


def classify_content(text: str) -> str:
    lower = text.lower()
    for token in FLAG_WORDS:
        if token in lower:
            return "flagged"
    return "safe"


def input_node(state: dict) -> dict:
    state["status"] = "received"
    return state


def moderation_node(state: dict) -> dict:
    state["decision"] = classify_content(state["content"])
    state["status"] = state["decision"]
    return state


def router_node(state: dict) -> dict:
    return state


def approval_handler_node(state: dict) -> dict:
    state["status"] = "pending"
    return state


def final_node(state: dict) -> dict:
    return state


workflow = Workflow(
    nodes=[
        WorkflowNode("input", input_node),
        WorkflowNode("moderation", moderation_node),
        WorkflowNode("route", router_node),
        WorkflowNode("approval", approval_handler_node),
        WorkflowNode("done", final_node),
    ],
    edges=[
        ConditionalEdge("input", "moderation", lambda s: True),
        ConditionalEdge("moderation", "route", lambda s: True),
        ConditionalEdge("route", "approval", lambda s: s["status"] == "flagged"),
        ConditionalEdge("route", "done", lambda s: s["status"] == "safe"),
        ConditionalEdge("approval", "done", lambda s: True),
    ],
)


def create_task(content: str) -> TaskData:
    task_id = str(uuid4())
    state = {"id": task_id, "content": content.strip(), "status": None, "decision": None}
    outcome = workflow.run(state)
    if outcome["status"] == "safe":
        task = TaskData(
            id=task_id,
            content=content,
            status=TaskStatus.approved,
            decision="auto-approved",
            created_at=datetime.utcnow(),
        )
    else:
        task = TaskData(
            id=task_id,
            content=content,
            status=TaskStatus.pending,
            decision="flagged",
            created_at=datetime.utcnow(),
        )
        pending_items[task_id] = task
    history[task_id] = task
    return task


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
def submit(request: Request, content: str = Form(...)):
    if not content.strip():
        raise HTTPException(status_code=400, detail="Content is required")
    task = create_task(content)
    return templates.TemplateResponse(
        "status.html",
        {"request": request, "task": task},
    )


@app.get("/status/{task_id}", response_class=HTMLResponse)
def status_page(request: Request, task_id: str):
    task = history.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse("status.html", {"request": request, "task": task})


@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    pending = list(pending_items.values())
    return templates.TemplateResponse("admin.html", {"request": request, "pending": pending})


@app.post("/admin/{task_id}/decision", response_class=HTMLResponse)
def review_task(request: Request, task_id: str, decision: str = Form(...)):
    task = pending_items.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Pending task not found")
    if decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be approve or reject")
    task.status = TaskStatus.approved if decision == "approve" else TaskStatus.rejected
    task.decision = "human-approved" if decision == "approve" else "human-rejected"
    pending_items.pop(task_id, None)
    history[task_id] = task
    return RedirectResponse(f"/status/{task_id}", status_code=303)


@app.get("/api/pending")
def api_pending():
    return [task.dict() for task in pending_items.values()]


@app.get("/api/task/{task_id}")
def api_task_status(task_id: str):
    task = history.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.dict()


@app.post("/api/admin/{task_id}/decision")
def api_review_task(task_id: str, payload: DecisionPayload):
    task = pending_items.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Pending task not found")
    if payload.decision not in {"approve", "reject"}:
        raise HTTPException(status_code=400, detail="Decision must be approve or reject")
    task.status = TaskStatus.approved if payload.decision == "approve" else TaskStatus.rejected
    task.decision = "human-approved" if payload.decision == "approve" else "human-rejected"
    pending_items.pop(task_id, None)
    history[task_id] = task
    return task.dict()
