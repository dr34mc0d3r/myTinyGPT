from typing import List, Dict, Any

class ShortTermMemory:
    """
    Maintains a rolling window of the current conversation history.
    """
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """
        Adds a message to the history. Role is typically 'user' or 'assistant'.
        """
        self.history.append({"role": role, "content": content})
        # Maintain rolling window
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def format_for_prompt(self) -> str:
        """
        Formats the history into a string for LLM consumption.
        """
        if not self.history:
            return ""
            
        formatted = "Conversation History:\n"
        for msg in self.history:
            role_label = "User" if msg['role'] == 'user' else "Assistant"
            formatted += f"{role_label}: {msg['content']}\n"
        return formatted

    def clear(self):
        self.history = []

if __name__ == "__main__":
    # Test
    stm = ShortTermMemory(max_messages=3)
    stm.add_message("user", "Hi there!")
    stm.add_message("assistant", "Hello! How can I help you?")
    stm.add_message("user", "What is the weather?")
    stm.add_message("assistant", "It is sunny.")
    
    print(stm.format_for_prompt())
