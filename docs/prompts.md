## [2026-05-19]
**User:** Fixed plotting crash in `trainer.py` by switching to `matplotlib.pyplot`.
**Context:** Resolution of `TypeError` caused by incorrect `plotext` usage.

# User Prompts

## [2026-05-19 12:20]
**User:** review the project and see what needs to be done for: System Prompt Leakage: The model is outputting its entire "System Prompt" (the internal instructions about how it should think and behave) instead of just the answer. This is a common symptom of a model that is either undertrained or failing to understand where the system prompt ends and its response begins.
**Context:** Investigation and resolution of internal prompt echoing in the tiny model.

## [2026-05-17]
**User:** create a new file docs/codeAssistant.md - in this file give detailed instructions on how to use the myTinyGPT as a javascript code assistant.
**Context:** Request for specialized documentation on using the system for JavaScript development.

## [2026-05-17]
**User:** i had you help build this project without the venv being activated. How can we fix this?
**Context:** Inquiry regarding correcting the development environment state after building without an active virtual environment.

## [2026-05-17]
**User:** update
**Context:** Request to synchronize and update project documentation files.

**User:** proceed with the Environment Setup and Directory Scaffolding
**Context:** Directive to implement the project structure and setup the Python environment.

**User:** create a new file docs/learning.md this file is for me to read later on the topics we are adding to the project. Initiate this file with a breif project discription, system info (this computer specifications, needed software with the current versions)
**Context:** Request for a knowledge-tracking document with system and project details.

**User:** proceed with the Tokenizer implementation
**Context:** Directive to implement the Tokenizer module, including training scripts and processing utilities using SentencePiece.

**User:** move on to the Tiny Transformer model implementation
**Context:** Directive to implement the core GPT-style transformer architecture as defined in the project requirements.

**User:** proceed with Training Loop implementation
**Context:** Directive to implement the training pipeline, including data loading, optimization, and logging.

**User:** proceed with the Inference stage
**Context:** Directive to implement the inference utility to load checkpoints and generate text.

**User:** proceed to the Hybrid Retrieval System implementation, starting with Dense Retrieval
**Context:** Directive to implement the multi-stage hybrid retrieval system (Dense, Sparse, Hybrid Merge, Reranking).

**User:** proceed with the Agent Loop and Orchestration Layer implementation
**Context:** Directive to implement the agentic reasoning loop, tool registry, and overall system orchestration.

**User:** update
**Context:** Request to synchronize and update all documentation files (history, prompts, suggestions, learning).

**User:** update
**Context:** Final synchronization check for all project documentation.

**User:** update
**Context:** Verification of the documentation status after the Agent Orchestration phase.

**User:** Memory System implementation or the FastAPI Inference Server - go
**Context:** Directive to implement the final core components (Memory and API Server).

**User:** in docs - write a HowToUse.md file detailing how to use the system, how to test the system, how to add my own data for use, other ideas and further improvments.
**Context:** Request for a user-facing guide and future development roadmap.
