import asyncio
from typing import Any

from src.code_agent.nodes import node_search as search_module


def test_node_search_returns_feedback(monkeypatch: Any):
    # Mock init_chat_model to return a dummy llm
    def fake_init_chat_model(*_args: Any, **_kwargs: Any):
        return object()

    # Mock create_react_agent to return an object with ainvoke
    class DummyAgent:
        async def ainvoke(self, _payload: Any):
            return {"messages": [object(), object(), type("M", (), {"content": "found"})()]}

    def fake_create_react_agent(*_args: Any, **_kwargs: Any):
        return DummyAgent()

    monkeypatch.setattr(search_module, "init_chat_model", fake_init_chat_model)
    monkeypatch.setattr(search_module, "create_react_agent", fake_create_react_agent)

    state = {
        "messages": ["m"],
        "code": "print()",
        "error_message": "",
        "feedback": "",
    }

    async def run():
        return await search_module.node_search(state)  # type: ignore[arg-type]

    res = asyncio.run(run())
    assert res["feedback"] == "found"

