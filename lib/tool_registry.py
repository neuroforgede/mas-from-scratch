from typing import Any, Optional, Dict, TypedDict

class ToolType(TypedDict):
    func: Any
    description: str
    example_usage: str

class ToolDescription(TypedDict):
    description: str
    example_usage: str


class ToolRegistry:
    tools: Dict[str, ToolType]

    """
    A centralized registry for managing tools.
    """
    def __init__(self):
        self.tools = {}

    def register_tool(
        self,
        name: str,
        tool_func: Any,
        description: Optional[str] = None,
        example_usage: Optional[str] = None
    ) -> None:
        """
        Register a tool with the registry.
        """
        self.tools[name] = {
            "func": tool_func,
            "description": description or "No description provided.",
            "example_usage": example_usage or "No example usage provided."
        }

    def get_tool(self, name: str) -> Any:
        """
        Retrieve a tool by name.
        """
        return self.tools.get(name)

    def list_tools(self) -> Dict[str, ToolDescription]:
        """
        List all available tools with their descriptions and example usage.
        """
        return {name: {
            "description": info["description"],
            "example_usage": info["example_usage"]
        } for name, info in self.tools.items()}

    def call_tool(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """
        Call a tool by name with the provided arguments.
        """
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found.")
        return tool["func"](*args, **kwargs)
