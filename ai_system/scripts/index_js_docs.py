"""
Script: index_js_docs.py
Purpose: Facilitates the ingestion of JavaScript-related documentation into the myTinyGPT retrieval system.

WHAT:
This script automates the process of loading local markdown (.md) documentation files, 
cleaning them of excessive formatting, and indexing them into the Hybrid Retrieval 
system (Dense Vector Search + BM25 Sparse Search).

WHAT IS READ:
- Source: `ai_system/data/raw/javascript_docs/`
- Format: All files with the `.md` extension.
- Content: Raw technical documentation, code snippets, and architectural guides.

WHERE IT GOES:
- Dense Vector Store: ChromaDB collection (defined in `RetrievalManager`).
- Sparse Index: BM25 index memory/file store (managed by `SparseRetriever`).

HOW:
1. It utilizes the custom `markdown_parser` utility to normalize the markdown text.
2. It invokes the `RetrievalManager`, which handles the heavy lifting of embedding
   generation (via SentenceTransformers) and vector storage (in ChromaDB).
3. It performs a batch index operation to ensure consistency across retrieval methods.

WHY:
By cleaning and normalizing our documentation before indexing, we significantly reduce 
"noise" in the embedding space. This leads to higher-quality retrieval (better semantic 
matches and keyword precision), which in turn provides the agent with more accurate
context for answering technical JavaScript queries.
"""

import sys
import os
import shutil

# Add project root to path so we can import ai_system modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from ai_system.app.retrieval.manager import RetrievalManager
from ai_system.app.utils.markdown_parser import load_markdown_files
from ai_system.app.utils.ingest_prep import clean_hidden_files

def run_indexing():
    # 0. Configuration
    db_path = "ai_system/data/embeddings/chroma"
    docs_path = "ai_system/data/raw/javascript_docs/"

    # 1. Clean the data directory
    clean_hidden_files(docs_path)

    # 2. Database Cleanup Confirmation
    if os.path.exists(db_path):
        confirm = input(f"Existing ChromaDB found at '{db_path}'.\nDo you want to clear it and start fresh? (Y/N): ").strip().upper()
        if confirm == 'Y':
            print("Clearing existing database...")
            shutil.rmtree(db_path)
            print("Database cleared.")
        else:
            print("Indexing aborted by user.")
            return

    # 3. Initialize the manager
    # The manager handles the orchestration of Dense and Sparse retrievers.
    manager = RetrievalManager()

    # 4. Define the source directory for documentation
    if not os.path.exists(docs_path):
        print(f"Error: Directory {docs_path} not found.")
        return

    # 5. Load and clean your markdown files
    # This uses our parser to remove markdown syntax that might confuse the model
    # while preserving the structural content.
    print(f"Loading markdown files from: {docs_path}")
    markdown_docs = load_markdown_files(docs_path)

    if not markdown_docs:
        print("No markdown files found to index.")
        return

    print(f"Successfully loaded and cleaned {len(markdown_docs)} documents.")

    # 6. Prepare data for indexing
    # We extract contents, ids, and metadata as expected by the RetrievalManager.
    contents = [doc["content"] for doc in markdown_docs]
    ids = [doc["id"] for doc in markdown_docs]
    metadatas = [doc["metadata"] for doc in markdown_docs]

    # 7. Index the documents
    # This adds documents to both ChromaDB (vector) and the BM25 (sparse) index.
    print(f"Communicating with RetrievalManager to index {len(markdown_docs)} documents... (this may take a moment)")
    manager.index_documents(contents, ids, metadatas=metadatas)

    print(f"Successfully indexed {len(markdown_docs)} documents into both Vector Store and Sparse Index.")
if __name__ == "__main__":
    run_indexing()
