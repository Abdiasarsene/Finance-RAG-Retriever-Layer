# src/rankers/re_ranker.py
from sentence_transformers import CrossEncoder
from typing import List, Dict

# ====== RE-RANKER ======
class ReRanker:
    # Set up
    def __init__(self):
        # Templates by query type
        self.models = {
            "semantic": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"),
            "factual": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"), 
            "contextual": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"), 
        }

    # Returns documents reordered according to the selected template score.
    def re_rank(self, query: str, docs: List[Dict], query_type: str = "semantic", top_k: int = 5) -> List[Dict]:
        model = self.models.get(query_type, self.models["semantic"])
        pairs = [(query, doc["content"]) for doc in docs]
        scores = model.predict(pairs)
        for i, doc in enumerate(docs):
            doc["score"] = scores[i]
        return sorted(docs, key=lambda x: x["score"], reverse=True)[:top_k]