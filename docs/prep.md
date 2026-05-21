# Preparing myTinyGPT for a New Knowledge Domain

This guide explains how to prepare `myTinyGPT` for any distinct knowledge domain, from collecting domain content to indexing, tokenizer preparation, training, fine-tuning, and testing. It is built from the current repository structure and the available scripts.

---

## 1. Workspace and Environment

1. Open the repository root:
   ```bash
   cd /home/chris/DEV/myTinyGPT
   ```
2. Activate the Python virtual environment:
   ```bash
   source ai_system/.venv/bin/activate
   ```

> Most commands in this guide assume you are in the repository root with the `ai_system` venv activated.

---

## 2. Domain Content: What to Prepare

### 2.1 Distinct Knowledge Domains

Create a separate raw-data folder for each domain under `ai_system/data/raw/`.

Examples:

- `ai_system/data/raw/javascript_docs/`
- `ai_system/data/raw/gardening_docs/`
- `ai_system/data/raw/finance_docs/`
- `ai_system/data/raw/medical_docs/`

### 2.2 File Types

The system can ingest:

- Markdown files (`.md`) for documentation, tutorials, and guides
- Plain text files (`.txt`) for training corpora

### 2.3 Example Corpus Layout

For a gardening domain, use:

```text
ai_system/data/raw/gardening_docs/plant-care.md
ai_system/data/raw/gardening_docs/soil-types.md
ai_system/data/raw/gardening_docs/pruning-guide.md
```

Example file content for `plant-care.md`:

```markdown
# Plant Care Basics

Indoor plants need regular watering, good drainage, and indirect sunlight.

## Watering

- Check soil moisture with your finger.
- Water only when the top 2cm of soil is dry.

## Fertilizer

- Use a balanced fertilizer every 4-6 weeks during the growing season.
```

#### What this corpus folder is for

The files under `ai_system/data/raw/<domain>_docs/` are the source documents that the retrieval system reads and indexes. During indexing, the markdown parser cleans and splits this text, then the retrieval manager creates embeddings and stores them in ChromaDB. Those documents are later searched at runtime to provide relevant domain-specific passages to the agent.

The corpus folder is not the same as the model training corpus. It is primarily used for retrieval and knowledge lookup, meaning the model can answer questions by referencing the indexed source material rather than having memorized it.

#### How this file is used in the system

- `ai_system/app/utils/markdown_parser.py` loads and cleans markdown files from the raw folder.
- `ai_system/app/retrieval/manager.py` receives the cleaned text and builds the dense/sparse index.
- `ai_system/data/embeddings/chroma/` stores the persistent vector index created from these files.
- At query time, retrieval components search this index and return passages to the agent prompt.

This means your raw markdown files are the knowledge base that retrieval depends on, so keep them structured, clear, and focused on the new domain.

### 2.4 Distinct Corpus for Model Training

If you want to train or fine-tune the model on domain-specific language, prepare a raw text corpus file:

```text
ai_system/data/raw/my_gardening_corpus.txt
```

This should be a single text file or a few large text files with raw domain content.

Example corpus content:

```text
Roses perform best in well-drained soil with a pH of 6.0 to 6.5.
A balanced fertilizer supports leaf growth and flowering.
Pruning in early spring encourages stronger stems.
```

---

## 3. Tokenizer Preparation

The tokenizer used by `myTinyGPT` is SentencePiece. A custom tokenizer helps if your domain includes many new terms, symbols, or syntax.

### 3.1 When to re-train the tokenizer

Re-train when your domain is:

- a new formal language or syntax (code, math, chemical formulas)
- a new language or jargon-heavy field
- very different from the existing model’s vocabulary

Do not re-train if you are only adding general-domain content like new blog posts or articles in normal English.

### 3.2 How to train the tokenizer

The tokenizer trainer lives in `ai_system/app/tokenizer/trainer.py`.

Example command:

```bash
python3 -m ai_system.app.tokenizer.trainer
```

This script currently trains on the default sample corpus at:

- `ai_system/data/raw/sample_corpus.txt`

and writes tokenizer files to:

- `ai_system/models/tokenizer/tokenizer.model`
- `ai_system/models/tokenizer/tokenizer.vocab`

The `.model` file is the SentencePiece binary tokenizer, and the `.vocab` file contains the vocabulary entries and token scores.

For a custom domain, update or extend the `TokenizerTrainer` call in `ai_system/app/tokenizer/trainer.py` with your input files:

```python
from ai_system.app.tokenizer.trainer import TokenizerTrainer

trainer = TokenizerTrainer(vocab_size=8000)
trainer.train(["ai_system/data/raw/my_gardening_corpus.txt"], "ai_system/models/tokenizer")
```

### 3.3 Verify tokenizer availability

The model loader expects:

- `ai_system/models/tokenizer/tokenizer.model`

If the tokenizer is in a different path, update the path in `ai_system/app/tokenizer/processor.py` or pass the correct path to the relevant loader.

---

## 4. Data Indexing for Retrieval

The retrieval system uses hybrid search: dense semantic retrieval plus sparse BM25 keyword retrieval.

### 4.1 Existing indexing script

The repo includes one indexing script for JavaScript docs:

- `ai_system/scripts/index_js_docs.py`

It currently indexes files from:

- `ai_system/data/raw/javascript_docs/`

### 4.2 Using the script for another domain

To index a new domain, copy or adapt the existing script:

- set `docs_path` to your domain folder, e.g. `ai_system/data/raw/gardening_docs/`
- optionally update any collection or metadata logic

Example adaptation:

```python
from ai_system.app.retrieval.manager import RetrievalManager
from ai_system.app.utils.markdown_parser import load_markdown_files

manager = RetrievalManager()
markdown_docs = load_markdown_files("ai_system/data/raw/gardening_docs/")
contents = [doc["content"] for doc in markdown_docs]
ids = [doc["id"] for doc in markdown_docs]
metadatas = [doc["metadata"] for doc in markdown_docs]
manager.index_documents(contents, ids, metadatas=metadatas)
```

### 4.3 Indexing command example

From the repo root:

```bash
python3 ai_system/scripts/index_js_docs.py
```

> Note: this script prompts before clearing the existing ChromaDB store at `ai_system/data/embeddings/chroma`.

### 4.4 Where the index is stored

- Vector store: `ai_system/data/embeddings/chroma`
- Sparse index: internal to the `SparseRetriever` component

### 4.4.1 What the index files contain

- `ai_system/data/embeddings/chroma/` contains ChromaDB persistent data for the dense vector index, including the stored embeddings, document IDs, and metadata needed for retrieval.
- The sparse index is managed by `SparseRetriever`; it may keep its own state in memory or save supporting data structures in the retrieval subsystem, but the main persisted retrieval artifacts are the ChromaDB files.

### 4.5 Clean markdown before indexing

The parser removes markdown noise and preserves text structure. Always keep the input files in plain readable markdown rather than binary formats.

---

## 5. Model Training vs Fine-Tuning

### 5.1 Training the main model

The main training pipeline is in:

- `ai_system/app/training/trainer.py`

From the repository root, run:

```bash
python3 -m ai_system.app.training.trainer
```

This will:

- build the `TinyTransformer` model
- load the tokenizer
- create a training dataloader from `ai_system/data/raw/sample_corpus.txt` or your custom data
- execute training loops with gradient updates
- save checkpoints to `ai_system/models/checkpoints/`

#### Checkpoint files created by training

Training writes checkpoint artifacts under `ai_system/models/checkpoints/`.
Common files include:

- `ai_system/models/checkpoints/ckpt_best.pt`
- `ai_system/models/checkpoints/ckpt_iter_<n>.pt`

Each checkpoint file contains:

- `model`: the model weights
- `optimizer`: the optimizer state
- `model_config`: the model configuration
- `training_config`: the training hyperparameters
- `iter`: the iteration number
- `loss`: the loss value at save time

### 5.2 Fine-tuning a pre-trained checkpoint

The repo includes a fine-tune helper:

- `ai_system/scripts/fine_tune.py`

This script:

- loads `ai_system/models/checkpoints/ckpt_best.pt` if available
- modifies training hyperparameters for fine-tuning
- runs the `Trainer` on new instruction data
- saves a final fine-tuned checkpoint

#### Fine-tune checkpoint artifacts

Fine-tuning writes artifacts to `ai_system/models/checkpoints/`, often including:

- `ai_system/models/checkpoints/ckpt_fine_tuned.pt`
- `ai_system/models/checkpoints/ckpt_best.pt` (if the fine-tune run produces a new best model)

These files contain the same structured checkpoint contents as standard training checkpoints.

Run it from the repo root:

```bash
python3 ai_system/scripts/fine_tune.py
```

### 5.3 If you only want retrieval for a new domain

You do not need to retrain the model. Add the domain content as retrieval documents and index them. Fine-tuning is only required if you want the model itself to learn domain-specific language patterns.

---

## 6. Preparing Training Data

### 6.1 Domain-specific training corpus

Create a raw text file under `ai_system/data/raw/` such as:

- `ai_system/data/raw/gardening_corpus.txt`
- `ai_system/data/raw/finance_corpus.txt`

This file should contain clean domain text without markdown formatting in the main training corpus.

Example:

```text
Succulents prefer bright light and infrequent watering.
A balanced fertilizer should be used in early spring.
Organic mulch helps retain soil moisture and suppress weeds.
```

### 6.2 Training dataset loader

`ai_system/app/training/dataset.py` converts text into token windows for training. It uses the tokenizer to encode the entire file and slices it into overlapping blocks of `block_size` tokens.

### 6.3 Recommended training flow

1. Prepare tokenizer (if needed).
2. Prepare training corpus text.
3. Run training.
4. Monitor validation loss and save checkpoints.

---

## 7. Testing and Validation

### 7.1 Basic inference test

Load the model checkpoint and run a quick example with `ai_system/app/llm/inference.py`.

Example script:

```python
from ai_system.app.llm.inference import Generator

gen = Generator(checkpoint_path="ai_system/models/checkpoints/ckpt_best.pt")
print(gen.generate("What is the best way to prune roses?", max_new_tokens=50))
```

### 7.2 API test

Start the API and send a chat request:

```bash
python3 -m ai_system.app.api.main
```

Then issue a POST request:

```bash
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the best fertilizer for indoor plants?"}'
```

### 7.3 Domain retrieval verification

Verify that retrieval is finding your new domain content. If your query uses domain terms and the response is not relevant, re-index the documents and confirm the parser cleaned them correctly.

### 7.4 Post-training validation

Use the repository’s testing guidance in `docs/testing.md` for a structured validation workflow.

---

## 8. Recommended Workflow for a New Domain

1. **Create the domain folder**
   - `ai_system/data/raw/<domain>_docs/`
2. **Add markdown files**
   - `ai_system/data/raw/<domain>_docs/topic1.md`
   - `ai_system/data/raw/<domain>_docs/topic2.md`
   - `ai_system/data/raw/<domain>_docs/faq.md`
3. **Optionally create a raw text corpus**
   - `ai_system/data/raw/<domain>_corpus.txt`
4. **Decide on tokenizer retraining**
   - If domain vocabulary is special, retrain SentencePiece
5. **Run indexing**
   - Modify `ai_system/scripts/index_js_docs.py` to point to `ai_system/data/raw/<domain>_docs/` and run it
6. **Train or fine-tune if needed**
   - `python3 -m ai_system.app.training.trainer`
   - or `python3 ai_system/scripts/fine_tune.py`
7. **Test retrieval and inference**
   - use `Generator` from `ai_system/app/llm/inference.py` and the API endpoint
8. **Iterate**
   - update documents, re-index, and evolve prompts as domain needs change

---

## 9. Notes on Multi-Domain Support

The current repository provides a single indexing script for JavaScript docs, but the architecture supports multiple domains.

- Keep each domain in its own `ai_system/data/raw/<domain>_docs/` folder.
- Store indices in `ai_system/data/embeddings/chroma`.
- To support separate ChromaDB collections per domain, follow the plan in `docs/diversity.md` and extend `RetrievalManager` to accept a collection name.

---

## 10. Useful Paths and Files

- Raw data root: `ai_system/data/raw/`
- Tokenizer model: `ai_system/models/tokenizer/tokenizer.model`
- Model checkpoints: `ai_system/models/checkpoints/`
- JavaScript indexing script: `ai_system/scripts/index_js_docs.py`
- Training loop: `ai_system/app/training/trainer.py`
- Fine-tuning helper: `ai_system/scripts/fine_tune.py`
- Inference utility: `ai_system/app/llm/inference.py`
- Retrieval orchestrator: `ai_system/app/retrieval/manager.py`
- Markdown parser: `ai_system/app/utils/markdown_parser.py`

---

## 11. When to Use Retrieval vs Training

- **Use retrieval only** when the domain is a knowledge base you want the agent to refer to, but the model itself does not need to internalize the language.
- **Use training/fine-tuning** when you want the model to learn domain-specific phrasing, style, or terminology directly.
- **Use both** if you need a robust system: retrieval for the facts, training for natural domain fluency.

---

## 12. Quick Example: Adding a Gardening Domain

1. Create files:
   - `ai_system/data/raw/gardening_docs/plant-care.md`
   - `ai_system/data/raw/gardening_docs/soil-types.md`
2. Prepare corpus:
   - `ai_system/data/raw/gardening_corpus.txt`
3. (Optional) retrain tokenizer if the domain is jargon-rich.
4. Update or duplicate `ai_system/scripts/index_js_docs.py` to point to `ai_system/data/raw/gardening_docs/`.
5. Run indexing.
6. Run training or fine-tuning if you want model-level domain knowledge.
7. Start the API and verify responses.

---

## 13. Troubleshooting

- If indexing fails, verify the raw files are readable and not hidden system files.
- If retrieval returns unrelated content, re-index and confirm the cleaned text looks correct.
- If training diverges, reduce `batch_size` or learning rate in the config.
- If inference cannot load the tokenizer, confirm `tokenizer.model` exists at `ai_system/models/tokenizer/tokenizer.model`.

---

## 15. File Artifact Summary

| Artifact               | Location                                          | Contents / Purpose                                                                                       |
| ---------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Domain markdown files  | `ai_system/data/raw/<domain>_docs/*.md`           | Source knowledge for retrieval; text is cleaned and embedded by `load_markdown_files()` before indexing. |
| Domain corpus text     | `ai_system/data/raw/<domain>_corpus.txt`          | Raw corpus text used for tokenizer retraining or model training.                                         |
| Tokenizer binary       | `ai_system/models/tokenizer/tokenizer.model`      | SentencePiece tokenizer model used by `TokenizerProcessor` to encode/decode text.                        |
| Tokenizer vocabulary   | `ai_system/models/tokenizer/tokenizer.vocab`      | Vocabulary entries and scores produced by SentencePiece.                                                 |
| Dense index storage    | `ai_system/data/embeddings/chroma/`               | ChromaDB vector store containing document embeddings, IDs, and metadata.                                 |
| Model checkpoint       | `ai_system/models/checkpoints/ckpt_best.pt`       | Saved best model weights, optimizer state, configs, iteration, and loss.                                 |
| Model checkpoint       | `ai_system/models/checkpoints/ckpt_iter_<n>.pt`   | Periodic training checkpoint with model state and optimizer state.                                       |
| Fine-tuned checkpoint  | `ai_system/models/checkpoints/ckpt_fine_tuned.pt` | Fine-tuned model weights and training metadata after a fine-tuning run.                                  |
| Retrieval orchestrator | `ai_system/app/retrieval/manager.py`              | Coordinates dense, sparse, hybrid retrieval, and reranking.                                              |
| Markdown parser        | `ai_system/app/utils/markdown_parser.py`          | Cleans markdown into plain text for indexing.                                                            |

---

## 14. Related Docs

- `docs/diversity.md` — multi-domain strategy and collection planning
- `docs/learning.md` — model architecture, training philosophy, tokenizer notes
- `docs/HowToUse.md` — operational commands and environment setup
- `docs/testing.md` — validation and testing workflow
- `docs/config_variables.md` — model and training hyperparameters
