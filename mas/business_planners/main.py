from mas.business_planners.shared_state import SharedState
from mas.business_planners.agents import BusinessAdvisor, BusinessPlanner
from lib.dispatcher import Dispatcher
from lib.message import Message
from termcolor import colored
import yaml


# Initialize shared state
shared_state = SharedState({"user_input": "Write a business plan for SaaS company which provides CRM software."})

# Initialize agents with Azure OpenAI deployment name
business_planner_agent = BusinessPlanner("BusinessPlanner")
business_advisor_agent = BusinessAdvisor("BusinessAdvisor")

# Register agents with the dispatcher
dispatcher = Dispatcher(shared_state)
dispatcher.register_agent(business_planner_agent)
dispatcher.register_agent(business_advisor_agent)


# Start the workflow
print(colored("[System] Starting workflow...", on_color="on_white") + "\n")
initial_message = Message(content="Starting workflow", next_agent="BusinessPlanner")
dispatcher.dispatch(start_agent_name="BusinessPlanner", initial_message=initial_message)

# Display final shared state
print("\nFinal Shared State:")
print(yaml.dump(shared_state.show()))

print(colored(shared_state.get("business_plan"), "green", attrs=["underline"]))
