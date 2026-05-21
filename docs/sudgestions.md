# Project Suggestions

## 2026-05-17

- **JavaScript Assistance**:
  - Implement a `JSExecutor` tool using `node -e` for real-time validation of JS code snippets.
  - Add a specialized "Code Formatter" tool (e.g., using `prettier`) to help the assistant output cleaner JS code.
  - Create a "Snippet Library" in the retrieval system with common JS patterns and best practices.

- **Environment Management**:
  - Add a `.python-version` file to the root and `ai_system/` to help tools like `uv` and `pyenv` auto-select the right version.
  - Create a simple `Makefile` or `justfile` in the root to automate common tasks like `install`, `test`, `run-api`, etc., ensuring they always use the correct venv.
  - Consider using `uv workspace` if the project grows to include multiple sub-packages.

- **API & Deployment**:
  - Implement authentication (e.g., API keys) for the endpoints.
  - Add request rate limiting to prevent abuse.
  - Create a Dockerfile for easy containerization and deployment.

- **Memory Enhancements**:
  - Implement "Memory Consolidation": Periodically summarize short-term history into long-term memories to save space.
  - Add "Forgetting": Implement a decay factor or explicit deletion mechanism for outdated memories.

- **Agent Orchestration**:
  - Implement a more robust "Planning" stage where the agent lists all required tools before execution.
  - Add an "Environment" tool that allows the agent to see its own current state (e.g., current time, OS, available memory).
  - Use structured output (e.g., XML or JSON tags) to help the parser extract tool calls from the model's response.

- **Retrieval Enhancements**:
  - Implement dynamic weighting for hybrid search based on query intent (e.g., keyword-heavy vs. conceptual).
  - Add support for different chunking strategies (e.g., sliding window, semantic chunking) in the indexing phase.
  - Integrate metadata filtering (e.g., filter by source or date) into the `RetrievalManager`.

- **Inference Enhancements**:
  - Implement beam search or contrastive search for better generation quality.
  - Add support for batch inference to process multiple prompts simultaneously.
  - Create a simple CLI wrapper for the generator to interact with the model directly from the terminal.

- **Training Enhancements**:
  - Implement mixed precision (AMP) if moving to GPU training.
  - Add data augmentation or more complex chunking strategies for larger datasets.
  - Integrate a progress bar (e.g., `tqdm`) for better CLI feedback during long training runs.

- **Environment & Compatibility**:
  - Keep a record of "known good" library versions for this specific CPU environment (Ubuntu 24.04 headless with 2 cores).
  - The "Illegal instruction" error was resolved by ensuring `numpy < 2.0.0` and using `torch+cpu` specific wheels.
  - Future environment setups should use a `requirements.txt` generated from the current working state to avoid regression.

- **Model Enhancements**:
  - Implement Flash Attention (if supported by environment) for better performance.
  - Add support for different positional embedding types (e.g., RoPE).
  - Create a visualization script for attention maps to help understanding.

- **Tokenizer Improvements**:
  - Consider a larger corpus for the final tokenizer training (e.g., Wikipedia or OpenWebText subset).
  - Add a CLI interface to `trainer.py` for easier configuration without editing code.
  - Implement a validation step in `processor.py` to check model integrity on load.

## [2026-05-17] Phase 2: Tokenizer & Model Prototype

1. **Implement SentencePiece Tokenizer:** Create `ai_system/app/tokenizer/trainer.py` to train on a sample corpus and `ai_system/app/tokenizer/processor.py` for encoding/decoding.
2. **Download/Prepare Sample Data:** Place a small text dataset (e.g., TinyShakespeare or similar) in `ai_system/data/raw/` for tokenizer training.
3. **Core Model Definition:** Implement the `TinyTransformer` class in `ai_system/app/llm/model.py` using the parameters specified in `GEMINI.md` (4 layers, 4 heads, 256 dim).
4. **Configuration System:** Implement `ai_system/app/config/config.py` using `pyyaml` to manage model and training hyperparameters.

## My Note
