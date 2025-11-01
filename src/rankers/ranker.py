from typing import List, Dict

class Ranker:
    """
    Classe pour le ranking initial des résultats des retrievers.
    Fusionne et normalise les scores de différents retrievers.
    """

    def __init__(self, weights: Dict[str, float] = None):
        """
        weights: dictionnaire optionnel pour pondérer chaque retriever
        ex: {'milvus': 0.7, 'elasticsearch': 0.3}
        """
        self.weights = weights or {}

    def normalize_scores(self, docs: List[Dict], retriever_name: str):
        """
        Normalise les scores selon le retriever.
        """
        max_score = max([doc['score'] for doc in docs]) or 1
        for doc in docs:
            doc['score'] = doc['score'] / max_score
            # applique poids si spécifié
            if retriever_name in self.weights:
                doc['score'] *= self.weights[retriever_name]
        return docs

    def rank(self, retriever_results: Dict[str, List[Dict]], top_k: int = 5):
        """
        Fusionne les résultats de plusieurs retrievers et retourne top-k.
        """
        all_docs = []
        for name, docs in retriever_results.items():
            normalized = self.normalize_scores(docs, name)
            all_docs.extend(normalized)
        # tri final
        all_docs.sort(key=lambda x: x['score'], reverse=True)
        return all_docs[:top_k]