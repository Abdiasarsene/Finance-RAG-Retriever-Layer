from src.retrievers.milvus_retriever import MilvusRetriever
from src.retrievers.es_retriever import ElasticsearchRetriever

class HybridRetriever:
    def __init__(self):
        self.milvus = MilvusRetriever()
        self.es = ElasticsearchRetriever()

    def retrieve(self, query: str, top_k: int = 5):
        milvus_results = self.milvus.retrieve(query, top_k)
        es_results = self.es.retrieve(query, top_k)

        # Fusion simple : concat + tri par score moyen
        combined = milvus_results + es_results
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:top_k]