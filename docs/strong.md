# myTinyGPT: Specialized Configurations

This document outlines how to configure `myTinyGPT` for high-performance specialized tasks.

---

## 1. Code Assistant Setup

To transform `myTinyGPT` into an expert code assistant, the system relies heavily on the quality of its retrieval corpus and tokenizer training data. For detailed instructions on setting up `myTinyGPT` as a JavaScript code assistant, refer to `codeAssistant.md`.

### A. Data Curation Strategy
The model's intelligence as a code assistant is derived primarily from the **Hybrid Retrieval System** rather than the LLM's raw parameter count. Focus on idiomatic source code and high-quality documentation.

### B. Configuration Tuning
Adjust `app/config/default_config.yaml` to favor retrieval precision, increasing `top_k` for dense search and prioritizing `reranker` scores.

### C. Suggested Workflow for Code Assistance
The general workflow involves ingestion and indexing of language-specific documentation and utilizing prompt templates to guide the agent.

## 2. Financial Analysis GPT Setup

To configure `myTinyGPT` for financial analysis, the system must shift focus from syntactic code structures to semantic, time-series, and quantitative document analysis.

### A. Data Sources & Corpus Examples
The model's analytical power will come from high-quality, dense financial datasets:

1. **Training Data:**
   - **SEC Filings (10-K, 10-Q):** Excellent for learning corporate financial reporting language.
   - **Earnings Call Transcripts:** Provide insight into executive sentiment and future guidance.
   - **Financial Textbooks/Guides:** Essential for teaching the model foundational accounting and valuation metrics (P/E ratios, DCF models).

2. **Retrieval Corpus (`data/raw/`):**
   - **Market Reports:** Daily summaries from reputable financial news outlets.
   - **Company Profiles:** Structured data (JSON/CSV) converted to Markdown describing company fundamentals.
   - **Research Notes:** Analyst reports focusing on sector-specific trends.

### B. Strategies for Real-Time Stock Analysis
Standard `myTinyGPT` is local-first, but real-time analysis requires bridging the gap to live market data:

1. **Live Tool Integration:**
   - Develop a `MarketDataTool` (e.g., using a library like `yfinance` or a REST API like Alpha Vantage).
   - The agent should use this tool to fetch current prices, historical data, or recent market headlines.
   - **Implementation:** Register the tool in `app/tools/registry.py` and ensure the agent knows when to invoke it (e.g., "Analyze the recent performance of TSLA").

2. **Temporal Memory:**
   - Financial data is time-sensitive. Augment the `memory/long_term.py` storage to include metadata timestamps for every retrieved chunk.
   - The agentic loop should prioritize "fresh" information (high-weighting of recent retrievals) over historical data during retrieval.

3. **Inference Server Updates:**
   - Real-time analysis might require the FastAPI server to trigger periodic background jobs (e.g., refreshing a vector cache of today's market headlines) to ensure the agent is "aware" of the current day's events.

## 3. Internet Search Implementation

For tasks requiring real-time data or information beyond the local knowledge base, a `SearchTool` is essential.

### A. Architectural Approach
- **Tool Implementation:** Create `app/tools/search.py` using the `duckduckgo-search` library (privacy-friendly, no API key required).
- **Processing:** Include a lightweight scraper (e.g., `trafilatura`) to convert fetched web pages into clean Markdown for the LLM.
- **Integration:** Register the tool in `app/tools/registry.py` and ensure it returns structured results (URL, summary, content).

### B. Invocation Strategy
The agent should be prompted in `app/prompts/templates.py` to trigger the `SearchTool` when:
- **Temporal Relevance:** Querying events or data post-dating the latest model checkpoint.
- **Verification:** Fact-checking local retrieved documents or resolving internal hallucinations.
- **Coverage Gaps:** When local vector search scores are below a specified confidence threshold.

### C. Agentic Workflow
1. **Decision:** The agent evaluates the prompt and identifies a gap in local knowledge.
2. **Execution:** The agent calls `SEARCH(query="...")`.
3. **Synthesis:** The `ContextBuilder` appends the search results as "live context" alongside local documents before passing the final state to the Tiny LLM for response generation.

## 4. General Purpose Adaptations

*Coming soon: Guides for Creative Writing and Scientific Research.*
