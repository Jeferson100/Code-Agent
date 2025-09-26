from ..states_outputs.states import StateCode


def should_continue(state: StateCode) -> str:
    interactions = state.get("interactions", 0)

    valid = state.get("valid")

    print(f"Debug - interactions: {interactions}, valid: {valid}")

    if valid is True:
        return "return_messages"

    if interactions >= 5:
        return "return_messages"

    if valid is False and interactions == 3:
        return "search"

    return "code"
