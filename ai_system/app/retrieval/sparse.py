import re
import numpy as np
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi

class SparseRetriever:
    """
    Handles sparse retrieval using the BM25 algorithm.
    Suitable for exact term matching and technical keyword retrieval.
    """
    def __init__(self):
        self.bm25 = None
        self.documents = []
        self.ids = []
        self.metadatas = []

    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenizer that converts text to lowercase and splits into words.
        Removes non-alphanumeric characters for better keyword matching.
        """
        text = text.lower()
        # Keep alphanumeric and some technical characters like _ and -
        tokens = re.findall(r'[a-z0-9_\-]+', text)
        return tokens

    def add_documents(self, documents: List[str], ids: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Tokenizes and indexes documents for BM25 search.
        """
        print(f"Adding {len(documents)} documents to sparse index...")
        self.documents.extend(documents)
        self.ids.extend(ids)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            self.metadatas.extend([{"source": "manual"} for _ in documents])
            
        tokenized_corpus = [self._tokenize(doc) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized_corpus)
        print("Documents indexed successfully.")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs BM25 search for a given query.
        """
        if not self.bm25:
            return []
            
        tokenized_query = self._tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        
        # Get top k indices
        top_n = np.argsort(scores)[::-1][:k]
        
        formatted_results = []
        for i in top_n:
            if scores[i] <= 0: # Skip documents with no relevance
                continue
            formatted_results.append({
                "id": self.ids[i],
                "content": self.documents[i],
                "metadata": self.metadatas[i],
                "score": float(scores[i])
            })
            
        return formatted_results

if __name__ == "__main__":
    # Test script
    retriever = SparseRetriever()
    
    test_docs = [
        "The transformer architecture uses attention mechanisms to process sequences.",
        "PyTorch is a flexible deep learning framework commonly used for LLM development.",
        "ChromaDB is a vector database designed for AI applications.",
        "Dense retrieval uses embeddings to find semantically similar content.",
        "SentencePiece is used for subword tokenization in many NLP models."
    ]
    test_ids = [f"id_{i}" for i in range(len(test_docs))]
    
    retriever.add_documents(test_docs, test_ids)
    
    query = "transformer attention"
    print(f"\nSearching for: '{query}'")
    results = retriever.search(query, k=2)
    
    for res in results:
        print(f"- [{res['score']:.4f}] {res['content']}")
        
    query = "PyTorch deep learning"
    print(f"\nSearching for: '{query}'")
    results = retriever.search(query, k=2)
    
    for res in results:
        print(f"- [{res['score']:.4f}] {res['content']}")
