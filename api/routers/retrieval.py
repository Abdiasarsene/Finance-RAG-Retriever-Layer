# api/routers/retrieval.py
from fastapi import APIRouter, Depends, HTTPException
from src.routers.query_router import route_query
from core.secure import verify_api_key
from core.monitoring import REQUEST_COUNT, REQUEST_LATENCY
import time

# ====== API ROUTER ======
router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/retrieve")
def retrieve(query: str, api_key: str = Depends(verify_api_key)):
    start = time.time()
    REQUEST_COUNT.labels(endpoint="/retrieve").inc()
    route_result = route_query(query)
    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint="/retrieve").observe(latency)
    return {"router_output": route_result}