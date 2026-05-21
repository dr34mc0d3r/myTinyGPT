# CLI Beginnings: Agentic Filesystem Interaction

This document outlines the architectural strategy for enabling **myTinyGPT** to interact with local JavaScript projects. This functionality allows the agent to review, refactor, and create code by bridging the gap between LLM reasoning and local file operations.

---

## 1. Core Architecture: FilesystemTool
We will implement a modular tool registered in `app/tools/registry.py` that provides controlled access to the filesystem.

### Capabilities
- **`list_files(directory)`**: Maps the project structure to provide context.
- **`read_file(filepath)`**: Allows the agent to review existing code.
- **`write_file(filepath, content)`**: Enables the agent to perform refactoring or code generation.

---

## 2. Safety & Engineering Principles
Since granting an AI write-access to your machine is high-risk, we will adhere to these mandates:

- **Strict Sandboxing**: All tools will be hard-coded to operate within a specific workspace directory. Any attempt to access paths outside this sandbox (e.g., `../`) will be rejected.
- **Auditability**: Every file read or write operation MUST be logged via `structlog` for complete transparency in the agent's history.
- **Iterative Implementation**: We follow a "Read-Only First" development lifecycle to ensure the agent can safely interpret code before attempting to modify it.

---

## 3. The Validation Workflow
To compensate for the limitations of a "tiny" transformer model, we will integrate a validation loop:

1. **Agent Logic**: The agent follows the **THINK-TOOL CALL-REFLECT** loop.
2. **Execution Check**: Before committing changes, the agent will trigger a `JSExecutor` tool (e.g., `eslint` or `node -e`) to validate the generated code.
3. **Refinement**: If validation fails, the agent receives the error, "thinks" about the cause, and attempts a fix.

---

## 4. How-To: Agentic Code Assistant Workflow
This is how you will utilize **myTinyGPT** as a code assistant once the filesystem tools are implemented.

### Scenario: Refactoring a JavaScript Function
**User Query:** *"Review `app/services/calculator.js` and refactor the `calculateTotal` function to use `reduce` instead of a loop."*

#### The Step-by-Step Agentic Loop:
1.  **THINK**: "The user wants to refactor a specific function. I need to read the file first to understand its current implementation."
2.  **TOOL CALL**: `read_file("app/services/calculator.js")`.
3.  **ANALYZE**: The agent reads the code, notes the `for` loop, and identifies the transformation to `reduce`.
4.  **THINK**: "I will generate the refactored code and run it through `eslint` to ensure it passes."
5.  **TOOL CALL**: `write_file("app/services/calculator.js", new_code)`.
6.  **REFLECT**: "The write was successful. Now I call `JSExecutor` to ensure no syntax errors."
7.  **TOOL CALL**: `run_lint("app/services/calculator.js")`.
8.  **RESPOND**: "I have refactored the function. Linting passed, and the code is now more functional."

---

## 5. Implementation Strategy
We will implement these capabilities in incremental phases:

1. **Phase 1: Read-Only Access**: Implement `list_files` and `read_file` to allow the agent to "observe" the JS project structure.
2. **Phase 2: File Modification**: Introduce `write_file` with strict path validation and pre-commit logging.
3. **Phase 3: Validation Integration**: Add the `JSExecutor` tool for automated code verification.

---
*Last Updated: Monday, May 18, 2026*
