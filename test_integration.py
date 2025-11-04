# test_full_pipeline_script.py
from unittest.mock import patch, MagicMock

# Import pipeline components
from src.routers.query_router import route_query
from src.retrievers.hybrid_retriever import HybridRetriever
from src.rankers.ranker import Ranker
from src.rankers.re_ranker import ReRanker
from src.builders.context_builder import ContextBuilder

# Import mocks
from tests.mocks.mock_milvus import MockMilvusClient
from tests.mocks.mock_es import MockElasticsearchClient

# ======= MOCK CROSSENCODER =======
class MockCrossEncoder:
    def predict(self, pairs):
        # Return a score proportional to length of doc content
        return [len(pair[1]) / 100.0 for pair in pairs]

# ======= MAIN PIPELINE SCRIPT =======
def main():
    query = "Impact of AI on finance article"

    # 1️⃣ Detect query type
    q_type = route_query(query)
    print("Query type:", q_type)

    # 2️⃣ Initialize mocks
    mock_milvus = MockMilvusClient()
    mock_es = MockElasticsearchClient()

    # 3️⃣ Patch HybridRetriever to use mocks
    with patch("src.retrievers.milvus_retriever.Collection", new=MagicMock()):
        with patch("src.retrievers.milvus_retriever.connections.connect", new=MagicMock()):
            retriever = HybridRetriever()
            retriever.milvus.collection = mock_milvus
            retriever.es = mock_es

            # 4️⃣ Insert dummy docs
            dummy_docs = [
                {"id": "doc1", "content": "AI is transforming the finance sector.", "metadata": {"source": "mock"}},
                {"id": "doc2", "content": "Finance analytics benefit from machine learning.", "metadata": {"source": "mock"}},
                {"id": "doc3", "content": "Regulations in banking affect AI adoption.", "metadata": {"source": "mock"}}
            ]
            embeddings = [[0.1 * i for i in range(768)] for _ in dummy_docs]
            retriever.milvus.insert("finance_docs", embeddings, dummy_docs)
            for doc in dummy_docs:
                retriever.es.index("finance_texts", id=doc["id"], document=doc)

            # 5️⃣ Retrieve
            retriever_results = {
                "milvus": retriever.milvus.search("finance_docs", [embeddings[0]])[0],
                "elasticsearch": [
                    {"doc_id": hit["_id"], "score": hit["_score"], "content": hit["_source"]["content"], "metadata": hit["_source"]["metadata"]}
                    for hit in retriever.es.search("finance_texts", {"match": {"content": "finance"}})["hits"]["hits"]
                ]
            }

            print("\nRetriever results:")
            print(retriever_results)

            # 6️⃣ Ranker
            ranker = Ranker(weights={"milvus": 0.7, "elasticsearch": 0.3})
            top_docs = ranker.rank(retriever_results, top_k=5)
            print("\nRanked docs:")
            for doc in top_docs:
                print(doc)

            # 7️⃣ ReRanker with mock CrossEncoder
            reranker = ReRanker()
            for k in reranker.models:
                reranker.models[k] = MockCrossEncoder()
            reranked_docs = reranker.re_rank(query, top_docs, query_type=str(q_type), top_k=5)
            print("\nRe-ranked docs:")
            for doc in reranked_docs:
                print(doc)

            # 8️⃣ Context Builder
            builder = ContextBuilder(max_tokens=50)
            context = builder.build_context(reranked_docs)
            print("\n--- Final Pipeline Context ---\n")
            print(context)

if __name__ == "__main__":
    main()