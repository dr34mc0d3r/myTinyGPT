# System Data Flow: User Query Lifecycle

This document traces the path of a user query through the `myTinyGPT` architecture, from the initial API request to the final generated response.

---

## 1. Entry Point: API Layer
The journey begins at the FastAPI server.

- **File:** `ai_system/app/api/main.py`
- **Function:** `chat_endpoint(request: ChatRequest)`
- **Role:** Receives the raw JSON payload containing the user's query and session context (e.g., conversation ID).
- **Process:** 
    - Initializes the `AgentController`.
    - Manages streaming responses using `StreamingResponse`.

---

## 2. Orchestration: Agentic Controller
The `AgentController` manages the high-level logic (the "Agent Loop").

- **File:** `ai_system/app/agent/controller.py`
- **Function:** `AgentController.execute(query: str, history: List[Message])`
- **Role:** Orchestrates the THINK-RETRIEVE-TOOL-RESPOND cycle.
- **Process:**
    - Calls the LLM to determine the next action (THINK).
    - If retrieval is needed, invokes `RetrievalManager`.
    - If a tool is needed, delegates to `ToolRegistry`.
    - Aggregates all results into a coherent context.

---

## 3. Retrieval: Hybrid Search
Retrieval provides the LLM with relevant, grounded information.

- **File:** `ai_system/app/retrieval/manager.py`
- **Function:** `RetrievalManager.search(query: str, top_k: int)`
- **Role:** Unified interface for dense and sparse retrieval.
- **Process:**
    - Calls `dense.py` (`VectorStore.search`) for semantic matches.
    - Calls `sparse.py` (`BM25Search.search`) for keyword matches.
    - Calls `reranker.py` (`CrossEncoderReranker.score`) to rank the combined candidates.
    - Returns a `Context` object containing the most relevant snippets.

---

## 4. Tool Execution: Tool Registry
When the agent decides to use a tool (e.g., calculator).

- **File:** `ai_system/app/tools/registry.py`
- **Function:** `ToolRegistry.run(tool_name: str, args: Dict)`
- **Role:** Routes the agent's request to the appropriate tool instance.
- **Process:**
    - Maps the string `tool_name` to a class (e.g., `CalculatorTool` in `calculator.py`).
    - Executes the tool's `run` method.
    - Returns a structured observation string to the `AgentController`.

---

## 5. Inference: The Tiny LLM
The final stage is generating the natural language response.

- **File:** `ai_system/app/llm/inference.py`
- **Function:** `Generator.generate(prompt: str, max_tokens: int)`
- **Role:** Autoregressive text generation.
- **Process:**
    - Tokenizes the final prompt (the user query + retrieved context + tool observations).
    - Uses `model.py` (`TransformerModel`) to predict the next tokens.
    - Returns the generated text stream to the `AgentController`, which forwards it to the API response.

---

## Summary Diagram
`User` -> `API` -> `AgentController` -> [`RetrievalManager` / `ToolRegistry`] -> `ContextBuilder` -> `LLM Generator` -> `API` -> `User`
