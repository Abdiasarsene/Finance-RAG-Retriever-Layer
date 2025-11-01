from enum import Enum

class QueryType(str, Enum):
    LEXICAL = "lexical"
    SEMANTIC = "semantic"
    FACTUAL = "factual"
    CONTEXTUAL = "contextual"

def route_query(query: str) -> QueryType:
    """Stub logic for now"""
    if "article" in query.lower():
        return QueryType.LEXICAL
    elif "impact" in query.lower() or "effet" in query.lower():
        return QueryType.SEMANTIC
    else:
        return QueryType.CONTEXTUAL