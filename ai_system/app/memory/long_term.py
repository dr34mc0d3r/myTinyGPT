import os
import uuid
import time
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.utils import embedding_functions

class LongTermMemory:
    """
    Persistent vector storage for long-term memory using ChromaDB.
    """
    def __init__(
        self, 
        model_name: str = "all-MiniLM-L6-v2", 
        persist_directory: str = "data/embeddings/chroma",
        collection_name: str = "agent_memories"
    ):
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=model_name
        )
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn,
            metadata={"hnsw:space": "cosine"}
        )

    def save_memory(self, text: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Saves a text chunk as a memory.
        """
        mem_id = str(uuid.uuid4())
        default_metadata = {"timestamp": time.time(), "type": "conversation_event"}
        if metadata:
            default_metadata.update(metadata)
            
        self.collection.add(
            documents=[text],
            ids=[mem_id],
            metadatas=[default_metadata]
        )

    def recall(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieves relevant memories for a given query.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )
        
        formatted = []
        if results['ids']:
            for i in range(len(results['ids'][0])):
                formatted.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": 1 - results['distances'][0][i]
                })
        return formatted

if __name__ == "__main__":
    # Test
    ltm = LongTermMemory()
    ltm.save_memory("The user likes to talk about AI and transformers.", {"category": "preferences"})
    ltm.save_memory("The user mentioned their name is Chris.", {"category": "user_info"})
    
    print("\nRecalling info about the user:")
    memories = ltm.recall("What do we know about the user?")
    for m in memories:
        print(f"- [{m['score']:.4f}] {m['content']}")
