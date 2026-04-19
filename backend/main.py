from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, schemes, chat, rag, agents, admin
from database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GovScheme AI API",
    description="API for AI-Powered Government Scheme Recommendation Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(schemes.router, prefix="/schemes", tags=["Schemes"])
app.include_router(chat.router, prefix="/chat", tags=["Chat & AI"])
app.include_router(rag.router, prefix="/rag", tags=["RAG Processing"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "service": "GovScheme AI"}

@app.get("/metrics", tags=["System"])
async def get_metrics():
    # Placeholder for monitoring metrics
    return {"active_users": 0, "api_calls_today": 0}
