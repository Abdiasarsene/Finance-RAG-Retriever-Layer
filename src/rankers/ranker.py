# src/rankers/ranker.py
from typing import List, Dict

# ====== FIRST RANK ======
class Ranker:
    # Set up
    def __init__(self, weights: Dict[str, float] = None):
        """
        weights: optional dictionary to weight each retriever
        ex: {'milvus': 0.7, 'elasticsearch': 0.3}
        """
        self.weights = weights or {}

    # Normalizes scores according to retriever
    def normalize_scores(self, docs: List[Dict], retriever_name: str):
        max_score = max([doc['score'] for doc in docs]) or 1
        for doc in docs:
            doc['score'] = doc['score'] / max_score
            # applique poids si spécifié
            if retriever_name in self.weights:
                doc['score'] *= self.weights[retriever_name]
        return docs

    # Merges results from multiple retrievers and returns top-k
    def rank(self, retriever_results: Dict[str, List[Dict]], top_k: int = 5):
        all_docs = []
        for name, docs in retriever_results.items():
            normalized = self.normalize_scores(docs, name)
            all_docs.extend(normalized)
        # tri final
        all_docs.sort(key=lambda x: x['score'], reverse=True)
        return all_docs[:top_k]