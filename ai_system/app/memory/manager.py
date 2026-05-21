from typing import List, Dict, Any, Optional
from app.memory.short_term import ShortTermMemory
from app.memory.long_term import LongTermMemory

class MemoryManager:
    """
    Unified interface for short-term and long-term memory.
    """
    def __init__(
        self, 
        max_short_term: int = 10,
        ltm_collection: str = "agent_memories"
    ):
        self.short_term = ShortTermMemory(max_messages=max_short_term)
        self.long_term = LongTermMemory(collection_name=ltm_collection)

    def add_interaction(self, user_query: str, assistant_response: str):
        """
        Saves an interaction to both short-term and long-term memory.
        """
        # Save to short-term (for immediate context)
        self.short_term.add_message("user", user_query)
        self.short_term.add_message("assistant", assistant_response)
        
        # Save to long-term (for future recall)
        memory_text = f"User asked: {user_query}\nAssistant answered: {assistant_response}"
        self.long_term.save_memory(memory_text, {"type": "conversation_history"})

    def get_context(self, query: str) -> str:
        """
        Retrieves context from both short-term and long-term memory.
        """
        # 1. Get recent conversation history
        history = self.short_term.format_for_prompt()
        
        # 2. Recall relevant past interactions
        memories = self.long_term.recall(query, k=2)
        formatted_memories = ""
        if memories:
            formatted_memories = "\nRelevant Past Memories:\n"
            for m in memories:
                formatted_memories += f"- {m['content']}\n"
                
        return history + formatted_memories

if __name__ == "__main__":
    # Test
    manager = MemoryManager(max_short_term=2)
    manager.add_interaction("What is your name?", "I am TinyGPT assistant.")
    manager.add_interaction("What do you like?", "I like processing information.")
    
    print("\n--- Current Context for 'What do you know about me?' ---")
    print(manager.get_context("What do you know about me?"))
