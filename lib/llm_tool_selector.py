from lib.llm import client
from pydantic import BaseModel

class ToolType(BaseModel):
    tool: str
    args: list[str]
    kwargs: dict[str, str]

class LLMToolSelector:
    """
    Uses an LLM to decide which tool to call.
    """
    def __init__(self, tool_registry, deployment_name):
        self.tool_registry = tool_registry
        self.deployment_name = deployment_name  # Azure-specific deployment name

    def decide_tool(self, user_input):
        """
        Query Azure OpenAI to decide which tool to call.
        """
        tools_metadata = self.tool_registry.list_tools()
        tools_description = "\n".join([
            f"{name}: {info['description']}. Example: {info['example_usage']}"
            for name, info in tools_metadata.items()
        ])

        prompt = (
            f"You are an intelligent assistant. Based on the user's input, decide which tool to use "
            f"from the list below and provide the arguments needed.\n\n"
            f"Available Tools:\n{tools_description}\n\n"
            f"User Input: {user_input}\n\n"
        )

        print("[LLMToolSelector] Sending prompt to Azure OpenAI.")
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=300,
            temperature=0.7,
            response_format=ToolType
        )
        print("[LLMToolSelector] Received response from Azure OpenAI.")

        # Parse the LLM's response
        if response.choices[0].message.refusal:
            print(f"[LLMToolSelector] Failed to parse LLM response: {str(response.choices[0].message.refusal)}")
            return None
        else:
            decision = response.choices[0].message.parsed
            return decision
