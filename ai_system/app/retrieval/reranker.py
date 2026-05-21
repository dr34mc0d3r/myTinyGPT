from typing import List, Dict, Any
from sentence_transformers import CrossEncoder

class Reranker:
    """
    Reranks retrieval results using a Cross-Encoder model.
    Provides more accurate relevance scoring than bi-encoders.
    """
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model_name = model_name
        self.model = CrossEncoder(model_name)
        print(f"Reranker initialized with model: {model_name}")

    def rerank(self, query: str, documents: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Scores each document against the query and sorts by relevance.
        """
        if not documents:
            return []
            
        # Prepare pairs for cross-encoder
        pairs = [[query, doc['content']] for doc in documents]
        
        # Get scores from cross-encoder
        scores = self.model.predict(pairs)
        
        # Update scores and sort
        for i, doc in enumerate(documents):
            doc['rerank_score'] = float(scores[i])
            
        # Sort by rerank_score
        reranked = sorted(documents, key=lambda x: x['rerank_score'], reverse=True)
        
        return reranked[:top_n]

if __name__ == "__main__":
    # Test script
    reranker = Reranker()
    
    query = "transformers and attention"
    # Simulated hybrid results
    test_results = [
        {"id": "id_0", "content": "The transformer architecture uses attention mechanisms to process sequences.", "score": 1.0},
        {"id": "id_4", "content": "SentencePiece is used for subword tokenization in many NLP models.", "score": 0.095},
        {"id": "id_1", "content": "PyTorch is a flexible deep learning framework commonly used for LLM development.", "score": 0.08}
    ]
    
    print(f"\nReranking results for: '{query}'")
    reranked_results = reranker.rerank(query, test_results, top_n=2)
    
    for res in reranked_results:
        print(f"- [{res['rerank_score']:.4f}] {res['content']}")
