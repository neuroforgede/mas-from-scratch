from mas.coder_tester.shared_state import SharedState
from mas.coder_tester.agents import CodeGeneratorAgent, CodeValidatorAgent
from lib.dispatcher import Dispatcher
from lib.message import Message
from termcolor import colored
import yaml


# Initialize shared state
shared_state = SharedState({"user_input": "Write a program that implements fibonacci sequence calculation"})

# Initialize agents with Azure OpenAI deployment name
code_generator_agent = CodeGeneratorAgent("CodeGeneratorAgent")
code_validator_agent = CodeValidatorAgent("CodeValidatorAgent")

# Register agents with the dispatcher
dispatcher = Dispatcher(shared_state)
dispatcher.register_agent(code_generator_agent)
dispatcher.register_agent(code_validator_agent)


# Start the workflow
print(colored("[System] Starting workflow...", on_color="on_white") + "\n")
initial_message = Message(content="Starting workflow", next_agent="CodeGeneratorAgent")
dispatcher.dispatch(start_agent_name="CodeGeneratorAgent", initial_message=initial_message)

# Display final shared state
print("\nFinal Shared State:")
print(yaml.dump(shared_state.show()))

print(colored(shared_state.get("code"), "green", attrs=["underline"]))
