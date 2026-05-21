from typing import List, Dict, Any, Optional
from ai_system.app.retrieval.dense import DenseRetriever
from ai_system.app.retrieval.sparse import SparseRetriever
from ai_system.app.retrieval.hybrid import HybridRetriever
from ai_system.app.retrieval.reranker import Reranker

class RetrievalManager:
    """
    Orchestrates the full hybrid retrieval pipeline: Dense + Sparse -> Hybrid Merge -> Reranking.

    WHAT:
    The central coordinator for all retrieval operations. It wraps the dense vector, 
    sparse keyword, and reranking components into a unified interface for the system.

    WHAT IS READ:
    - Input documents: Lists of strings (the content) along with their unique IDs and 
      associated metadata (source, timestamp, etc.).
    - Input queries: Natural language strings from the Agent or user.

    WHERE IT GOES:
    - Indexing: Documents are dispersed into two backend stores: ChromaDB (vector index)
      and a Sparse index (managed by SparseRetriever).
    - Output: Returns a ranked list of dictionaries containing content, metadata, 
      and similarity scores for use in LLM context windows.

    HOW:
    1. Hybrid Search: Queries both Dense and Sparse retrievers and merges the results.
    2. Score Normalization: The HybridRetriever aligns scores from different search methods.
    3. Reranking: A cross-encoder model evaluates the merged set to surface the most relevant content.

    WHY:
    By decoupling the search mechanisms from the agent, we can swap or upgrade retrieval 
    backends (e.g., changing models or vector stores) without affecting downstream 
    components. Hybridization balances the broad semantic reach of vector search with 
    the precise technical keyword matching of BM25.
    """
    def __init__(
        self,
        dense_model: str = "all-MiniLM-L6-v2",
        rerank_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
        persist_directory: str = "ai_system/data/embeddings/chroma"
    ):
        self.dense = DenseRetriever(model_name=dense_model, persist_directory=persist_directory)
        self.sparse = SparseRetriever()
        self.hybrid = HybridRetriever(self.dense, self.sparse)
        self.reranker = Reranker(model_name=rerank_model)

    def index_documents(self, documents: List[str], ids: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Indexes documents in both dense and sparse retrievers.
        """
        self.dense.add_documents(documents, ids, metadatas)
        self.sparse.add_documents(documents, ids, metadatas)

    def retrieve(self, query: str, k: int = 5, rerank_top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Complete retrieval pipeline.
        """
        # 1. Hybrid Search
        hybrid_results = self.hybrid.search(query, k=k*2)
        
        # 2. Rerank
        reranked_results = self.reranker.rerank(query, hybrid_results, top_n=rerank_top_n)
        
        return reranked_results

class ContextBuilder:
    """
    Formats retrieved documents into a context block for the LLM.
    """
    @staticmethod
    def build_context(results: List[Dict[str, Any]]) -> str:
        if not results:
            return "No relevant context found."
            
        context_parts = []
        for i, res in enumerate(results):
            context_parts.append(f"Source [{i+1}]:\n{res['content']}")
            
        return "\n\n".join(context_parts)

if __name__ == "__main__":
    # Full System Test
    manager = RetrievalManager()
    
    test_docs = [
        "The transformer architecture uses attention mechanisms to process sequences.",
        "PyTorch is a flexible deep learning framework commonly used for LLM development.",
        "ChromaDB is a vector database designed for AI applications.",
        "Dense retrieval uses embeddings to find semantically similar content.",
        "SentencePiece is used for subword tokenization in many NLP models.",
        "Reranking helps improve the precision of retrieval systems by using more complex models."
    ]
    test_ids = [f"doc_{i}" for i in range(len(test_docs))]
    
    manager.index_documents(test_docs, test_ids)
    
    query = "How to improve retrieval precision?"
    print(f"\nRetrieving for: '{query}'")
    results = manager.retrieve(query)
    
    context = ContextBuilder.build_context(results)
    print("\n--- Formatted Context ---")
    print(context)
