# src/retrievers/hybrid_retriever.py
from src.retrievers.milvus_retriever import MilvusRetriever
from src.retrievers.es_retriever import ElasticsearchRetriever

# ====== HYBRID RETRIEVER ======
class HybridRetriever:
    # Set up
    def __init__(self):
        self.milvus = MilvusRetriever()
        self.es = ElasticsearchRetriever()

    # Apply retriever
    def retrieve(self, query: str, top_k: int = 5):
        milvus_results = self.milvus.retrieve(query, top_k)
        es_results = self.es.retrieve(query, top_k)

        # Simple merge: concat + sort by mean score
        combined = milvus_results + es_results
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:top_k]