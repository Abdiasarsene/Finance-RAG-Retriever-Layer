from sentence_transformers import CrossEncoder
from typing import List, Dict

class ReRanker:
    """
    Re-ranker pour affiner la pertinence des documents top-k initialement classés.
    Supporte modèles spécifiques selon le type de requête.
    """

    def __init__(self):
        # Modèles par type de requête
        self.models = {
            "semantic": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"),
            "factual": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"),      # à remplacer par un modèle factuel
            "contextual": CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"),   # à remplacer par un modèle contextuel
        }

    def re_rank(self, query: str, docs: List[Dict], query_type: str = "semantic", top_k: int = 5) -> List[Dict]:
        """
        Retourne les documents réordonnés selon le score du modèle choisi.
        """
        model = self.models.get(query_type, self.models["semantic"])
        pairs = [(query, doc["content"]) for doc in docs]
        scores = model.predict(pairs)

        for i, doc in enumerate(docs):
            doc["score"] = scores[i]

        return sorted(docs, key=lambda x: x["score"], reverse=True)[:top_k]