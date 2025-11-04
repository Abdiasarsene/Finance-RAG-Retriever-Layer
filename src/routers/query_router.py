# src/routers/query_router.py
from enum import Enum

# ====== DETECT TYPE OF QUERY ======
class QueryType(str, Enum):
    LEXICAL = "lexical"
    SEMANTIC = "semantic"
    FACTUAL = "factual"
    CONTEXTUAL = "contextual"

# ======= ROUTE OF QUERY ======
def route_query(query: str) -> QueryType:
    """Stub logic for now"""
    if "article" in query.lower():
        return QueryType.LEXICAL
    elif "impact" in query.lower() or "effet" in query.lower():
        return QueryType.SEMANTIC
    else:
        return QueryType.CONTEXTUAL