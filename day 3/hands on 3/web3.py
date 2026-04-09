"""
Human-in-the-Loop Content Moderation System

This application uses LangGraph for workflow management and FastAPI for the web interface.
It moderates content automatically and routes flagged items to human approval.

Workflow:
1. User submits content via /submit
2. Auto-moderation checks for toxicity using Groq API
3. If safe: auto-approve and return
4. If flagged: add to human queue, interrupt workflow
5. Human reviews via /flagged and decides via /decide/{id}
6. Resume workflow and return final status
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Optional
from groq import Groq
import uuid
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# State definition
class ModerationState(TypedDict):
    content: str
    status: str  # 'pending', 'safe', 'flagged', 'approved', 'rejected'
    decision: Optional[str]  # 'approve' or 'reject'
    id: str

# Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# Nodes
def moderate_content(state: ModerationState) -> ModerationState:
    """Classify content as safe or flagged using Groq API."""
    content = state['content']
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"Classify this content as 'safe' or 'flagged' if it contains toxic, harmful, or inappropriate material. Respond with only 'safe' or 'flagged': {content}"
        }],
        max_tokens=10
    )
    classification = response.choices[0].message.content.strip().lower()
    state['status'] = classification if classification in ['safe', 'flagged'] else 'flagged'  # default to flagged if unclear
    return state

def auto_approve(state: ModerationState) -> ModerationState:
    """Auto-approve safe content."""
    state['status'] = 'approved'
    return state

def human_queue(state: ModerationState) -> ModerationState:
    """Placeholder for human queue - workflow interrupts here."""
    return state

def human_decide(state: ModerationState) -> ModerationState:
    """Apply human decision."""
    if state.get('decision') == 'approve':
        state['status'] = 'approved'
    else:
        state['status'] = 'rejected'
    return state

# Build graph
graph = StateGraph(ModerationState)
graph.add_node("moderate", moderate_content)
graph.add_node("auto_approve", auto_approve)
graph.add_node("human_queue", human_queue)
graph.add_node("human_decide", human_decide)

graph.add_edge(START, "moderate")
graph.add_conditional_edges(
    "moderate",
    lambda s: s['status'],
    {"safe": "auto_approve", "flagged": "human_queue"}
)
graph.add_edge("auto_approve", END)
graph.add_edge("human_queue", "human_decide")
graph.add_edge("human_decide", END)

# Compile with checkpointer and interrupt
checkpointer = MemorySaver()
app_graph = graph.compile(checkpointer=checkpointer, interrupt_before=["human_decide"])

# FastAPI app
app = FastAPI(title="Content Moderation System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
flagged_queue = {}  # id: {'thread_id': str, 'content': str, 'status': str}

class SubmitRequest(BaseModel):
    content: str

class DecideRequest(BaseModel):
    decision: str  # 'approve' or 'reject'

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return FileResponse("templates/index.html", media_type="text/html")

@app.get("/review", response_class=HTMLResponse)
async def review_page(request: Request):
    return FileResponse("templates/review.html", media_type="text/html")

@app.post("/submit")
async def submit_content(request: SubmitRequest):
    """Submit content for moderation."""
    content = request.content
    id = str(uuid.uuid4())
    initial_state = ModerationState(
        content=content,
        status='pending',
        decision=None,
        id=id
    )
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    try:
        result = app_graph.invoke(initial_state, config)
        if result['status'] == 'approved':
            return {"status": "approved", "content": content, "id": id}
        else:
            # Interrupted, add to queue
            flagged_queue[id] = {
                'thread_id': thread_id,
                'content': content,
                'status': 'flagged'
            }
            return {"status": "flagged", "id": id, "message": "Content flagged for human review"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/flagged")
async def get_flagged():
    """Get list of flagged content for human review."""
    return [{"id": k, **v} for k, v in flagged_queue.items()]

@app.get("/status")
async def get_status():
    """Get overall system status and data."""
    return {
        "flagged_count": len(flagged_queue),
        "flagged_items": list(flagged_queue.values()),
        "server_status": "running"
    }

@app.post("/decide/{item_id}")
async def decide_content(item_id: str, request: DecideRequest):
    """Human decision on flagged content."""
    if item_id not in flagged_queue:
        return {"error": "Item not found in flagged queue"}

    thread_id = flagged_queue[item_id]['thread_id']
    config = {"configurable": {"thread_id": thread_id}}

    # Update state with decision
    app_graph.update_state(config, {"decision": request.decision})

    # Resume workflow
    try:
        result = app_graph.invoke(None, config)
        del flagged_queue[item_id]
        return {
            "status": result['status'],
            "content": result['content'],
            "id": item_id
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)