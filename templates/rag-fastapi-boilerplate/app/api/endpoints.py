from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.rag_service import rag_service

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@router.post("/query", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Endpoint to ask a question to the RAG system."""
    try:
        result = rag_service.query(request.question)
        return QueryResponse(answer=result["result"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest")
async def ingest_data(texts: list[str]):
    """Endpoint to ingest new documents into the system."""
    try:
        rag_service.initialize_db(texts)
        return {"message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
