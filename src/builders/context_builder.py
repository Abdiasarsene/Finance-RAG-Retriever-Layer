from typing import List, Dict

class ContextBuilder:
    """
    Transforme les résultats top-k en un contexte clair pour le LLM.
    Ne fait pas de LLM integration.
    """

    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens  # limite à respecter pour LLM

    def build_context(self, docs: List[Dict]) -> str:
        """
        Concatène les chunks en respectant max_tokens et format propre.
        """
        context = ""
        current_tokens = 0

        for doc in docs:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            # estimation simple tokens = mots (ou utiliser tokenizer réel)
            token_count = len(content.split())
            if current_tokens + token_count > self.max_tokens:
                break

            # formatage simple : contenu + métadonnées
            meta_str = " | ".join(f"{k}: {v}" for k, v in metadata.items())
            context += f"{content} [{meta_str}]\n"
            current_tokens += token_count

        return context