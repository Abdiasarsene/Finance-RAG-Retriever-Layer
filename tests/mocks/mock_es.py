# tets/mocks/mock_es.py
from typing import Dict, Any, List
import re
import uuid

# ====== MOCK ELASTICSEARCH CLIENT ======
class MockElasticsearchClient:
    def __init__(self):
        self._indices: Dict[str, Dict[str, Dict[str, Any]]] = {}

    # Simulates document indexing.
    def index(self, index: str, id: str = None, document: Dict[str, Any] = None):
        if index not in self._indices:
            self._indices[index] = {}
        doc_id = id or str(uuid.uuid4())
        self._indices[index][doc_id] = document or {}
        return {"result": "created", "_id": doc_id}

    # Naive search on text field (match)
    def search(self, index: str, query: Dict[str, Any], size: int = 10):
        if index not in self._indices:
            return {"hits": {"hits": []}}

        hits = []
        q = query.get("match", {})
        for field, value in q.items():
            pattern = re.compile(re.escape(str(value)), re.IGNORECASE)
            for doc_id, doc in self._indices[index].items():
                field_val = str(doc.get(field, ""))
                if pattern.search(field_val):
                    hits.append({
                        "_id": doc_id,
                        "_source": doc,
                        "_score": 1.0  # Simulated
                    })
        return {"hits": {"hits": hits[:size]}}

    # Removes a document from an index.
    def delete(self, index: str, id: str):
        if index not in self._indices or id not in self._indices[index]:
            return {"result": "not_found"}
        del self._indices[index][id]
        return {"result": "deleted"}

    def indices_exists(self, index: str):
        return index in self._indices

    def create_index(self, index: str):
        if index not in self._indices:
            self._indices[index] = {}
        return {"acknowledged": True}