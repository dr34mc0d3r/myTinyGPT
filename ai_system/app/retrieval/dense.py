import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

class DenseRetriever:
    """
    Handles dense vector retrieval using SentenceTransformers and ChromaDB.
    """
    def __init__(
        self, 
        model_name: str = "all-MiniLM-L6-v2", 
        persist_directory: str = "data/embeddings/chroma",
        collection_name: str = "mytinygpt_docs"
    ):
        self.model_name = model_name
        self.persist_directory = persist_directory
        
        # Initialize embedding function for ChromaDB
        # We use the SentenceTransformerEmbeddingFunction for seamless integration
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"} # Use cosine similarity
        )
        
        print(f"DenseRetriever initialized with model: {model_name}")
        print(f"ChromaDB persisting to: {persist_directory}")

    def add_documents(self, documents: List[str], ids: List[str], metadatas: Optional[List[Dict[str, Any]]] = None):
        """
        Embeds and adds documents to the vector database with detailed progress reporting.
        """
        if metadatas is None:
            metadatas = [{"source": "manual"} for _ in documents]
            
        chunk_size = 1000
        print(f"Adding {len(documents)} documents to dense index in chunks of {chunk_size}...")
        
        # Iterate through documents with tqdm for progress tracking
        for i in tqdm(range(len(documents)), desc="Processing documents"):
            # Individual document reporting
            print(f"Indexing document {i+1}/{len(documents)}: {ids[i]}")
            
            # Index in batches as before, but reporting is individual
            # Note: For efficiency, we still batch calls to collection.add
            if (i + 1) % chunk_size == 0 or (i + 1) == len(documents):
                start_batch = max(0, (i // chunk_size) * chunk_size)
                end_batch = i + 1
                self.collection.add(
                    documents=documents[start_batch:end_batch],
                    ids=ids[start_batch:end_batch],
                    metadatas=metadatas[start_batch:end_batch]
                )
        print("Documents added successfully.")

    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Performs similarity search for a given query.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results for easier consumption
        formatted_results = []
        # Results are lists of lists because query_texts is a list
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "score": 1 - results['distances'][0][i] # Convert distance to similarity score
            })
            
        return formatted_results

    def delete_collection(self):
        """Deletes the current collection."""
        self.client.delete_collection(self.collection.name)
        print(f"Collection {self.collection.name} deleted.")

if __name__ == "__main__":
    # Test script
    retriever = DenseRetriever()
    
    test_docs = [
        "The transformer architecture uses attention mechanisms to process sequences.",
        "PyTorch is a flexible deep learning framework commonly used for LLM development.",
        "ChromaDB is a vector database designed for AI applications.",
        "Dense retrieval uses embeddings to find semantically similar content.",
        "SentencePiece is used for subword tokenization in many NLP models."
    ]
    test_ids = [f"id_{i}" for i in range(len(test_docs))]
    
    retriever.add_documents(test_docs, test_ids)
    
    query = "How do transformers work?"
    print(f"\nSearching for: '{query}'")
    results = retriever.search(query, k=2)
    
    for res in results:
        print(f"- [{res['score']:.4f}] {res['content']}")
