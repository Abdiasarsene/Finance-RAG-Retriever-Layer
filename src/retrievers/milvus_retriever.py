# src/retrievers/milvus_retriever.py
from src.retrievers.base_retriever import BaseRetriever
from pymilvus import connections, Collection
import numpy as np

# ====== MILVUS RETRIEVER ======
class MilvusRetriever(BaseRetriever):
    # Set up
    def __init__(self, host="milvus", port="19530", collection_name="finance_docs"):
        connections.connect(host=host, port=port)
        self.collection = Collection(collection_name)

    # Call encoder for embedding
    def retrieve(self, query: str, top_k: int = 5):
        embedding = np.random.rand(768).tolist()
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["doc_id", "content", "metadata"]
        )
        hits = [
            {
                "doc_id": hit.id,
                "score": hit.distance,
                "content": hit.entity.get("content"),
                "metadata": hit.entity.get("metadata")
            }
            for hit in results[0]
        ]
        return hits