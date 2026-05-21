# Fresh Start for a New Knowledge Domain

This guide explains how to reset `myTinyGPT` and start fresh for a new knowledge domain. It covers cleanup, configuration, and the files that need to be recreated.

---

## 1. When to use this guide

Use this fresh-start workflow when you want to:

- switch to an entirely new domain of knowledge
- rebuild the retrieval index from scratch
- retrain or replace the tokenizer for a new vocabulary
- start training/fine-tuning with a clean checkpoint slate

If you want to keep old domains and add a second one, do not delete your raw domain folders. Instead use separate raw folders and consider multi-domain retrieval support.

---

## 2. Clean up old artifacts

From the repository root, delete the current retrieval and model artifacts:

```bash
cd /home/chris/DEV/myTinyGPT
rm -rf ai_system/data/embeddings/chroma
rm -rf ai_system/models/checkpoints/*
rm -f ai_system/models/tokenizer/tokenizer.model
rm -f ai_system/models/tokenizer/tokenizer.vocab
```

### What are these files?

/home/chris/DEV/myTinyGPT/ai_system/data/logs/\*

### Why these files are removed

- `ai_system/data/embeddings/chroma/`
  - Removes the existing dense retrieval database and all vector embeddings.
- `ai_system/models/checkpoints/*`
  - Removes old model checkpoints so training/fine-tuning starts from scratch.
- `ai_system/models/tokenizer/tokenizer.model`
  - Removes the old SentencePiece tokenizer model.
- `ai_system/models/tokenizer/tokenizer.vocab`
  - Removes the tokenizer vocabulary file.

> If you want to keep the existing tokenizer, skip the tokenizer removal step.

---

## 3. Configure a new domain

### 3.1 Create a new raw-data folder

Create a domain-specific folder under `ai_system/data/raw/`.

Example:

```bash
cd /home/chris/DEV/myTinyGPT
mkdir -p ai_system/data/raw/gardening_docs
```

Add markdown files there, for example:

- `ai_system/data/raw/gardening_docs/plant-care.md`
- `ai_system/data/raw/gardening_docs/soil-types.md`
- `ai_system/data/raw/gardening_docs/pruning-guide.md`

### 3.2 Create a domain corpus file (optional)

For training or tokenizer retraining, create one or more text files in `ai_system/data/raw/`.

Example:

- `ai_system/data/raw/gardening_corpus.txt`
- `ai_system/data/raw/finance_corpus.txt`

These files should contain clean plain text relevant to your new domain.

### 3.3 Update retrieval indexing source

The current indexing script is:

- `ai_system/scripts/index_js_docs.py`

For a fresh new domain, either:

- duplicate and modify this script to point to your new raw folder, or
- write a small script that calls `RetrievalManager.index_documents()` with the new folder.

The key setting is the source folder, e.g.:

```python
docs_path = "ai_system/data/raw/gardening_docs/"
```

---

## 4. Configure training and tokenizer paths

### 4.1 Confirm tokenizer path

The tokenizer loader expects:

- `ai_system/models/tokenizer/tokenizer.model`

The trainer and inference components also use this path.

### 4.2 Confirm checkpoint path

The default checkpoint directory is configured in `ai_system/app/config/config.py`:

- `checkpoint_dir: "ai_system/models/checkpoints"`

The API and inference scripts expect a checkpoint at:

- `ai_system/models/checkpoints/ckpt_best.pt`

If you change this path, update:

- `ai_system/app/api/main.py`
- `ai_system/scripts/fine_tune.py`
- `ai_system/app/training/trainer.py`
- `ai_system/app/llm/inference.py`

### 4.3 Optional config tuning

If you want to start fresh with a different training setup, edit `ai_system/app/config/default_config.yaml` or use `ai_system/app/config/config.py` to save a custom config.

Key values to adjust:

- `training.batch_size`
- `training.learning_rate`
- `training.max_iters`
- `training.eval_interval`
- `training.checkpoint_dir`
- `model.vocab_size`
- `model.block_size`

---

## 5. Recreate the tokenizer

If you deleted the tokenizer or need a new vocabulary for the domain, retrain SentencePiece.

### 5.1 Command

```bash
cd /home/chris/DEV/myTinyGPT/ai_system
python3 -m app.tokenizer.trainer
```

### 5.2 Custom training inputs

If you want a domain-specific tokenizer, modify `ai_system/app/tokenizer/trainer.py` to call `TokenizerTrainer.train()` on your domain corpus, for example:

```python
trainer = TokenizerTrainer(vocab_size=8000)
trainer.train(["ai_system/data/raw/gardening_corpus.txt"], "ai_system/models/tokenizer")
```

### 5.3 Files created

- `ai_system/models/tokenizer/tokenizer.model`
- `ai_system/models/tokenizer/tokenizer.vocab`

---

## 6. Rebuild the retrieval index

### 6.1 Data cleanup

If `ai_system/data/embeddings/chroma/` still exists, delete it first.

```bash
rm -rf ai_system/data/embeddings/chroma
```

### 6.2 Run indexing

For a fresh domain, use a script that loads markdown from your new raw folder and indexes it with `RetrievalManager`.

Example command if using a modified script:

```bash
python3 ai_system/scripts/index_js_docs.py
```

### 6.3 What this produces

- `ai_system/data/embeddings/chroma/`
  - ChromaDB persistent vector store
  - embedding vectors, document IDs, and metadata

---

## 7. Start fresh training or fine-tuning

### 7.1 Fresh model training

If you want the model to learn the new domain explicitly, run:

```bash
cd /home/chris/DEV/myTinyGPT
python3 -m ai_system.app.training.trainer
```

This creates fresh checkpoint files under:

- `ai_system/models/checkpoints/`

### 7.2 Fresh fine-tuning

If you already have a base model and want to fine-tune it on the new domain, run:

```bash
cd /home/chris/DEV/myTinyGPT
python3 ai_system/scripts/fine_tune.py
```

This produces:

- `ai_system/models/checkpoints/ckpt_fine_tuned.pt`
- possibly a refreshed `ai_system/models/checkpoints/ckpt_best.pt`

---

## 8. Validate the fresh domain setup

### 8.1 Check existence of artifacts

Confirm these files/directories were recreated:

- `ai_system/models/tokenizer/tokenizer.model`
- `ai_system/models/tokenizer/tokenizer.vocab`
- `ai_system/data/embeddings/chroma/`
- `ai_system/models/checkpoints/ckpt_best.pt`

### 8.2 Run a small inference test

```bash
python3 -c "from ai_system.app.llm.inference import Generator; gen = Generator('ai_system/models/checkpoints/ckpt_best.pt', 'ai_system/models/tokenizer/tokenizer.model'); print(gen.generate('Test query', max_new_tokens=10))"
```

### 8.3 Run the API and query

```bash
cd /home/chris/DEV/myTinyGPT
python3 -m ai_system.app.api.main
```

Then POST a query to `/chat` to ensure the new domain is active.

---

## 9. Fresh start checklist

- [ ] Deleted old retrieval database: `ai_system/data/embeddings/chroma/`
- [ ] Deleted old checkpoints: `ai_system/models/checkpoints/*`
- [ ] Deleted or replaced tokenizer files: `ai_system/models/tokenizer/tokenizer.model`, `ai_system/models/tokenizer/tokenizer.vocab`
- [ ] Created a new raw-data domain folder under `ai_system/data/raw/`
- [ ] Added domain markdown and/or corpus text
- [ ] Updated or duplicated indexing script to point to the new raw folder
- [ ] Verified tokenizer path and checkpoint path in the code
- [ ] Rebuilt the retrieval index
- [ ] Trained or fine-tuned the model
- [ ] Verified inference and API responses

---

## 10. Notes

- If you want to keep previous domains without deleting them, do not delete your old raw folders. Instead, create new domain folders and add support for separate collections later.
- If you reuse the old tokenizer for a similar domain, skip tokenizer deletion and retraining.
- Always save backups of any artifact you might want to preserve before deleting files.
