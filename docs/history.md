## [2026-05-19] Training Plotting Crash Fix
- Fixed `TypeError: cannot unpack non-iterable _figure_class object` in `ai_system/app/training/trainer.py` by correctly using `plotext.subplot()` instead of the unsupported `subplots()` method for terminal plotting.
- **Diagnosed System Prompt Leakage:** Identified that the model was leaking internal instructions because `Generator.generate` returned the entire input+output sequence and the prompt exceeded the 256-token `block_size`.
- **Inference Logic Update:** Modified `ai_system/app/llm/inference.py` to return only newly generated tokens by slicing the output tensor.
- **Prompt Window Optimization:** Shortened the `AGENT_SYSTEM_PROMPT` in `ai_system/app/prompts/templates.py` and implemented context truncation in `AgentController` to stay within the 256-token limit.
- **Instruction Fine-Tuning Scaffolding:** Created `ai_system/data/raw/instruction_data.txt` and `fine_tune.py` to teach the model the THINK/RESPOND format and improve response quality.
- **Verification:** Confirmed via `reproduce_leakage.py` that the system prompt is no longer echoed in the final response.

## [2026-05-18] Configuration Variables Documentation
- Created `docs/config_variables.md`: An educational reference mapping the `ModelConfig` and `TrainingConfig` hyperparameters to their definitions and functional roles, organized to mirror the `ai_system/app/config/config.py` structure.

## [2026-05-18] Project Review & Structural Cleanup
- Performed a comprehensive review of the project directory structure.
- Removed a redundant nested `ai_system/ai_system` directory to prevent import shadowing and configuration ambiguity.
- Validated `docs/Step-by-StepSetupProcess.md` against actual codebase paths and entry points.
- Updated `ai_system/app/config/config.py` to ensure consistent checkpoint paths when running from the repository root.

## [2026-05-18] Setup & Lifecycle Documentation
- Created `docs/Step-by-StepSetupProcess.md`: A definitive guide for the myTinyGPT startup sequence, mapping generated file artifacts to each stage, and providing a rigorous procedure for performing a "fresh start" system reset.

## [2026-05-18] Expanded Terminology Glossary
- Updated `docs/terminology.md` to include an expanded, comprehensive alphabetical glossary of AI engineering and myTinyGPT-specific terms, integrating all requested technical concepts.

## [2026-05-18] Terminology Glossary
- Created `docs/terminology.md`: An alphabetical reference guide for core AI engineering and `myTinyGPT`-specific terminology, defining key concepts, use cases, and providing examples to aid intermediate developers.

## [2026-05-18] Post-Training Testing Documentation
- Created `docs/testing.md`: A structured guide detailing the post-training validation workflow for `myTinyGPT`, including step-by-step testing procedures, an improvement matrix for interpreting results, and best practices for automated testing.

## [2026-05-18] Training Stability Documentation
- Updated `docs/learning.md` with best practices for handling unstable training sessions, specifically emphasizing that terminating divergent runs is safe and recommended engineering practice.

## [2026-05-18] Expanded Loss Curve Analysis Manual
- Updated `docs/Loss_Curve_Analysis.md` by ingesting and structuring comprehensive training manual guidance on loss curve interpretation, diagnostics, and engineering workflows.

## [2026-05-18] Loss Curve Analysis Documentation
- Created `docs/Loss_Curve_Analysis.md`: A new educational resource detailing best practices for training log monitoring, including key concepts for debugging, recommended metrics to log, and links to definitive industry resources.

## [2026-05-18] System Data Flow Documentation
- Created `docs/data_flow.md`: A detailed architectural mapping of the user query lifecycle, including specific file paths, function roles, and the interaction flow between the API, Agent, Retrieval, Tool, and Inference layers.

## [2026-05-18] Internet Search Implementation Strategy
- Updated `docs/strong.md` with an architectural roadmap for adding internet search capabilities to myTinyGPT, including tool implementation, invocation logic, and agentic integration.




## [2026-05-17] JavaScript Code Assistant Documentation
- Created `docs/codeAssistant.md`: A detailed guide on using myTinyGPT for JavaScript development.
- Included instructions for knowledge base setup, agentic workflows, and API integration for JS tasks.
- Suggested advanced extensions like a `JSExecutor` tool.

## [2026-05-17] Environment Fix & Cleanup
- Identified and removed redundant virtual environment artifacts (`bin/`, `lib/`, `lib64/`, `pyvenv.cfg`) from the repository root.
- Re-synchronized the `ai_system/.venv` environment using `uv`.
- Verified the project is correctly installed in editable mode within the intended virtual environment.
- Documented the environment fix and updated project logs.

## [2026-05-17] Final Documentation & Completion
- Created `docs/HowToUse.md`: A comprehensive guide covering setup, API usage, testing, data management, and training.
- Finalized project structure and verified all core components are documented.

## [2026-05-17] API Server & Memory System Implementation
- Implemented `ai_system/app/memory/`:
  - `short_term.py`: Rolling window conversation history.
  - `long_term.py`: Persistent vector memory using ChromaDB.
  - `manager.py`: Unified memory interface for the agent.
- Implemented `ai_system/app/api/main.py`: FastAPI server with `/chat`, `/health`, and `/retrieve` endpoints.
- Integrated the full stack: Tokenizer + Transformer + Hybrid Retrieval + Agent Loop + Tools + Memory + FastAPI.
- Verified the system via API calls, confirming end-to-end functionality.

## [2026-05-17] Agent Orchestration Implementation
- Implemented `ai_system/app/tools/`: Base tool class, tool registry, and a `CalculatorTool`.
- Implemented `ai_system/app/prompts/templates.py`: Structured system prompt for THINK-RETRIEVE-RESPOND loop.
- Implemented `ai_system/app/agent/controller.py`: `AgentController` to orchestrate retrieval, tool execution, and LLM generation.
- Verified agent loop logic: Retrieval and tool calls are correctly triggered and logged.
- Observed that the 3.2M model requires significant training to follow complex agentic instructions.

## [2026-05-17] Hybrid Retrieval System Implementation
- Implemented `ai_system/app/retrieval/dense.py`: Dense vector retrieval using `ChromaDB` and `SentenceTransformers` (`all-MiniLM-L6-v2`).
- Implemented `ai_system/app/retrieval/sparse.py`: Sparse keyword retrieval using `rank-bm25`.
- Implemented `ai_system/app/retrieval/hybrid.py`: Score normalization and weighted fusion of dense and sparse results.
- Implemented `ai_system/app/retrieval/reranker.py`: Fine-grained relevance scoring using a Cross-Encoder model (`ms-marco-MiniLM-L-6-v2`).
- Implemented `ai_system/app/retrieval/manager.py`: Unified `RetrievalManager` and `ContextBuilder` for full-pipeline orchestration and prompt formatting.
- Verified end-to-end retrieval with semantic queries and technical keywords.

## [2026-05-17] Inference Stage Implementation
- Implemented `ai_system/app/llm/inference.py` featuring a `Generator` class.
- Supported loading model state and architecture configuration from training checkpoints.
- Implemented high-level `generate` method for end-to-end text generation from string prompts.
- Resolved `torch.load` security restrictions regarding custom class deserialization (`weights_only=False`).
- Verified inference pipeline with the test checkpoint.

## [2026-05-17] Training Loop Implementation
- Implemented `ai_system/app/training/dataset.py` for chunking tokenized text into training samples.
- Implemented `ai_system/app/training/trainer.py` with:
  - AdamW optimizer.
  - Cosine learning rate decay with linear warmup.
  - TensorBoard integration for loss and LR tracking.
  - Evaluation loop and model checkpointing (best and periodic).
- Verified training functionality with a 50-iteration test run on CPU.

## [2026-05-17] Tiny Transformer Implementation
- Implemented `ai_system/app/config/config.py` for model and training hyperparameters using YAML.
- Implemented `ai_system/app/llm/model.py` with:
  - Token and Positional Embeddings.
  - Causal Self-Attention with multi-head support.
  - Transformer Blocks with LayerNorm and MLP (GELU).
  - Weight sharing between embeddings and output head.
  - Autoregressive `generate` method with temperature and top-k sampling.
- Verified model initialization (~3.2M parameters) and basic generation functionality.
- Resolved environment compatibility issues by ensuring AVX-compatible libraries (PyTorch 2.12.0+cpu, NumPy 1.26.4).

## [2026-05-17] Tokenizer Implementation
- Created `ai_system/data/raw/sample_corpus.txt` for initial training.
- Implemented `ai_system/app/tokenizer/trainer.py` using SentencePiece.
- Implemented `ai_system/app/tokenizer/processor.py` for encoding/decoding.
- Verified training and processing with a 100-vocab test run.
- Tokenizer supports special tokens: [PAD], [UNK], [BOS], [EOS], [SEP], [MASK].

## [2026-05-17] Environment Setup & Scaffolding
- Created directory structure under `ai_system/` following `GEMINI.md` specifications.
- Initialized `pyproject.toml`, `README.md`, and `.env`.
- Set up `uv` virtual environment in `ai_system/.venv`.
- Installed core dependencies: PyTorch, SentencePiece, sentence-transformers, ChromaDB, rank-bm25, FastAPI, etc.
- Verified editable install of the `mytinygpt` package.
- Created `docs/learning.md` to track project concepts and system specifications.
