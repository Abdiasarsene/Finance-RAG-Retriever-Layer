# src/retrievrs/es_retriever.py
from src.retrievers.base_retriever import BaseRetriever

# ====== LEASTICSEARCH RETRIEVER ======
class ElasticsearchRetriever(BaseRetriever):
    # Stub - in real life you would have an Elasticsearch client
    def __init__(self):
        pass

    # Returns a false list to simulate the behavior
    def retrieve(self, query: str, top_k: int = 5):
        return [
            {"doc_id": f"es_{i}", "score": 1.0 / (i + 1), "content": f"Result {i} for '{query}'"}
            for i in range(top_k)
        ]