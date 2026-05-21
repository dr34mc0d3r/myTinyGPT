# Learning Log: myTinyGPT - System Deep Dive

This document provides a comprehensive technical overview of all aspects of the **myTinyGPT** system. It is designed to serve as both a reference for developers and an educational resource for those learning about modern AI architectures.

---

## 1. Project Philosophy & Architecture
**myTinyGPT** is built on the principle of **Agentic Hybrid Retrieval**. The core idea is that a small, efficient LLM can outperform much larger models if it is properly integrated with external knowledge (Retrieval), functional capabilities (Tools), and state awareness (Memory).

### High-Level Data Flow:
1. **User Query**: Received via the FastAPI `/chat` endpoint.
2. **Memory Recall**: The `MemoryManager` retrieves recent context (STM) and relevant past interactions (LTM).
3. **Retrieval Orchestration**: The `RetrievalManager` performs a multi-stage search (Dense + Sparse + Rerank) to find supporting facts.
4. **Agent Logic**: The `AgentController` synthesizes memory, retrieved context, and tool outputs (e.g., Calculator) into a final prompt.
5. **LLM Generation**: The `TinyTransformer` generates a response based on the enriched prompt.
6. **Persistence**: The interaction is saved back into the Memory system.

## 2. Tokenization: The SentencePiece Unigram Model
Before text reaches the model, it must be converted into numerical IDs. We use **SentencePiece** for this task.

- **Why Unigram?**: Unlike BPE (Byte Pair Encoding) which builds up from characters, the Unigram model starts with a large vocabulary and iteratively removes the least useful tokens. This often results in more linguistically meaningful subwords.
- **Subword Advantages**: It allows the system to handle an infinite vocabulary with a finite set of tokens. For example, "unbelievable" might be broken into `un`, `believ`, and `able`.
- **Re-training the Tokenizer**: A tokenizer is built on a specific "corpus" (the initial text it was trained on). If your new dataset is significantly different from the original (e.g., shifting from general English to highly technical JavaScript or a completely different language like French), the existing tokenizer might break words into awkward, inefficient, or overly long sequences. Re-training builds a custom vocabulary that captures the unique patterns and symbols of your new domain, ensuring the Tiny Transformer sees the most meaningful representation of the data possible.

### When to Re-train the Tokenizer
- **Is it just a new topic?** (e.g., Gardening, Cooking, History). **No need to re-train.** General English tokens are sufficient to cover these topics well.
- **Is it a new language or formal syntax?** (e.g., JavaScript, Python, Math formulas). **Yes, re-train.** Programming languages have unique symbols (`===`, `=>`, `{`, `}`) and technical identifiers that general-purpose English tokenizers often break into inefficient, tiny character fragments. Training on a combined corpus (General English + Code) ensures the tokenizer learns these technical identifiers and symbols as singular, high-value tokens.

## 3. Core LLM: The Tiny Transformer
The "brain" of the system is a decoder-only transformer implemented in pure PyTorch.

- **Causal Self-Attention**: The heart of the transformer. It uses `Q` (Query), `K` (Key), and `V` (Value) matrices to determine how much "attention" each token should pay to every previous token. The "causal" part ensures the model cannot "cheat" by looking at future tokens.
- **Multi-Head Attention**: We use 4 heads. This allows the model to attend to different types of information simultaneously (e.g., one head might focus on grammar, another on factual entities).
- **Feed-Forward Network (MLP)**: Two linear layers with a **GELU** activation in between. This provides the non-linear processing power needed to model complex patterns.
- **Weight Tying**: We share weights between the input embedding layer and the output linear head. This reduces the number of parameters by roughly 30%, making the model more memory-efficient.
- **Pre-Normalization**: We apply `LayerNorm` *before* the attention and MLP blocks, which stabilizes training for deeper models.

## 4. The Training Pipeline
Training a transformer involves teaching it to predict the "next token" in a sequence.

- **Objective**: Cross-Entropy Loss between predicted logits and target token IDs.
- **Data Chunking**: We slice tokenized text into overlapping windows of `block_size` (256) to maximize training efficiency from limited text.
- **AdamW Optimizer**: A variation of Adam that handles weight decay correctly, leading to better generalization.
- **LR Scheduler**: Linear warmup for 2000 steps followed by Cosine Decay. Warmup prevents the model from diverging early on, while decay allows for fine-grained convergence.

## 5. Hybrid Retrieval: Combining Dense & Sparse
Retrieval bridges the gap between the model's static training and dynamic real-world information.

- **Dense Retrieval (Semantic)**: Uses `Sentence-Transformers` to map text to a 384-dimensional vector space. Similarity is measured by **Cosine Distance**. This finds "concepts."
- **Sparse Retrieval (Keyword)**: Uses **BM25**, a probabilistic ranking function. This finds "exact terms" like specific error codes or function names.
- **Hybrid Fusion**: We use **Min-Max Normalization** to bring scores from both systems into the same range (0-1), then apply a **Weighted Sum** (default 50/50) to produce a combined rank.
- **Reranking**: We use a **Cross-Encoder**. Unlike Bi-Encoders (which embed query and doc separately), a Cross-Encoder processes them together, allowing for much deeper interaction and higher precision at the cost of more computation.

## 6. Agent Orchestration & Tools
The Agent acts as the "conductor" of the system.

- **THINK-RETRIEVE-RESPOND**: This loop forces the model to deliberate.
  - **THINK**: Internal reasoning about the query.
  - **RETRIEVE**: Querying the knowledge base.
  - **TOOL CALL**: Using functions like the `Calculator`.
- **Tool Registry**: A modular system where new capabilities (like filesystem access or web search) can be added without modifying the core agent logic.
- **Heuristic Assistance**: For very small models (like our 3.2M parameter version), we use "guardrails" or heuristic routing to ensure tools are called correctly when the model's own reasoning might fail.

## 7. Memory System: STM & LTM
Memory allows for consistent, multi-turn interactions.

- **Short-Term Memory (STM)**: A simple list-based rolling window. It keeps the "immediate context" alive, allowing the user to say "Tell me more about *that*."
- **Long-Term Memory (LTM)**: Every interaction is embedded and stored in a separate ChromaDB collection. Before answering, the agent "searches its own past" to find relevant previous discussions.

## 8. API & Engineering Standards
The system is served via **FastAPI** to make it accessible and production-ready.

- **Singleton Components**: Models are loaded once at startup to avoid expensive reloading.
- **Pydantic Validation**: All API inputs and outputs are strictly typed and validated, preventing runtime errors from malformed data.
- **Structured Logging**: We use `structlog` to produce machine-readable (JSON) and human-friendly logs, making it easy to trace an agent's "thought process" through the system.
- **Environment**: Managed by `uv`, ensuring reproducible builds and fast dependency resolution.

## 9. Future Directions
- **Model Scaling**: Moving from 3M to 100M+ parameters.
- **Quantization**: Implementing 4-bit/8-bit weights for efficiency.
- **Graph Retrieval**: Moving from flat documents to structured Knowledge Graphs.
- **Multi-Modal**: Adding support for image or audio inputs.

## 10. ChromaDB Deep Dive

### 10.1 Markdown Ingestion
To bridge the gap between human-readable documentation and machine-processable context, we implemented a dedicated markdown ingestion utility.

- **`ai_system/app/utils/markdown_parser.py`**: This utility handles the extraction of clean text from markdown files. It performs normalization by removing:
  - Image links (`![]()`)
  - Raw markdown link labels (`[]()`)
  - Markdown headers (`#`)
  - Code block markers (```)
- **Indexing Workflow**: Once cleaned, the text is passed to the `RetrievalManager`. The script `ai_system/scripts/index_js_docs.py` provides the standard workflow:
  1. Recursively walk the directory tree from the source path, ignoring hidden system files (e.g., `._*` macOS resource forks).
  2. Normalize content via `clean_markdown` while handling potential encoding issues robustly.
  3. Extract document content and metadata.
  4. Index into the Hybrid Retrieval system (Dense + Sparse), with granular, per-document progress reporting and batch-optimized ChromaDB operations.
- **Rationale**: Markdown files are highly structured. Removing syntax markers helps reduce "noise" during embedding, leading to higher-quality retrieval results while preserving the semantic structure of technical documentation.

### 10.2 Indexing Process Deep Dive
When the RetrievalManager indexes a document, it performs two critical technical operations for each piece of content:

- **1. Embedding Generation (Semantic Mapping)**: The system sends the cleaned text to the **SentenceTransformer** model (e.g., `all-MiniLM-L6-v2`). The model converts the text into a 384-dimensional vector—a mathematical representation of the document's meaning. Documents with similar concepts end up closer together in this high-dimensional space, enabling semantic search.
- **2. Database Insertion (Storage & Indexing)**: The resulting vector is stored in a **ChromaDB** collection. ChromaDB manages:
  - **Vector Storage**: Uses an HNSW (Hierarchical Navigable Small World) index to enable fast similarity lookups.
  - **Metadata Storage**: Keeps the original text and file path associated with the vector so that, after a search, the system can return the actual content instead of just its mathematical ID.

While the script provides granular status updates for each document, the operations are batch-optimized for performance, writing data to the database in efficient chunks.

### 10.3 ChromaDB Index Anatomy
When you look into the ChromaDB storage folder, you will find files associated with the HNSW (Hierarchical Navigable Small World) index. Here is what they do:

- **`data_level0.bin`**: This is the primary storage for the actual vector data at the base level of the HNSW graph. It contains the coordinate information for your embedded documents.
- **`header.bin`**: Contains metadata about the index structure itself, such as the versioning and configuration parameters used during construction.
- **`index_metadata.pickle`**: A serialized Python object storing high-level information about the collection, including indexing parameters (like `M` and `ef_construction`) and mappings for the graph.
- **`length.bin`**: Stores the lengths of the vectors or the number of entries in the index, which helps the system allocate memory efficiently during searches.
- **`link_lists.bin`**: The core of the HNSW graph. It stores the "links" (edges) between vectors, allowing the search algorithm to jump quickly across the graph to find nearest neighbors.

**Why it matters**: Understanding these files helps you appreciate the complexity of the "vector space" your system is navigating. When searching, the system traverses `link_lists.bin` to navigate the graph and then retrieves the actual vector data from `data_level0.bin` to perform the final similarity calculation.

### 10.4 ChromaDB Storage Split (Text vs. Vectors)
ChromaDB uses a split-storage architecture to optimize for both search performance and data integrity:

- **`chroma.sqlite3` (The Metadata/Content Store)**: This is a standard relational database that acts as the "Source of Truth." It holds your original markdown text, file paths (metadata), and document IDs. When you view a document in the browser, the tool queries this SQLite database by ID to fetch the content.
- **The Binary Index Folder (The Vector Store)**: The hexadecimal-named folders contain the HNSW index files (e.g., `data_level0.bin`, `link_lists.bin`). These hold only the 384-dimensional floating-point vectors. The index does *not* store your text; it only stores mathematical representations of meaning.

**Why this matters**: This separation allows the HNSW index to remain highly compact and optimized for high-speed mathematical operations, while keeping your actual text data safe and easily queryable in a reliable, ACID-compliant SQLite database.

### 10.5 Database Troubleshooting & Best Practices
Indexing is a resource-intensive operation that involves writes to both SQLite metadata and HNSW vector index files. 

- **Avoid Interruptions**: Do not terminate (`Ctrl+C`) the indexing process while it is in progress. Interruption can leave the database in a partially written or inconsistent state, leading to "Failed to load records" errors when trying to browse or query the data.
- **Resolution**: If your database becomes corrupted or inconsistent:
  1. Remove the existing database directory (e.g., `rm -rf ai_system/data/embeddings/chroma`).
  2. Restart the indexing process from start to finish without interruption.
- **Verification**: Always wait for the "Indexing complete" confirmation before attempting to use or browse the collection.

### 10.6 Chroma Browser Tool
We have implemented a custom, project-integrated terminal browser (`ai_system/data/chroma_browser.py`) to replace the generic `chroma-cli`. This tool provides:
- **Rich Visualization**: Uses the `rich` library to render tables, panels, and styled output.
- **Interactive Browsing**: Supports pagination and detailed document views.
- **Integrated Semantic Search**: Allows you to test your embeddings directly within the browser tool.
- **No Dependencies on External CLI**: It runs entirely within your project's Python environment.

## 11. Training Execution and Monitoring

The training process for the `TinyTransformer` is orchestrated by the `ai_system.app.training.trainer` module. Execution is straightforward:

```bash
python3 -m ai_system.app.training.trainer | tee ai_system/logs/training_$(date +%Y%m%d_%H%M%S).log
```

### What to Expect During Training

*   **Loss Monitoring**: The training script outputs the current loss to the console/log every 10 iterations. Your primary goal is to see this value trending consistently downward. A stable, decreasing loss indicates the model is learning to predict the next token more accurately.
*   **Validation Intervals**: Every 500 iterations (the `eval_interval`), the model pauses training to evaluate itself on a held-out validation dataset. It prints the "val loss" to the console.
*   **Persistence**: If the evaluation finds that the current model has a lower validation loss than any previously encountered, it will automatically save a checkpoint to `models/checkpoints/ckpt_best.pt`.
*   **Post-Training Usage**: Once the `ckpt_best.pt` file is generated, the API server will be able to load it at startup, enabling the system to generate coherent, model-driven responses.

### Critical Warning: Monitoring for Overfitting

Because the system currently relies on `sample_corpus.txt`, which is relatively small, you must watch for signs of **overfitting**. 

- **The Symptom**: Your training loss continues to trend downward (the model is learning the training data perfectly), but your validation loss plateaus or begins to trend *upward*.
- **The Meaning**: The model is "memorizing" the exact sequences in the training set rather than learning general language patterns.

### Terminating Unstable Runs
If you notice extreme instability—such as the loss oscillating wildly, spiking dramatically, or appearing as `NaN` (Not a Number)—**it is perfectly safe to terminate the training session** (using `Ctrl+C`). 

- **Why?**: Terminating is the professional engineering decision. It prevents wasting compute resources on a failing run and ensures your logs/TensorBoard history aren't polluted with unusable, noisy data.
- **Risk Mitigation**: The only risk of immediate termination is a partially written checkpoint file (`ckpt_best.pt`). If you are concerned about corrupting a previously saved checkpoint, keep periodic backups of your `models/checkpoints/` directory.
- **Next Steps**: Always analyze the final log entries to identify the cause (e.g., gradient explosion) before restarting with adjusted hyperparameters (e.g., lower learning rate, enabled gradient clipping).

*Last Updated: Monday, May 18, 2026*
