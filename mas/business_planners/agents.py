from lib.message import Message
from lib.tool_registry import ToolRegistry
from lib.llm import query_llm
from mas.business_planners.shared_state import SharedState

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


class BusinessPlanner(Agent):
    def act(self, shared_state: SharedState, message: Optional[str]) -> Message:
        plan = shared_state.get("business_plan")

        # Following could be actually separated into 2 agents
        # one is for first generation, another for fixing
        if plan is not None:  # Check if it's first run
            # Generate code using LLM
            plan = query_llm([
                {
                    "role": "system",
                    "content": f"""
                        You are a professional business consultant.
                        You have to fix the following business plan according to the feedback.
                        Return only the fixed business plan, without any extra comments.
                        Plan: {plan}
                        Feedback: {shared_state.get("business_feedback")}"""
                }], max_tokens=10000)
        else:
            user_input = shared_state.get("user_input")
            print(f"[{self.name}] Received input: {user_input}")

            # Generate plan using LLM
            plan = query_llm([
                {
                    "role": "system",
                    "content": f"""
                        You are a professional business consultant.
                        Write a short business plan based on the following user input.
                        User input: {user_input}
                        """
                }], max_tokens=10000)
        print(f"[{self.name}] Generated plan:\n{plan}")

        shared_state.dispatch("SET_BUSINESS_PLAN", plan)
        return Message(content=plan, next_agent="BusinessAdvisor")


class BusinessAdvisor(Agent):
    def act(self, shared_state: SharedState, message: Optional[str]) -> Message:
        plan = shared_state.get("business_plan")
        print(colored(f"[{self.name}] Validating plan:\n{plan}", "blue", attrs=["bold"]))

        # Validate
        feedback = query_llm([
            {
                "role": "system",
                "content": f"""
                    You are a professional business advisor. Your task is to evaluate the following business plan.
                    Here are the criteria:
                    - plan is concise and clear;
                    - it has dates and approximate timelines with revenue estimates;
                    - it lists main possible risks and provides solutions.
                    - it has exact amount of people needed to hire and their roles.
                    - it has a unique and catchy name of the company.
                    In case the plan fits all the criteria, write only the phrase "Good job!".
                    Otherwise, provide feedback on what is missing.
                    Plan: {plan}
                    """
            }], max_tokens=10000)
        

        shared_state.dispatch("SET_BUSINESS_FEEDBACK", feedback)
        if "good job" in feedback.lower():
            print(colored(
                "[{self.name}] Business plan analysis result: Good job!",
                "blue", attrs=["bold"])
            )
            return Message(content=feedback, next_agent=None)
        else:
            print(colored(
                f"[{self.name}] Business plan analysis result: Not good. {feedback}",
                "red", attrs=["bold"])
            )
            return Message(content=feedback, next_agent="BusinessPlanner")
        
