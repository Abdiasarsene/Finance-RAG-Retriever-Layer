# api/core/monitoring.py
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import APIRouter, Response

# Metrics
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["endpoint"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Request latency", ["endpoint"])

router = APIRouter()

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")