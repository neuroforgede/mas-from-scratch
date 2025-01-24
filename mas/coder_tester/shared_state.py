from typing import Any, Optional, TypedDict, Literal

class SharedStateType(TypedDict, total=False):
    user_input: str
    code: str
    code_return: str

SharedStateTypeKey = Literal["user_input", "code", "code_return"]

ACTION_TYPE = Literal[
    "SET_USER_INPUT",
    "SET_CODE",
    "SET_CODE_RETURN"
]

class SharedState:
    """
    A shared state with a reducer pattern to manage updates.
    """
    def __init__(self, initial_state: Optional[SharedStateType] = None):
        self.state = initial_state or {}

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

        # Following can be done in a smarter way
        if action_type == "SET_USER_INPUT":
            new_state["user_input"] = payload

        elif action_type == "SET_CODE_RETURN":
            new_state["code_return"] = payload

        elif action_type == "SET_CODE":
            new_state["code"] = payload
        
        else:
            print(f"[Reducer] Unknown action type: {action_type}")

        return new_state
