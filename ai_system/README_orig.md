# myTinyGPT

A modular, local AI system featuring a tiny GPT-style transformer and an Agentic Hybrid Retrieval system.

## Project Structure
- `app/`: Core logic (LLM, Retrieval, Agent, etc.)
- `data/`: Storage for raw and processed data
- `models/`: Saved model checkpoints
- `scripts/`: Utility scripts for training and data prep
- `tests/`: Unit and integration tests

## Tech Stack
- **ML**: PyTorch
- **Tokenizer**: SentencePiece
- **Vector DB**: ChromaDB
- **Retrieval**: BM25 + Dense Embeddings
- **API**: FastAPI
- **Environment**: uv
