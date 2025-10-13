from typing import cast

from src.code_agent.nodes.should_continue import should_continue
from src.code_agent.states_outputs.states import StateCode


def test_should_continue_when_valid_true_returns_return_messages():
    state = cast(StateCode, {"valid": True, "interactions": 1, "messages": []})
    assert should_continue(state) == "return_messages"


def test_should_continue_when_interactions_gte_2_returns_return_messages():
    state = cast(StateCode, {"valid": False, "interactions": 2, "messages": []})
    assert should_continue(state) == "return_messages"


def test_should_continue_when_invalid_and_interactions_eq_3_returns_return_messages():
    state = cast(StateCode, {"valid": False, "interactions": 3, "messages": []})
    assert should_continue(state) == "return_messages"


def test_should_continue_default_returns_code():
    state = cast(StateCode, {"valid": False, "interactions": 1, "messages": []})
    assert should_continue(state) == "code"

