from fastapi import FastAPI
from src.routers.query_router import route_query

app = FastAPI(title="Finance RAG Retrieval API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/retrieve")
def retrieve(query: str):
    route_result = route_query(query)
    return {"router_output": route_result}