# myTinyGPT Configuration Variables

This document provides a breakdown of all hyperparameters defined in `ai_system/app/config/config.py`. These variables govern the architecture of the Transformer model and the behavior of the training pipeline.

---

## 1. ModelConfig
These variables define the architecture and structural constraints of the Tiny Transformer.

| Variable | Definition | Role |
| :--- | :--- | :--- |
| `vocab_size` | Size of the token vocabulary. | Sets the dimension of embedding and output layers. |
| `n_layers` | Number of transformer blocks. | Controls the model's depth and representational capacity. |
| `n_heads` | Number of attention heads. | Determines how many attention sub-spaces the model operates in. |
| `n_embd` | Embedding dimensionality. | Sets the vector size of token and positional representations. |
| `block_size` | Context window size (sequence length). | The maximum number of tokens the model processes at once. |
| `dropout` | Probability of randomly setting inputs to zero. | Regularization technique to prevent overfitting. |
| `bias` | Use of bias in linear/norm layers. | Affects how model layers shift output distributions. |

---

## 2. TrainingConfig
These variables control the optimization process and training efficiency.

| Variable | Definition | Role |
| :--- | :--- | :--- |
| `batch_size` | Number of training samples per iteration. | Balances hardware memory constraints and training stability. |
| `learning_rate` | Step size for weight updates. | The primary hyperparameter for controlling convergence speed. |
| `max_iters` | Total training iterations. | The limit on training duration. |
| `weight_decay` | L2 penalty on model weights. | Regularization to keep weights small and improve generalization. |
| `beta1` / `beta2` | AdamW optimizer moments. | Controls the moving averages of gradients and their squares. |
| `grad_clip` | Threshold for gradient rescaling. | Prevents exploding gradients during unstable training. |
| `decay_lr` | Boolean toggle for LR scheduling. | Whether to reduce LR as training progresses. |
| `warmup_iters` | Iterations for initial LR ramp-up. | Stabilizes training during the initial phase. |
| `lr_decay_iters` | Iterations for LR decay. | Defines the training horizon for scheduling. |
| `min_lr` | Minimum LR after decay. | Ensures training does not stop completely due to zero LR. |
| `eval_interval` | Frequency of evaluation steps. | Sets how often the model validates against test data. |
| `log_interval` | Frequency of log output. | Controls terminal verbosity. |
| `eval_iters` | Number of batches for evaluation. | Defines the precision of validation metrics. |
| `checkpoint_dir` | Storage path for model checkpoints. | Defines where training snapshots are saved. |
