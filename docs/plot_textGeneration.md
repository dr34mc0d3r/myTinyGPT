# Plot + Text Generation in trainer.py

This document explains what the text generation section in `ai_system/app/training/trainer.py` is doing, and what you should look for when the training loop displays generation samples.

## What the training text generation is doing

During training, the code now does the following at each `log_interval` step:

1. The model is switched to evaluation mode with `self.model.eval()`.
2. Multiple prompts (currently JavaScript code snippets) are iterated over.
3. For each prompt, the prompt is encoded using the tokenizer.
4. The model generates additional tokens autoregressively from that prompt, using the model's `generate()` method.
5. The generated token ids are decoded back into text with `self.tokenizer.decode(...)`.
6. All sample continuations are displayed in the top half of the `plotext` output.
7. Training resumes with `self.model.train()` so gradient updates continue normally.

That means the samples are not used for training. They are only live qualitative checks on the model's current behavior across diverse prompts.

## What the generated text represents

- Each output is a continuation of a given prompt, e.g. `"function fetchData("` → `"function fetchData(url) { ...`.
- Each is produced by sampling from the model's predicted next-token distribution.
- By sampling from multiple different prompts, you get a sense of whether the model generalizes beyond one context.
- This gives you a rough sense of whether the model is learning syntax, vocabulary, and coherence across different coding patterns.

## What to look for

When the generator samples appear, pay attention to:

- **Prompt-specific behavior**: Does the model produce sensible continuations for each different prompt?
- **Coherence**: Are the next tokens making sense together, or are they random junk?
- **Language consistency**: Do JavaScript samples contain JavaScript patterns (braces, semicolons, arrow functions)?
- **Repetition**: Does the model repeat the same token or phrase over and over?
- **Grammar and tokenization artifacts**: Sentence shape, spacing, and weird token pieces can reveal tokenizer or decoding issues.

## How this relates to training metrics

The generated samples are a qualitative signal, not a precise metric.

- Use the loss curves for quantitative progress (training loss, validation loss).
- Use the sample text as a sanity check for output quality.
- If loss improves but generated text is still poor, it may indicate the model is overfitting, the prompts are not representative, or the tokenizer/model capacity is too small.

## Why generate during training?

Including live generated text from multiple prompts in the training display helps you:

- catch early problems in text quality across different domains
- confirm the model is producing natural-looking output for diverse contexts
- see how generation behavior changes over iterations
- identify whether the model is learning prompt-specific patterns or generic language

## Generation settings and modifications

You can tune the text generation behavior from `trainer.py` by changing the prompts and sampling parameters.

### Prompts

The current default uses JavaScript code snippets:

```python
prompts = [
    "function fetchData(",
    "Array.prototype.map",
    "async function getUser(",
    "const promise = new Promise",
    "document.addEventListener('click', ",
    "The Map object allows you to ",
]
```

You can replace these with:

- domain-specific text (e.g., API documentation, scientific papers, poetry)
- a mix of short and long prompts for variety
- task-specific seeds that match your training data

### Sampling parameters

- `max_new_tokens`: Control how many tokens are generated per sample. Use a smaller value (e.g. `20`) for quick checks, or a larger value (e.g. `100`) for longer continuations.
- `temperature`: Adjust model randomness.
  - `temperature = 1.0` is standard sampling.
  - `temperature < 1.0` makes output more conservative and deterministic.
  - `temperature > 1.0` increases creativity and randomness.
  - The current default is `0.8` for a balance between coherence and diversity.
- `top_k`: Restrict sampling to the top K most likely tokens.
  - `top_k=40` is the current default, a good starting point.
  - Lower values such as `top_k=10` make generation safer and more focused.
  - Leaving `top_k=None` samples from the full distribution.

### Other modifications

- **Generate less frequently**: Only generate samples on validation intervals, not on every `log_interval`, to reduce overhead.
- **Rotate prompts**: Use different prompts on different training steps.
- **Save output**: Append the generated text to a log file instead of only printing it in the terminal.
- **Adjust display**: Change the line wrapping width (e.g., `55` characters) to fit your terminal better.

## Notes

- The samples are produced at every `log_interval`, so they update frequently.
- Generating from multiple prompts provides a better sense of model generalization than a single prompt.
- If you want more realistic behavior, use prompts that match your actual training data distribution.
