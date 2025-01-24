from typing import Any, Optional, TypedDict, Literal

class SharedStateType(TypedDict, total=False):
    user_input: str
    business_plan: str
    business_feedback: str

SharedStateTypeKey = Literal["user_input", "business_plan", "business_feedback"]

ACTION_TYPE = Literal[
    "SET_USER_INPUT",
    "SET_BUSINESS_PLAN",
    "SET_BUSINESS_FEEDBACK"
]

class SharedState:
    """
    A shared state with a reducer pattern to manage updates.
    """
    def __init__(self, initial_state: Optional[SharedStateType] = None):
        self.state = {
            "user_input": None,
            "business_plan": None,
            "business_feedback": None
        }
        if initial_state is not None:
            for key in initial_state:
                self.state[key] = initial_state[key]

    def get(self, key: SharedStateTypeKey) -> Any:
        return self.state.get(key)

    def show(self) -> Any:
        """
        Display the current state.
        """
        return self.state

    def dispatch(self, action_type: ACTION_TYPE, payload: Any) -> None:
        """
        Dispatch an action to the reducer.
        """
        self.state = self.reducer(self.state, action_type, payload)

    @staticmethod
    def reducer(state: SharedStateType, action_type: ACTION_TYPE, payload: Any):
        """
        Reducer function to handle state transitions.
        """
        new_state = state.copy()

        state = action_type.lower().replace("set_", "")
        if state in new_state:
            new_state[action_type.lower().replace("set_", "")] = payload
        else:
            print(f"[Reducer] Unknown action type: {action_type}")

        return new_state
