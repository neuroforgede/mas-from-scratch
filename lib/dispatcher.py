from concurrent.futures import ThreadPoolExecutor
from termcolor import colored


class Dispatcher:
    """
    A dispatcher to manage message passing and shared state.
    """
    def __init__(self, shared_state):
        self.agents = {}
        self.shared_state = shared_state

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def dispatch(self, start_agent_name, initial_message):
        current_agent_name = start_agent_name
        message = initial_message

        with ThreadPoolExecutor() as executor:
            while current_agent_name:
                agent = self.agents.get(current_agent_name)
                if not agent:
                    print(colored(
                        f"[Dispatcher] No agent found with name: {current_agent_name}",
                        "red", attrs=["bold"])
                    )
                    break

                # currently this is slightly pointless to do in a separate thread...

                # Call the agent in a separate thread
                future = executor.submit(agent.act, self.shared_state, message)
                message = future.result()  # Wait for the agent to complete

                print(colored(
                    f"\n[Dispatcher] Dispatching to next agent: {message.next_agent}",
                    "blue", attrs=["bold"])
                )
                current_agent_name = message.next_agent
