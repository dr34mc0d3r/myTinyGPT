# Multi-Domain Knowledge: Scaling myTinyGPT

This document details how **myTinyGPT** handles multiple, distinct knowledge domains (e.g., JavaScript Documentation, Gardening Guides, etc.) within a single instance. 

---

## 1. The Strategy: ChromaDB Collections
You do not need multiple copies of the system. ChromaDB uses **Collections**—distinct "folders" of data within a single database file.

- **System Centrality**: The LLM, Agent, and Tools remain constant.
- **Knowledge Segregation**: Collections keep your "JavaScript" vector space separate from your "Gardening" vector space, ensuring high retrieval precision.
- **Unified Storage**: All indices reside in `ai_system/data/embeddings/chroma/`, keeping your file structure clean.

---

## 2. Implementation Plan: Dynamic Collection Support

To enable the system to switch between knowledge bases, we will follow this development plan:

### Phase 1: Parameterize Retrieval
- [ ] Modify `RetrievalManager` to accept an optional `collection_name` argument in its constructor.
- [ ] Ensure the `DenseRetriever` uses the provided collection name when interacting with ChromaDB.

### Phase 2: Domain-Specific Indexers
- [ ] Create a modular indexing script (or update the existing one) to accept CLI arguments for source path and target collection name:
  ```bash
  python3 ai_system/scripts/index_docs.py --source data/raw/gardening_docs/ --collection gardening_docs
  ```

### Phase 3: Agentic Topic Routing (Optional)
- [ ] Implement a lightweight heuristic or classifier in the `AgentController`.
- [ ] When a user query arrives, the agent selects the appropriate collection based on keywords (e.g., "function" -> `javascript_docs`, "flower" -> `gardening_docs`).

---

## 3. Workflow for Adding New Domains
1. **Prepare Data**: Place your new markdown files in `ai_system/data/raw/<new_topic>_docs/`.
2. **Index**: Run the generalized indexing script pointing to the new directory and collection name.
3. **Query**: The agent can now access the new domain via the routing logic or by explicitly specifying the collection.

---
*Last Updated: Monday, May 18, 2026*
