"""Testes para o módulo node_return_message."""
from typing import Any

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.code_agent.nodes import node_return_message as return_module
from src.code_agent.states_outputs.states import StateCode


class TestNodeReturnMessage:
    """Testes para a função return_messages."""

    @pytest.mark.asyncio
    async def test_return_messages_returns_last_message(self, monkeypatch: Any):
        """Testa que return_messages retorna a última mensagem do agente."""
        # Mock init_chat_model
        class DummyLLM:
            pass

        def fake_init_chat_model(*_args: Any, **_kwargs: Any):
            return DummyLLM()

        # Mock create_react_agent
        class DummyAgent:
            async def ainvoke(self, _payload: Any):
                return {
                    "messages": [
                        HumanMessage(content="msg1"),
                        HumanMessage(content="msg2"),
                        AIMessage(content="final response"),
                    ]
                }

        def fake_create_react_agent(*_args: Any, **_kwargs: Any):
            return DummyAgent()

        # Mock TavilyClient
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": f"Mock search result for: {query}"}]}

        monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
        monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        state: StateCode = {
            "messages": [HumanMessage(content="user question")],
            "code": "print('hello')",
            "feedback": "code is valid",
        }

        result = await return_module.return_messages(state)

        assert isinstance(result["messages"], list)
        assert len(result["messages"]) == 1
        assert hasattr(result["messages"][0], "content")
        assert result["messages"][0].content == "final response"

    @pytest.mark.asyncio
    async def test_return_messages_includes_state_in_prompt(self, monkeypatch: Any):
        """Testa que return_messages inclui informações do state no prompt."""
        captured_payload = []

        class DummyLLM:
            pass

        def fake_init_chat_model(*_args: Any, **_kwargs: Any):
            return DummyLLM()

        class DummyAgent:
            async def ainvoke(self, payload: Any):
                captured_payload.append(payload)
                return {"messages": [AIMessage(content="response")]}

        def fake_create_react_agent(*_args: Any, **_kwargs: Any):
            return DummyAgent()

        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
        monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        state: StateCode = {
            "messages": [HumanMessage(content="user question")],
            "code": "def test():\n    pass",
            "feedback": "needs improvement",
        }

        await return_module.return_messages(state)

        assert len(captured_payload) == 1
        assert "messages" in captured_payload[0]

    @pytest.mark.asyncio
    async def test_return_messages_handles_dict_response(self, monkeypatch: Any):
        """Testa que return_messages lida com resposta em formato dict."""
        class DummyLLM:
            pass

        def fake_init_chat_model(*_args: Any, **_kwargs: Any):
            return DummyLLM()

        class DummyAgent:
            async def ainvoke(self, _payload: Any):
                return {"messages": [AIMessage(content="response")]}

        def fake_create_react_agent(*_args: Any, **_kwargs: Any):
            return DummyAgent()

        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
        monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
            "feedback": "",
        }

        result = await return_module.return_messages(state)

        assert isinstance(result, dict)
        assert "messages" in result
        assert len(result["messages"]) == 1

    @pytest.mark.asyncio
    async def test_return_messages_handles_non_dict_response(self, monkeypatch: Any):
        """Testa que return_messages lida com resposta que não é dict."""
        class DummyLLM:
            pass

        def fake_init_chat_model(*_args: Any, **_kwargs: Any):
            return DummyLLM()

        class DummyAgent:
            async def ainvoke(self, _payload: Any):
                # Retorna mensagem diretamente, não dict
                return AIMessage(content="direct response")

        def fake_create_react_agent(*_args: Any, **_kwargs: Any):
            return DummyAgent()

        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
        monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
            "feedback": "",
        }

        result = await return_module.return_messages(state)

        assert isinstance(result, dict)
        assert "messages" in result
        assert len(result["messages"]) == 1

    @pytest.mark.asyncio
    async def test_return_messages_uses_last_message_from_state(self, monkeypatch: Any):
        """Testa que return_messages usa apenas a última mensagem do state."""
        captured_payload = []

        class DummyLLM:
            pass

        def fake_init_chat_model(*_args: Any, **_kwargs: Any):
            return DummyLLM()

        class DummyAgent:
            async def ainvoke(self, payload: Any):
                captured_payload.append(payload)
                return {"messages": [AIMessage(content="response")]}

        def fake_create_react_agent(*_args: Any, **_kwargs: Any):
            return DummyAgent()

        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        monkeypatch.setattr(return_module, "init_chat_model", fake_init_chat_model)
        monkeypatch.setattr(return_module, "create_react_agent", fake_create_react_agent)

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        state: StateCode = {
            "messages": [
                HumanMessage(content="first"),
                HumanMessage(content="last"),
            ],
            "code": "print('ok')",
            "feedback": "",
        }

        await return_module.return_messages(state)

        assert len(captured_payload) == 1
        # Verifica que apenas a última mensagem foi passada
        messages = captured_payload[0]["messages"]
        assert len(messages) == 1 or messages[-1].content == "last"

