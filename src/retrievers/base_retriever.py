# src/retrievers/base_retrievr.py
from abc import ABC, abstractmethod

# ======= BASE RETRIEVER ======
class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5):
        pass