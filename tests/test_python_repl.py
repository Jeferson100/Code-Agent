from typing import cast

from src.code_agent.nodes.node_python import python_repl
from src.code_agent.states_outputs.states import StateCode


def test_python_repl_executes_simple_code():
    state = cast(StateCode, {
        "messages": ["calc"],
        "code": "result = 2 + 2\nprint(result)",
        "imports": "",
    })

    # Should not raise and should return None on success
    assert python_repl(state) is None


def test_python_repl_handles_error_returns_error_message():
    state = cast(StateCode, {
        "messages": ["calc"],
        "code": "raise ValueError('boom')",
        "imports": "",
    })

    result = python_repl(state)
    assert isinstance(result, dict)
    assert "error_message" in result
    assert isinstance(result["error_message"], list)

