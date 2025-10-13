from ..states_outputs.states import StateCode


def should_continue(state: StateCode) -> str:
    interactions = state.get("interactions", 0)

    valid = state.get("valid")

    if valid is True or interactions >= 2:
        return "return_messages"
    return "code"
