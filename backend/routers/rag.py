from fastapi import APIRouter

router = APIRouter()

@router.post("/ingest")
def ingest_documents():
    return {"message": "Document ingestion triggered."}

@router.get("/status")
def get_rag_status():
    return {"status": "Ready", "indexed_docs": 0}
