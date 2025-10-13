import asyncio
from typing import Any

from src.code_agent.nodes import node_return_message as return_module


def test_return_messages_returns_last_message(monkeypatch: Any):
    # Mock init_chat_model to return a dummy llm
    def fake_init_chat_model(*_args: Any, **_kwargs: Any):
        return object()

    # Mock create_react_agent to return an object with ainvoke
    class DummyAgent:
        async def ainvoke(self, _payload: Any):
            return {"messages": [object(), object(), type("M", (), {"content": "ok"})()]}

    def fake_create_react_agent(*_args: Any, **_kwargs: Any):
        return DummyAgent()

    # Mock TavilyClient to avoid API key error
    class DummyTavilyClient:
        def search(self, query: str):
            return {"results": [{"content": f"Mock search result for: {query}"}]}

    monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
    monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)
    
    # Mock the TavilyClient in the think_tavily module
    import src.code_agent.tools.think_tavily as tt
    monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

    state = {
        "messages": ["m"],
        "code": "print()",
        "feedback": "",
    }

    async def run():
        return await return_module.return_messages(state)  # type: ignore[arg-type]

    res = asyncio.run(run())
    assert isinstance(res["messages"], list)
    assert len(res["messages"]) == 1

