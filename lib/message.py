from typing import Optional
class Message:
    """
    A message that agents use to pass updates and determine the next step.
    """
    def __init__(self, content: Optional[str], next_agent: Optional[str] = None):
        self.content = content  # Content of the message
        self.next_agent = next_agent  # The next agent to execute, if any

    def __repr__(self):
        return f"Message(content={self.content}, next_agent={self.next_agent})"
