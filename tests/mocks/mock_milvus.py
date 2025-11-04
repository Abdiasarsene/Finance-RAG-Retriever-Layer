# tets/mocks/mock_milvus.py
from typing import List, Dict, Any
import numpy as np
import uuid

# ====== SIMULMATE REAL EXTERNAL SERVICE ======
class MockMilvusClient:
    def __init__(self):
        self._collections: Dict[str, List[Dict[str, Any]]] = {}

    def create_collection(self, name: str):
        if name not in self._collections:
            self._collections[name] = []

    # Simulates the insertion of vectors into a collection.
    def insert(self, collection_name: str, embeddings: List[List[float]], metadatas: List[Dict[str, Any]]):
        self.create_collection(collection_name)
        for vector, meta in zip(embeddings, metadatas):
            self._collections[collection_name].append({
                "id": meta.get("id", str(uuid.uuid4())),
                "embedding": np.array(vector, dtype=float),
                "metadata": meta
            })
        return {"insert_count": len(embeddings)}

    # Returns the top_k most similar vectors according to cosine distance.
    def search(self, collection_name: str, query_vectors: List[List[float]], top_k: int = 5):
        if collection_name not in self._collections or not self._collections[collection_name]:
            return []

        # Cosine similarity
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9)

        results = []
        for qv in query_vectors:
            sims = []
            for doc in self._collections[collection_name]:
                score = cosine_similarity(np.array(qv), doc["embedding"])
                sims.append({"id": doc["id"], "score": score, "metadata": doc["metadata"]})
            sims.sort(key=lambda x: x["score"], reverse=True)
            results.append(sims[:top_k])
        return results

    # Deletes vectors with the specified IDs
    def delete(self, collection_name: str, ids: List[str]):
        if collection_name not in self._collections:
            return {"deleted": 0}
        before = len(self._collections[collection_name])
        self._collections[collection_name] = [
            d for d in self._collections[collection_name] if d["id"] not in ids
        ]
        after = len(self._collections[collection_name])
        return {"deleted": before - after}

    def list_collections(self):
        return list(self._collections.keys())

    def flush(self, collection_name: str):
        """No-op (for compatibility)."""
        return True
