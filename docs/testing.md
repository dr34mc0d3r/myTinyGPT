# Post-Training Validation & Testing Workflow

This document outlines the standard procedure for validating `myTinyGPT` after completing a training session, ensuring that the model has successfully converged and is ready for deployment.

---

## 1. Step-by-Step Validation Procedure

### Step 1: Environment Verification
Ensure your environment is correctly configured to utilize the latest checkpoint.
- Activate your `uv` virtual environment: `source ai_system/.venv/bin/activate`
- Verify the existence of the checkpoint: `ls -lh ai_system/models/checkpoints/ckpt_best.pt`

### Step 2: Basic Inference Test
Verify that the `Generator` can load the model state and produce coherent text.
- **Script:** `ai_system/app/llm/inference.py`
- **Action:** Run a minimal inference test script:
  ```python
  from ai_system.app.llm.inference import Generator
  gen = Generator(checkpoint_path="ai_system/models/checkpoints/ckpt_best.pt")
  print(gen.generate("What is the role of an agent in AI?", max_tokens=50))
  ```
- **Goal:** Confirm the model loads without error and produces output (even if the output is not yet high-quality).

### Step 3: Functional Agent Testing
Test the orchestration layer to ensure the agent correctly uses tools and retrieval.
- **Action:** Initiate a chat session via the `AgentController`.
- **Query:** "Use the calculator to compute 123 * 456."
- **Expected Outcome:** The agent correctly identifies the need for the `calculator` tool, executes it, and incorporates the result into the final response.

### Step 4: System Integration Test
Validate the FastAPI inference server.
- **Action:** Start the server: `uvicorn ai_system.app.api.main:app --reload`
- **Test:** Use `curl` or a browser to hit the `/chat` endpoint.
- **Goal:** Confirm streaming responses and memory persistence (multi-turn interaction) function correctly.

---

## 2. Interpreting Results & Improvement Strategies

Use this matrix to guide your iterative improvements based on test outcomes.

| Observed Behavior | Diagnosis | Recommended Improvement |
| :--- | :--- | :--- |
| **Output is Gibberish** | Model underfit or data corruption | Train longer, increase training dataset size, or check tokenizer training. |
| **Repeated Phrases** | Overfitting / Lack of diversity | Increase temperature, add dropout, or introduce more diverse training data. |
| **Agent Fails Tool Call** | Prompt/Instruction following issue | Refine system prompt in `app/prompts/templates.py`; check tool registration in `app/tools/registry.py`. |
| **Retrieval is Irrelevant** | Embedding mismatch / Corpus issue | Re-index `data/raw/` with better cleaned markdown; tune hybrid retrieval weights in `retrieval/manager.py`. |
| **Slow Response Time** | Inference/Retrieval bottleneck | Profile `reranker.py` or increase embedding batch sizes. |

---

## 3. Automated Testing (Best Practices)
As you mature the project, move beyond manual verification:
- **PyTest:** Use `pytest` to run automated test suites on core modules (`app/retrieval/`, `app/agent/`, `app/llm/`).
- **Regression Testing:** Keep a set of 10-20 "Golden Queries" with expected tool/retrieval outcomes. Run these automatically after every training run to ensure new checkpoints don't break expected agent behavior.

*Last Updated: Monday, May 18, 2026*
