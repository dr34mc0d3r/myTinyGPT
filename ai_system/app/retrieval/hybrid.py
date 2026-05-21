from typing import List, Dict, Any, Optional
from ai_system.app.retrieval.dense import DenseRetriever
from ai_system.app.retrieval.sparse import SparseRetriever

class HybridRetriever:
    """
    Combines Dense and Sparse retrieval results.
    Implements normalization, weighted merging, and deduplication.
    """
    def __init__(
        self, 
        dense_retriever: DenseRetriever, 
        sparse_retriever: SparseRetriever,
        dense_weight: float = 0.5,
        sparse_weight: float = 0.5
    ):
        self.dense = dense_retriever
        self.sparse = sparse_retriever
        self.dense_weight = dense_weight
        self.sparse_weight = sparse_weight

    def _normalize_scores(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalizes scores to a 0-1 range using min-max scaling.
        """
        if not results:
            return []
            
        scores = [res['score'] for res in results]
        min_score = min(scores)
        max_score = max(scores)
        
        if max_score == min_score:
            for res in results:
                res['norm_score'] = 1.0
            return results
            
        for res in results:
            res['norm_score'] = (res['score'] - min_score) / (max_score - min_score)
            
        return results

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs hybrid search by merging dense and sparse results.
        """
        # Get results from both retrievers (fetching more than k to allow for overlap/merging)
        dense_results = self.dense.search(query, k=k*2)
        sparse_results = self.sparse.search(query, k=k*2)
        
        # Normalize scores
        dense_results = self._normalize_scores(dense_results)
        sparse_results = self._normalize_scores(sparse_results)
        
        # Merge results with weights
        combined_results = {}
        
        # Process dense results
        for res in dense_results:
            doc_id = res['id']
            combined_results[doc_id] = {
                "content": res['content'],
                "metadata": res['metadata'],
                "score": res['norm_score'] * self.dense_weight
            }
            
        # Process sparse results and deduplicate
        for res in sparse_results:
            doc_id = res['id']
            if doc_id in combined_results:
                combined_results[doc_id]['score'] += res['norm_score'] * self.sparse_weight
            else:
                combined_results[doc_id] = {
                    "content": res['content'],
                    "metadata": res['metadata'],
                    "score": res['norm_score'] * self.sparse_weight
                }
                
        # Convert to list and sort by combined score
        merged = [
            {"id": doc_id, **data} 
            for doc_id, data in combined_results.items()
        ]
        merged.sort(key=lambda x: x['score'], reverse=True)
        
        return merged[:k]

if __name__ == "__main__":
    # Test script
    dense = DenseRetriever()
    sparse = SparseRetriever()
    
    test_docs = [
        "The transformer architecture uses attention mechanisms to process sequences.",
        "PyTorch is a flexible deep learning framework commonly used for LLM development.",
        "ChromaDB is a vector database designed for AI applications.",
        "Dense retrieval uses embeddings to find semantically similar content.",
        "SentencePiece is used for subword tokenization in many NLP models."
    ]
    test_ids = [f"id_{i}" for i in range(len(test_docs))]
    
    # We don't need to re-add to dense as it's persistent, 
    # but for testing reproducibility we might want to ensure they are there.
    # Note: ChromaDB add is idempotent if IDs match.
    dense.add_documents(test_docs, test_ids)
    sparse.add_documents(test_docs, test_ids)
    
    hybrid = HybridRetriever(dense, sparse)
    
    query = "transformers and attention"
    print(f"\nSearching for: '{query}'")
    results = hybrid.search(query, k=3)
    
    for res in results:
        print(f"- [{res['score']:.4f}] {res['content']}")
