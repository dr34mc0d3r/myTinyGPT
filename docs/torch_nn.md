# torch.nn usage in myTinyGPT

This document lists every code file outside `docs/` that uses `torch.nn`, what the `nn` constructs are used for, and the key parameters involved.

## ai_system/app/llm/model.py

### What it is used for

This file defines the GPT-style model architecture and its building blocks using PyTorch `nn.Module` classes.

### `torch.nn` classes and usage

- `NewGELU(nn.Module)`
  - Custom GELU activation function implementation.
  - No explicit parameters beyond the input tensor.

- `CausalSelfAttention(nn.Module)`
  - Multi-head causal self-attention block.
  - Uses `nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)` for combined query/key/value projection.
  - Uses `nn.Linear(config.n_embd, config.n_embd, bias=config.bias)` for output projection.
  - Uses `nn.Dropout(config.dropout)` for attention dropout.
  - Uses `nn.Dropout(config.dropout)` for residual dropout.
  - Creates a causal attention mask buffer sized `(config.block_size, config.block_size)`.
  - Stores `config.n_heads`, `config.n_embd`, and `config.dropout` for head splitting and dropout.

- `MLP(nn.Module)`
  - Feed-forward network inside each transformer block.
  - Uses `nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)` for expansion.
  - Uses `NewGELU()` activation.
  - Uses `nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias)` for projection back to embedding size.
  - Uses `nn.Dropout(config.dropout)` for post-activation dropout.

- `Block(nn.Module)`
  - Single transformer block combining layer normalization, attention, and MLP.
  - Uses `nn.LayerNorm(config.n_embd, elementwise_affine=config.bias)` before attention.
  - Uses `CausalSelfAttention(config)`.
  - Uses `nn.LayerNorm(config.n_embd, elementwise_affine=config.bias)` before the MLP.
  - Uses `MLP(config)`.

- `TinyTransformer(nn.Module)`
  - Full GPT-style transformer model.
  - Uses `nn.ModuleDict` containing:
    - `wte = nn.Embedding(config.vocab_size, config.n_embd)` for token embeddings.
    - `wpe = nn.Embedding(config.block_size, config.n_embd)` for position embeddings.
    - `drop = nn.Dropout(config.dropout)` for embedding dropout.
    - `h = nn.ModuleList([Block(config) for _ in range(config.n_layers)])` for stacked transformer blocks.
    - `ln_f = nn.LayerNorm(config.n_embd, elementwise_affine=config.bias)` final layer normalization.
  - Uses `nn.Linear(config.n_embd, config.vocab_size, bias=False)` for the language modeling head.

### Initialization using `torch.nn` utilities

- `torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)` for `nn.Linear` weights.
- `torch.nn.init.zeros_(module.bias)` for linear biases when bias is present.
- `torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)` for `nn.Embedding` weights.
- Special scaled initialization for all `c_proj.weight` parameters using `torch.nn.init.normal_` with
  `std=0.02 / sqrt(2 * config.n_layers)`.

## ai_system/app/training/trainer.py

### What it is used for

This file uses a `torch.nn` utility during training.

### `torch.nn` utility usage

- `torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.config.training.grad_clip)`
  - Clips gradient norms during training.
  - Uses `self.model.parameters()` and `self.config.training.grad_clip`.

## Notes

- This document intentionally excludes any usage of `torch` that is not part of the `torch.nn` module.
- No other Python source files outside `docs/` use `torch.nn` in this repository.
