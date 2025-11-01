from src.retrievers.base_retriever import BaseRetriever

class ElasticsearchRetriever(BaseRetriever):
    def __init__(self):
        # Stub - en vrai tu aurais un client Elasticsearch
        pass

    def retrieve(self, query: str, top_k: int = 5):
        # Retourne une fausse liste pour simuler le comportement
        return [
            {"doc_id": f"es_{i}", "score": 1.0 / (i + 1), "content": f"Result {i} for '{query}'"}
            for i in range(top_k)
        ]