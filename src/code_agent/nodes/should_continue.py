from ..states_outputs.states import StateCode


def should_continue(state: StateCode) -> str:
    # Garantir que `interactions` seja um inteiro (pode ser None no state)
    interactions_value = state.get("interactions")

    interactions: int = int(interactions_value) if interactions_value is not None else 0

    valid = state.get("valid")

    if valid is True or interactions >= 2:
        return "END"

    return "supervisor"
