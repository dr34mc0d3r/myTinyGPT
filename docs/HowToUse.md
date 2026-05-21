# How To Use myTinyGPT

Welcome to the **myTinyGPT** user guide. This document provides step-by-step instructions on how to operate, test, and extend your local AI system.

---

## 1. Environment Setup

The system uses `uv` for package management. Ensure you are in the `ai_system` directory.

```bash
cd ai_system
source .venv/bin/activate
```

## 2. Running the API Server

The primary way to interact with the system is via the FastAPI server. Run this from your project root (~/DEV/myTinyGPT):

```bash
python3 -m ai_system.app.api.main
```

The server will start at `http://localhost:8000`.

## 3. How to Test the System

### Manual Testing with Curl

You can test the server using `curl` from another terminal:

```bash
# Health Check
curl -s http://localhost:8000/health

# Chat with Agent
curl -s -X POST http://localhost:8000/chat
     -H "Content-Type: application/json"
     -d '{"query": "What is transformer architecture?"}'

# Formatted example
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"query": "show me a fetch example."}'

# Test Math Tool
curl -s -X POST http://localhost:8000/chat
     -H "Content-Type: application/json"
     -d '{"query": "Calculate 150 / 3"}'
```

## 4. How to Add Your Own Data

The system uses a **Hybrid Retrieval** system. To add your own knowledge:

### Method 1: Direct Indexing

You can use the `RetrievalManager` to index text documents:

1. Create a script or use the `app/retrieval/manager.py` test block.
2. Call `manager.index_documents(documents, ids, metadatas)`.

```python
from app.retrieval.manager import RetrievalManager

manager = RetrievalManager()
my_docs = ["My custom technical document content..."]
my_ids = ["doc_custom_1"]
manager.index_documents(my_docs, my_ids)
```

### Method 2: Data Folder

Place your raw text files in `ai_system/data/raw/`. You can then write a simple script to read these files and pass them to the `RetrievalManager`.

## 5. Training the Model

If you want to train the Tiny Transformer on a new dataset:

1. Prepare your text data in a single `.txt` file (e.g., `ai_system/data/raw/my_data.txt`).
2. **Re-train the Tokenizer**:
   - _When to do this_: If your new data contains many specialized terms, symbols, or a different language not represented in the existing `tokenizer.model`.
   - _Why_: A custom tokenizer ensures your data is broken into the most meaningful sub-word units, drastically improving model performance.
   ```bash
   python3 -m ai_system.app.tokenizer.trainer
   ```
3. Run the training loop from your project root:
   ```bash
   python3 -m ai_system.app.training.trainer
   ```
   Checkpoints will be saved

## 6. Ideas and Further Improvements

### Architectural Ideas

- **Multi-Agent Systems**: Split the agent into a "Manager" and "Specialists" (e.g., a "Math Specialist" and a "Coder Specialist").
- **External Tools**: Add a `WebSearchTool` (using an API like Serper) or a `PythonExecTool` for complex logic.
- **Quantization**: Implement 8-bit or 4-bit quantization to run larger models on even smaller hardware.

### UI Improvements

- **Web Interface**: Build a simple React or Streamlit frontend to chat with the API.
- **Streaming**: Update the API to support Server-Sent Events (SSE) for real-time token streaming.

### Memory & Learning

- **Memory Summarization**: Have the agent summarize long conversations periodically to fit more into the "Long-Term Memory" without hitting context limits.
- **RLHF (Reinforcement Learning from Human Feedback)**: Implement a simple "Thumbs Up/Down" system in the API to collect data for future fine-tuning.

## 7. Troubleshooting

- **Illegal Instruction**: If you see this error, it means your CPU lacks certain AVX instructions. We have pinned `torch` and `numpy` to compatible versions, but ensure you are using the `.venv` environment.
- **Memory Errors**: The system is designed for low-resource environments, but training requires at least 4GB of RAM. If you hit OOM, reduce the `batch_size` in `app/config/config.py`.

## 8. Managing Long-Running Processes with TMux

For resource-heavy tasks like indexing embeddings or training transformers, use **TMux**. It keeps your processes alive even if your SSH session disconnects or your terminal closes.

### Quick-Start Workflow

1. **Create Session**: `tmux new -s ai_indexer`
2. **Activate Environment**: `source ai_system/.venv/bin/activate`
3. **Run with Logging**:
   ```bash
   python3 ai_system/scripts/index_js_docs.py | tee ai_system/logs/indexing_$(date +%Y%m%d_%H%M%S).log
   ```
4. **Detach (Safely)**: Press `CTRL+A`, then `D`.
5. **Reconnect Anytime**: `tmux attach -t ai_indexer`

### Useful TMux Commands

- **List Sessions**: `tmux ls`
- **Split Pane (Horizontally)**: `CTRL+A` then `"`
- **Split Pane (Vertically)**: `CTRL+A` then `%`
- **Switch Windows**: `CTRL+A` then `N` (next) or `P` (previous)
- **Kill Session**: `tmux kill-session -t ai_indexer`

### Monitoring Performance

In a split pane, keep an eye on your system resources to monitor CPU/RAM usage:

- **CPU/RAM**: `htop`
- **GPU (if applicable)**: `nvtop`

_Pro-Tip: Using `tee indexing.log` allows you to monitor the live output while keeping a permanent record that you can check later with `tail -f indexing.log`._

## 9. Logging & Monitoring

To maintain auditability for long-running AI jobs (like indexing or training), we use a structured logging system.

### Centralized Logging Structure

All logs are stored in ai_system/logs/. This directory is configured to be ignored by Git to avoid bloat.

### Recommended Execution Pattern

Use the `tee` command to stream output to the terminal while saving to a log file:

```bash
python3 ai_system/scripts/index_js_docs.py | tee ai_system/logs/indexing_$(date +%Y%m%d_%H%M%S).log
```

### Pro-Tips:

- **Timestamped Logs**: Prevent overwriting old runs by using timestamps:
  ```bash
  # Run this command:
  python3 ai_system/scripts/index_js_docs.py | tee ai_system/logs/indexing_$(date +%Y%m%d_%H%M%S).log
  ```
- **Real-Time Monitoring**: Open a second terminal pane and watch the log as it happens:
  ```bash
  tail -f ai_system/logs/indexing.log
  ```
