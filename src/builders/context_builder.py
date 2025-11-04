# src/builders/context_builder.py
from typing import List, Dict

# ====== CONTEXT BUILDER ======
class ContextBuilder:
    # Set  up
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens

    # Concatenates chunks respecting max_tokens and clean format
    def build_context(self, docs: List[Dict]) -> str:
        context = ""
        current_tokens = 0
        for doc in docs:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            # estimate simple tokens = word
            token_count = len(content.split())
            if current_tokens + token_count > self.max_tokens:
                break

            # simple formatting: content + metadata
            meta_str = " | ".join(f"{k}: {v}" for k, v in metadata.items())
            context += f"{content} [{meta_str}]\n"
            current_tokens += token_count
        return context