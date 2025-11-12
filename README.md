# **Finance RAG: 02 – Retriever Layer**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-success)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-orange)](https://python.langchain.com/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-informational)](https://www.docker.com/)
[![ElasticSearch](https://img.shields.io/badge/ElasticSearch-Search%20Engine-yellow)](https://www.elastic.co/elasticsearch/)

*"This second core layer of the **Finance-RAG** project handles **retrieval and hierarchical ranking of financial information**.
The **first stage — the Data Engineering module — is already completed** and can be found here:
👉 [Finance-RAG-Data-Engineering](https://github.com/Abdiasarsene/Finance-RAG-Data-Engineering)
Here, the goal is to transform processed data into **structured, ranked, and contextually relevant information** that can be directly consumed by large language models (LLMs)."*

---

---

## ⚙️ **Capabilities**

1. **Input Parsing** – receives and categorizes incoming user queries via the **Router**.
2. **Retrieval Layer** – performs parallel searches across multiple backends (ElasticSearch, Milvus, etc.).
3. **Ranking Layer** – applies multi-criteria filtering and reorders retrieved chunks based on relevance.
4. **Context Builder** – consolidates and formats the final context for interpretation.
5. **API Serving** – provides a unified interface for the LLM to consume the ranked results.

---

---

## 📊 **Data Pipeline Overview**

The Retriever Layer operates as the **bridge between raw document retrieval and semantic reasoning**. Once a user query reaches the Router, it dynamically identifies the query type and routes it to the appropriate retrievers. These retrievers then pull semantically aligned data from vector databases, ensuring precision in both lexical and contextual similarity.

Once the documents are retrieved, the Rankers step in. They first perform a top-k selection based on cosine similarity or BM25, followed by a **contextual refinement stage** using either a **cross-encoder** or a **lightweight LLM reranker**, depending on the request. The **Builder** then structures the context into a form that’s directly usable by the next pipeline layer, while the **API** ensures seamless interaction between this retriever system and the core LLM module.

---

---

## 🧩 **Architecture Snapshot**

```text
┌─────────────────────────────────────────────┐
│                 USER QUERY                  │
└─────────────────────────────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │       Router       │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │     Retrievers     │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │      Rankers       │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │      Builder       │
        └────────────────────┘
                    │
                    ▼
        ┌────────────────────┐
        │        API         │
        └────────────────────┘
```

---

---

## 🧪 **Testing**

Unit and integration tests validate the integrity and cohesion of each module:

* **Unit tests** → Validate the logic and consistency of each subcomponent (`pytest`).
* **Integration tests** → Simulate complete end-to-end retrieval flows to ensure inter-module harmony.

---

---
## 🚀 **Next Modules**

* **Finance-RAG-LLM-Integration**
* **Finance-RAG-Agents**
* **Finance-RAG-Serving-API**
* **Finance-RAG-LLMops**
