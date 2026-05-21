import structlog
from typing import List, Dict, Any, Optional

from app.llm.inference import Generator
from app.retrieval.manager import RetrievalManager, ContextBuilder
from app.tools.registry import ToolRegistry
from app.prompts.templates import format_agent_prompt
from app.memory.manager import MemoryManager

logger = structlog.get_logger()

class AgentController:
    """
    Orchestrates the agent loop: THINK, RETRIEVE, TOOL CALL, RESPOND.
    """
    def __init__(
        self,
        generator: Generator,
        retrieval_manager: RetrievalManager,
        tool_registry: ToolRegistry,
        memory_manager: Optional[MemoryManager] = None
    ):
        self.generator = generator
        self.retrieval_manager = retrieval_manager
        self.tool_registry = tool_registry
        self.memory_manager = memory_manager or MemoryManager()

    def run(self, query: str, max_iterations: int = 1) -> str:
        """
        Runs the agent orchestration loop.
        """
        logger.info("agent_start", query=query)
        
        # 1. MEMORY RECALL
        logger.info("agent_step", phase="MEMORY_RECALL")
        memory_context = self.memory_manager.get_context(query)
        
        # 2. THINK & RETRIEVE (Heuristic for now: always check retrieval for relevance)
        logger.info("agent_step", phase="THINK/RETRIEVE")
        search_results = self.retrieval_manager.retrieve(query)
        retrieval_context = ContextBuilder.build_context(search_results)
        
        # 3. ANALYZE & TOOL CALL (Heuristic: check for math keywords to trigger calculator)
        # Note: In a larger model, the model would decide this. 
        # For our tiny model, we assist with basic routing logic.
        tool_output = ""
        if any(kw in query.lower() for kw in ["calculate", "math", "+", "-", "*", "/"]):
            logger.info("agent_step", phase="TOOL_CALL", tool="calculator")
            # Primitive extraction for testing
            import re
            expr = re.search(r'[\d\+\-\*\/\(\)\s\.]+', query)
            if expr:
                tool_output = self.tool_registry.execute_tool("calculator", expression=expr.group().strip())
                logger.info("tool_result", result=tool_output)

        # 4. CONTEXT BUILDING
        full_retrieval_context = retrieval_context
        if tool_output:
            full_retrieval_context += f"\n\nTool Result (Calculator):\n{tool_output}"

        # 5. REFLECT & RESPOND (Generate the final answer)
        logger.info("agent_step", phase="RESPOND")
        tools_desc = "\n".join([f"- {t.name}: {t.description}" for t in self.tool_registry.list_tools()])
        
        # Calculate available budget for context
        # Base prompt is about 60-80 tokens now. We want to leave 100 for generation.
        # So we have about 70-90 tokens for context + query.
        
        def truncate_context(ctx: str, max_tokens: int) -> str:
            tokens = self.generator.tokenizer.encode(ctx)
            if len(tokens) <= max_tokens:
                return ctx
            return self.generator.tokenizer.decode(tokens[:max_tokens])

        # Very aggressive truncation for 256 context window
        short_context = truncate_context(full_retrieval_context, 100)
        
        prompt = format_agent_prompt(
            query=query,
            tools_description=tools_desc,
            memory=memory_context,
            context=short_context
        )
        
        # Ensure total prompt is not too long
        prompt_tokens = self.generator.tokenizer.encode(prompt)
        if len(prompt_tokens) > 150: # leave 100 for generation
             prompt = self.generator.tokenizer.decode(prompt_tokens[-150:])

        response = self.generator.generate(prompt, max_new_tokens=100, temperature=0.7)
        
        # Cleanup: Extract only the RESPOND part if the model follows the prompt
        if "RESPOND:" in response:
            final_answer = response.split("RESPOND:")[-1].strip()
        else:
            final_answer = response

        # 6. SAVE TO MEMORY
        self.memory_manager.add_interaction(query, final_answer)

        logger.info("agent_complete", response=final_answer)
        return final_answer

if __name__ == "__main__":
    # Integration Test
    from app.tools.calculator import CalculatorTool
    
    # Initialize components
    # We use dummy paths or assume they exist from previous steps
    ckpt = "models/checkpoints/ckpt_best.pt"
    tok = "models/tokenizer/tokenizer.model"
    
    import os
    if not os.path.exists(ckpt):
        print("Test skipped: Model checkpoint not found.")
    else:
        gen = Generator(ckpt, tok)
        rm = RetrievalManager()
        tr = ToolRegistry()
        tr.register(CalculatorTool())
        
        agent = AgentController(gen, rm, tr)
        
        # Test 1: Retrieval query
        print("\n--- Test 1: Retrieval ---")
        answer = agent.run("What is transformer architecture?")
        print(f"Final Answer: {answer}")
        
        # Test 2: Math query
        print("\n--- Test 2: Math ---")
        answer = agent.run("Calculate 25 * 4")
        print(f"Final Answer: {answer}")
