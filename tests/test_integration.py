# test_full_pipeline_script.py
from unittest.mock import MagicMock
from src.routers.query_router import route_query
from src.rankers.ranker import Ranker
from src.rankers.re_ranker import ReRanker
from src.builders.context_builder import ContextBuilder
from tests.mocks.mock_milvus import MockMilvusClient
from tests.mocks.mock_es import MockElasticsearchClient

# ======= MOCK CROSSENCODER =======
class MockCrossEncoder:
    def predict(self, pairs):
        # Return a score proportional to length of doc content
        return [len(pair[1]) / 100.0 for pair in pairs]

# ======= MOCK HYBRID RETRIEVER =======
class MockHybridRetriever:
    def __init__(self, milvus_mock, es_mock):
        self.milvus = milvus_mock
        self.es = es_mock

    def retrieve(self, query, top_k=5):
        # Milvus retrieval
        milvus_results_raw = self.milvus.search(
            "finance_docs", [[0.1 * i for i in range(768)]], top_k
        )[0]
        milvus_results = [
            {"doc_id": doc["id"], "score": doc["score"], "content": doc["metadata"]["content"], "metadata": doc["metadata"]}
            for doc in milvus_results_raw
        ]

        # Elasticsearch retrieval
        es_hits = self.es.search("finance_texts", {"match": {"content": "finance"}})["hits"]["hits"]
        es_results = [
            {"doc_id": hit["_id"], "score": hit["_score"], "content": hit["_source"]["content"], "metadata": hit["_source"]["metadata"]}
            for hit in es_hits
        ]

        # Combine results
        combined = milvus_results + es_results
        combined.sort(key=lambda x: x["score"], reverse=True)
        return combined[:top_k]

# ======= MAIN PIPELINE SCRIPT =======
def main():
    query = "Impact of AI on finance article"

    # Detect query type
    q_type = route_query(query)
    print("Query type:", q_type)

    # Initialize mocks
    mock_milvus = MockMilvusClient()
    mock_es = MockElasticsearchClient()

    # Insert dummy docs
    dummy_docs = [
        {"id": "doc1", "content": "AI is transforming the finance sector.", "metadata": {"content": "AI is transforming the finance sector.", "source": "mock"}},
        {"id": "doc2", "content": "Finance analytics benefit from machine learning.", "metadata": {"content": "Finance analytics benefit from machine learning.", "source": "mock"}},
        {"id": "doc3", "content": "Regulations in banking affect AI adoption.", "metadata": {"content": "Regulations in banking affect AI adoption.", "source": "mock"}}
    ]
    embeddings = [[0.1 * i for i in range(768)] for _ in dummy_docs]
    mock_milvus.insert("finance_docs", embeddings, dummy_docs)
    for doc in dummy_docs:
        mock_es.index("finance_texts", id=doc["id"], document=doc)

    # Initialize HybridRetriever with mocks
    retriever = MockHybridRetriever(mock_milvus, mock_es)

    # Retrieve
    retriever_results = {
        "milvus": retriever.retrieve(query, top_k=5),
        "elasticsearch": []  # already merged inside retrieve
    }

    print("\nRetriever results:")
    for doc in retriever_results["milvus"]:
        print(doc)

    # Ranker
    ranker = Ranker(weights={"milvus": 0.7, "elasticsearch": 0.3})
    top_docs = ranker.rank({"milvus": retriever_results["milvus"]}, top_k=5)
    print("\nRanked docs:")
    for doc in top_docs:
        print(doc)

    # ReRanker with mock CrossEncoder
    reranker = ReRanker()
    for k in reranker.models:
        reranker.models[k] = MockCrossEncoder()
    reranked_docs = reranker.re_rank(query, top_docs, query_type=str(q_type), top_k=5)
    print("\nRe-ranked docs:")
    for doc in reranked_docs:
        print(doc)

    # Context Builder
    builder = ContextBuilder(max_tokens=50)
    context = builder.build_context(reranked_docs)
    print("\n--- Final Pipeline Context ---\n")
    print(context)

if __name__ == "__main__":
    main()