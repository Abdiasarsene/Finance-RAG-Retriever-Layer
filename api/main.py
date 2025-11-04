# api/main.py
from fastapi import FastAPI
from routers.retrieval import router as retrieval_router

# Include router
app = FastAPI(title="Finance RAG Retrieval API")
app.include_router(retrieval_router)