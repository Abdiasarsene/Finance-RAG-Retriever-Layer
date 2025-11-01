from fastapi import FastAPI
from routers.retrieval import router as retrieval_router

app = FastAPI(title="Finance RAG Retrieval API")

# Inclure le router
app.include_router(retrieval_router)