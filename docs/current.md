# Current Project Performance Report

This report summarizes the expected performance of the current `ai_system` setup based on:

- `ai_system/app/config/config.py`
- `ai_system/app/config/default_config.yaml`
- `ai_system/app/tokenizer/processor.py`
- `ai_system/app/training/trainer.py`
- `ai_system/app/training/dataset.py`
- `ai_system/app/llm/model.py`
- `ai_system/app/llm/inference.py`
- `ai_system/app/retrieval/manager.py`
- `ai_system/app/agent/controller.py`
- `ai_system/app/api/main.py`
- `ai_system/data/raw/sample_corpus.txt`
- `ai_system/data/raw/javascript_docs`

## 1. Current model and training configuration

The default training configuration is:

- `vocab_size`: 8000 (adjusted automatically to actual tokenizer size 100 at runtime)
- `n_layers`: 4
- `n_heads`: 4
- `n_embd`: 128
- `block_size`: 128
- `dropout`: 0.1
- `bias`: True
- `batch_size`: 1
- `gradient_accumulation_steps`: 8
- `learning_rate`: 6e-4
- `weight_decay`: 0.1
- `beta1`: 0.9
- `beta2`: 0.95
- `grad_clip`: 1.0
- `warmup_iters`: 500
- `lr_decay_iters`: 5000
- `min_lr`: 6e-5
- `max_iters`: 5000
- `eval_interval`: 200
- `log_interval`: 10
- `eval_iters`: 100
- `checkpoint_dir`: `ai_system/models/checkpoints`

Note: `ai_system/app/training/trainer.py` constructs `Config()` from `ai_system/app/config/config.py` and uses the tokenizer from `ai_system/models/tokenizer/tokenizer.model`. The file `ai_system/app/config/default_config.yaml` exists with alternate defaults (`block_size: 256`, `batch_size: 32`), but the current training script does not load that YAML automatically.

### Model size and capacity

The current Tiny Transformer is a small GPT-style model with roughly **0.8M parameters**.

This means the model is very lightweight and intended for experimentation or low-resource training, not for high-quality large-scale language performance.

## 2. Tokenizer and vocabulary

The system currently uses a SentencePiece tokenizer loaded from `ai_system/models/tokenizer/tokenizer.model`.

- Actual tokenizer vocabulary size: **100**
- This is much smaller than the default config's `vocab_size` of 8000.
- The training code adjusts the model vocab size at startup to match the tokenizer.

A 100-token vocabulary is extremely small for natural language, especially for English and JavaScript. It is likely to produce very coarse or fragmented output.

## 3. Training data: `sample_corpus.txt`

The current sample corpus is a tiny JavaScript-focused text file with:

- **7,140 characters**
- **467 lines**
- **902 words**

It contains basic JavaScript examples covering:

- variables (`let`, `const`, `var`)
- functions and arrow functions
- arrays and object access
- async/await and Promises
- Node.js server examples
- React components and hooks
- common patterns like `map`, `filter`, and `reduce`

### Expected performance from this corpus

- The model can learn a few basic JavaScript patterns from this small dataset.
- It is likely to overfit rapidly because the corpus is tiny.
- Generalization beyond the exact examples is limited.
- Generated output will probably reflect the same repetitive phrases and simple examples.

## 4. Training and inference pipeline behavior

- `ai_system/app/training/trainer.py` loads `ai_system/models/tokenizer/tokenizer.model` and automatically adjusts `config.model.vocab_size` to the tokenizer's actual size.
- `ai_system/app/training/dataset.py` tokenizes the entire training text and creates sliding windows of length `block_size`; with `batch_size=1`, the model sees one sequence at a time.
- There is no explicit separate validation file in the default training call; if `val_path` is not provided, evaluation runs over the training data itself.
- The current training script uses the defaults from `ai_system/app/config/config.py`. The alternate YAML file `ai_system/app/config/default_config.yaml` and `ai_system/app/config/config copy.py` are present, but neither is automatically loaded by the standard trainer.
- `ai_system/app/llm/inference.py` loads the checkpoint and tokenizer, adds a BOS token, and returns only the generated continuation tokens.
- `ai_system/app/agent/controller.py` always performs retrieval with `ai_system/app/retrieval/manager.py` and truncates retrieved context to around 100 tokens before prompt construction. That means even if the document corpus is large, the tiny transformer only receives a very small amount of retrieved context.
- The API in `ai_system/app/api/main.py` depends on a checkpoint file at `ai_system/models/checkpoints/ckpt_best.pt` and on the retrieval manager using `all-MiniLM-L6-v2` plus `cross-encoder/ms-marco-MiniLM-L-6-v2`.

## 5. JavaScript documentation corpus

The raw JavaScript docs folder contains a large MDN snapshot:

- **12,056 markdown files** under `ai_system/data/raw/javascript_docs`
- **~45 MB** of markdown text in total

This corpus is large enough to represent a broad set of JavaScript/web API documentation topics.

### Expected performance against the docs corpus

- The current trainer does not automatically train on `javascript_docs` unless a script or dataset loader is updated to use it.
- If the retrieval/indexing pipeline is configured to use these docs, then the system can potentially retrieve relevant passages from a large knowledge base.
- However, the underlying text generator remains the same small transformer trained on the tiny `sample_corpus.txt`, so generated answers will still be very limited.

## 6. Practical performance expectations

### Training quality

- With `max_iters=5000` and a tiny corpus, the model may fit the sample text quickly.
- Validation loss is useful, but the validation split is likely very small as well.
- The model may learn simple JavaScript syntax and short examples, but it will not become a robust JS assistant.

### Inference quality

- Expected output quality: low-to-moderate for very simple prompts.
- The model is likely to generate short, repetitive completions that resemble the sample data.
- The small tokenizer and limited vocabulary will hurt fluency and code syntax coverage.

### Retrieval / docs usage

- `javascript_docs` is a strong raw knowledge source if indexed.
- The current project can support retrieval, but the answer generation quality depends on the tiny transformer model.
- The system may be better suited to retrieval-based lookup than free-form code generation in its current state.

## 7. Recommendations for better performance

To improve output quality and usefulness:

1. Train the tokenizer on a larger corpus or a JavaScript-specific corpus to increase vocab coverage.
2. Use a larger model configuration:
   - more layers (`n_layers > 4`)
   - more heads (`n_heads > 4`)
   - larger embedding size (`n_embd > 128`)
3. Train on much more text than `sample_corpus.txt`.
4. Add the JavaScript docs corpus to the training dataset or fine-tune against it.
5. Use retrieval from `javascript_docs` for factual lookup while keeping generation simple.

## 8. Summary

The current project configuration is valid for lightweight experiments, but the expected performance is constrained by:

- a tiny model (0.8M parameters)
- a very small tokenizer vocabulary (100 tokens)
- a tiny training corpus (`sample_corpus.txt`)
- a large documentation corpus that is not currently the primary training source

This means the system can illustrate training and text generation mechanics, but it should not be expected to produce strong JavaScript assistant behavior without further data and model scaling.

## 9. Current `ai_system/app/config/config.py` variable values

The training pipeline currently uses these values from `ai_system/app/config/config.py`:

- `ModelConfig.vocab_size = 8000`
- `ModelConfig.n_layers = 4`
- `ModelConfig.n_heads = 4`
- `ModelConfig.n_embd = 128`
- `ModelConfig.block_size = 128`
- `ModelConfig.dropout = 0.1`
- `ModelConfig.bias = True`
- `TrainingConfig.batch_size = 1`
- `TrainingConfig.gradient_accumulation_steps = 8`
- `TrainingConfig.learning_rate = 6e-4`
- `TrainingConfig.max_iters = 5000`
- `TrainingConfig.weight_decay = 0.1`
- `TrainingConfig.beta1 = 0.9`
- `TrainingConfig.beta2 = 0.95`
- `TrainingConfig.grad_clip = 1.0`
- `TrainingConfig.decay_lr = True`
- `TrainingConfig.warmup_iters = 500`
- `TrainingConfig.lr_decay_iters = 5000`
- `TrainingConfig.min_lr = 6e-5`
- `TrainingConfig.eval_interval = 200`
- `TrainingConfig.log_interval = 10`
- `TrainingConfig.eval_iters = 100`
- `TrainingConfig.checkpoint_dir = ai_system/models/checkpoints`

Recommended config changes for a more useful JavaScript code assistant:

- increase `ModelConfig.n_layers` to 6-12 or higher for richer reasoning/body of code
- increase `ModelConfig.n_embd` to 256 or 512 so the model can represent more syntax and semantics
- keep or increase `ModelConfig.n_heads` to 4-8 for better attention capacity
- increase `ModelConfig.block_size` to 256 or 512 to support longer code examples and prompt context
- use a larger tokenizer vocabulary than 100 tokens; the config should match the tokenizer size after training
- increase `TrainingConfig.batch_size` from 1 to 8-32 if memory allows, or keep `gradient_accumulation_steps` high to simulate larger batches
- extend `TrainingConfig.max_iters` beyond 5000 when training on more data
- ensure `TrainingConfig.eval_interval` and `TrainingConfig.eval_iters` are tuned to the dataset size so validation is meaningful

## 10. How to improve `ai_system/data/raw/sample_corpus.txt`

To make `sample_corpus.txt` support a useful JavaScript code assistant, the corpus should be expanded and structured with:

- more representative JavaScript code examples covering modern syntax, browser APIs, Node.js, React, TypeScript-style patterns, and common data structures
- clear problem/solution pairs, function signatures, and short code snippets with comments
- more diverse contexts instead of only one or two repeated idioms
- explicit prompts and answers or doc-style Q&A examples to help the model learn helpful behavior
- real code samples from multiple sources rather than only handcrafted toy snippets

Specific improvements:

1. add many more examples of JavaScript standard library and DOM APIs, e.g. `fetch`, `Promise`, `async/await`, `Map`, `Set`, `Array.prototype.*`, events, and DOM selection
2. include full code examples for common tasks like form handling, event delegation, API fetching, error handling, file I/O in Node, and simple component rendering
3. mix natural language descriptions with code examples so the model learns to map questions to code
4. keep each example compact enough for the current `block_size`, but increase diversity and quantity so the model does not overfit
5. optionally add a small validation split to the dataset and use a larger tokenizer/vocab so syntax is better preserved

These changes would make the corpus more useful for training a JavaScript assistant rather than merely a toy syntax generator.
