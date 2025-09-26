import asyncio
from typing import Any

from src.code_agent.nodes import node_supervisor as supervisor_module


def test_node_supervisor_returns_feedback_and_valid(monkeypatch: Any):
    class DummyRouter:
        def __init__(self, *_args: Any, **_kwargs: Any):
            pass

        async def llm_router(self):
            return {"feedback": "ok", "valid": True}

    monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

    state = {
        "messages": ["m"],
        "code": "print('ok')",
        "error_message": "",
        "interactions": 0,
    }
    async def run():
        return await supervisor_module.node_supervisor(state)  # type: ignore[arg-type]

    res = asyncio.run(run())
    assert res["feedback"] == "ok"
    assert res["valid"] is True
    assert res["interactions"] == 1

