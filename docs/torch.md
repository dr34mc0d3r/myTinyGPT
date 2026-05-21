# torch usage in myTinyGPT

This document lists every code file outside `docs/` that uses `torch`, and explains what the `torch` classes or functions are used for in each file.

## ai_system/app/llm/model.py

- `torch.tanh`, `torch.pow`: used inside `NewGELU.forward()` to compute the GELU activation.
- `torch.tril`, `torch.ones`: used to build the causal attention mask buffer in `CausalSelfAttention.__init__()`.
- `torch.nn.init.normal_`, `torch.nn.init.zeros_`: used in `TinyTransformer._init_weights()` and the special residual projection init loop to initialize model weights and biases.
- `torch.arange`: used in `TinyTransformer.forward()` to create position indices for token sequences.
- `torch.no_grad`: used as a decorator for `TinyTransformer.generate()` to disable gradient tracking during sampling.
- `torch.topk`, `torch.multinomial`, `torch.cat`: used in `TinyTransformer.generate()` to compute top-k logits, sample the next token, and append it to the generated sequence.
- `torch.randint`: used in the module test block under `if __name__ == "__main__"` to create dummy input token indices.

## ai_system/app/llm/inference.py

- `torch.load`: loads a saved checkpoint from disk into CPU or the chosen device.
- `torch.no_grad`: used as a decorator for `Generator.generate()` to run inference without tracking gradients.
- `torch.tensor`: converts encoded token ID lists into a `torch.Tensor` on the selected device for model input.

## ai_system/app/training/dataset.py

- `torch.tensor`: converts token ID lists into `torch.Tensor` objects when preparing the dataset.
- `torch.Tensor`: used in type annotations for `__getitem__()` return values.
- `torch.utils.data.Dataset`: base class for `TextDataset`, enabling PyTorch dataset behavior.
- `torch.utils.data.DataLoader`: used in `create_dataloader()` to wrap `TextDataset` for batch loading.

## ai_system/app/training/trainer.py

- `torch.optim.AdamW`: optimizer used to train the model with learning rate, beta, and weight decay settings.
- `torch.nn.utils.clip_grad_norm_`: clips the gradients of model parameters during training when `grad_clip` is enabled.
- `torch.no_grad`: used as a decorator for `Trainer.estimate_loss()` to evaluate model loss without gradient tracking.
- `torch.zeros`: creates a tensor for accumulating evaluation losses during `estimate_loss()`.
- `torch.save`: saves training checkpoints to disk.

## ai_system/scripts/fine_tune.py

- `torch.load`: loads a checkpoint from disk for fine-tuning, including model weights and configuration.
