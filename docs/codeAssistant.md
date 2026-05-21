# myTinyGPT: JavaScript Code Assistant Guide

This guide explains how to leverage the **myTinyGPT** system as a specialized JavaScript code assistant. By utilizing the Hybrid Retrieval system and the Agentic Orchestration layer, you can turn this tiny model into a powerful tool for JS development.

---

## 1. Building the JavaScript Knowledge Base

The most effective way to use myTinyGPT for a specific language is to feed it high-quality context.

### Step 1: Prepare Your JS Documentation

Gather `.txt` or `.md` files containing:

- JavaScript syntax rules.
- Documentation for your favorite frameworks (React, Vue, Node.js).
- Your own project's code snippets and architectural patterns.

Place these in `ai_system/data/raw/javascript_docs/`.

### Step 2: Index the Data

We have provided a dedicated utility to handle markdown files effectively.

Use the `index_js_docs.py` script, which leverages the `markdown_parser` to recursively find, clean, and index your markdown files before adding them to the ChromaDB vector store.

```bash
# Ensure you are in the project root
python3 ai_system/scripts/index_js_docs.py
```

This script will automatically traverse all subdirectories of `ai_system/data/raw/javascript_docs/`, filtering out hidden system files and resource forks, and loading all `.md` files to populate your retrieval index. It also includes robust encoding handling to prevent ingestion failures.

## 2. Querying for JavaScript Assistance

Once your knowledge base is indexed, you can ask the agent for help.

### Example Queries

#### Logic & Refactoring

**User:** "How do I rewrite this nested `for` loop into a more functional approach using `.map()` or `.reduce()`?"
**Agent Process:**

1. **THINK**: The user wants to refactor a loop. I should check if there are any specific JS functional patterns in my retrieval.
2. **RETRIEVE**: Searches for "javascript functional programming patterns" or "map reduce examples".
3. **RESPOND**: Provides the refactored code based on retrieved context.

#### Debugging

**User:** "Why is my `async` function returning `[object Promise]` instead of the data?"
**Agent Process:**

1. **THINK**: This is a common JS error related to missing `await`.
2. **RETRIEVE**: Looks for "javascript async await common mistakes".
3. **RESPOND**: Explains the need for `await` and provides a corrected snippet.

## 3. Agentic Workflow for JS Tasks

The Agent Loop is designed to follow a **THINK-RETRIEVE-RESPOND** pattern. For JS tasks, it excels at:

1. **Contextual Awareness**: It uses the `Hybrid Retrieval` to find exact keyword matches (like specific API names) via BM25 and conceptual matches via Dense search.
2. **Iterative Refinement**: If you enable multiple iterations, the agent can "THINK" about its own previous answer and refine the JS code for better performance or readability.

## 4. Integration with Your JS Projects

You can call the myTinyGPT API directly from your JavaScript or TypeScript code.

### Example: Using `fetch` in Node.js or Browser

```javascript
async function getCodeHelp(query) {
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON_stringify({
      query: query,
      max_iterations: 1,
    }),
  });

  const data = await response.json();
  console.log("Assistant Response:", data.response);
}

getCodeHelp("Explain the difference between '==' and '===' in JavaScript.");
```

## 5. Advanced: Adding a JS Tool

To make the assistant even more powerful, you can add a tool to execute JS code for validation.

### Idea: `JSExecutor` Tool

1. Create `ai_system/app/tools/js_executor.py`.
2. Use `subprocess` to run `node -e "your_code"`.
3. Register it in `app/tools/registry.py`.

Now, when you ask "What is the result of this complex JS expression?", the agent can actually _run_ it to give you the correct answer.

## 6. Pro Tips for Better Results

- **Be Specific**: Instead of "Fix my code", say "Fix this JavaScript function to handle null inputs correctly."
- **Use Special Tokens**: The system is trained with specific markers. Ensure your queries are clear and technical.
- **Reranking**: The system uses a Cross-Encoder to rerank the top 10 retrieval results. This is particularly useful for finding the exact JS function signature among many similar-looking ones.
