from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    """Interface commune à tous les retrievers."""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5):
        """Exécute la recherche et renvoie une liste de documents"""
        pass