AGENT_SYSTEM_PROMPT = """You are an AI assistant. Use the context and tools to answer.

Tools: {tools_description}
Context: {context}
Query: {query}

THINK: Analyze request.
RESPOND: Final answer.
"""

def format_agent_prompt(query: str, tools_description: str, memory: str = "", context: str = "") -> str:
    # memory is currently ignored to save space, but can be added if short
    full_context = context
    if memory:
        full_context = f"Recent history: {memory}\n{context}"
        
    return AGENT_SYSTEM_PROMPT.format(
        query=query,
        tools_description=tools_description,
        context=full_context
    )
