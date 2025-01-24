from lib.message import Message
from lib.tool_registry import ToolRegistry
from lib.llm import query_llm
from mas.coder_tester.shared_state import SharedState

from termcolor import colored
from typing import Optional

default_tools = ToolRegistry()


class Agent:
    """
    Base class for all agents.
    """
    def __init__(self, name: str):
        self.name = name

    def act(self, shared_state: SharedState, message: Optional[str]) -> Message:
        """
        Perform an action based on the incoming message and shared state.
        Must be implemented by subclasses.
        """
        raise NotImplementedError


class CodeGeneratorAgent(Agent):
    def act(self, shared_state: SharedState, message: Optional[str]) -> Message:
        code = shared_state.get("code")

        # Following could be actually separated into 2 agents
        # one is for first generation, another for fixing the code
        if code is not None:  # Check if it's first run
            # Generate code using LLM
            code = query_llm([
                {
                    "role": "system",
                    "content": f"""
                        You are an Agent that is tasked to fix python code.
                        Only ever produce the code directly, without any extra comments. Don't use code fences.
                        Based on the following code and its output, re-generate the code to fix any issues:
                        Code: {code}
                        Output: {shared_state.get("code_return")}"""
                }], max_tokens=10000)
            print(f"[CodeGeneratorAgent] Generated code:\n{code}")

            shared_state.dispatch("SET_CODE", code)
            return Message(content=code, next_agent="CodeValidatorAgent")
        else:
            user_input = shared_state.get("user_input")
            print(f"[CodeGeneratorAgent] Received plan: {user_input}")

            # Generate code using LLM
            code = query_llm([
                {
                    "role": "system",
                    "content": f"""
                        You are an Agent that is tasked to generate Python code based on a given user input.
                        Only ever produce the code directly, without any extra comments. Don't use code fences.
                        The input is the following: {user_input}"""
                }], max_tokens=10000)
            print(f"[CodeGeneratorAgent] Generated code:\n{code}")

            shared_state.dispatch("SET_CODE", code)
            return Message(content=code, next_agent="CodeValidatorAgent")


class CodeValidatorAgent(Agent):
    def act(self, shared_state: SharedState, message: Optional[str]) -> Message:
        code = shared_state.get("code")
        print(colored(f"[CodeValidatorAgent] Validating code:\n{code}", "blue", attrs=["bold"]))

        # Validate using a tool
        try:
            exec(code)
            code_return = ""
        except Exception as e:
            code_return = f"Execution failed: {str(e)}"

        shared_state.dispatch("SET_CODE_RETURN", code_return)
        if code_return == "":
            print(colored(
                "[CodeValidatorAgent] Validation result: Code executed correctly",
                "blue", attrs=["bold"])
            )
            return Message(content=code_return, next_agent=None)
        else:
            print(colored(
                f"[CodeValidatorAgent] Validation result: Code failed to execute: {code_return}",
                "red", attrs=["bold"])
            )
            return Message(content=code_return, next_agent="CodeGeneratorAgent")
