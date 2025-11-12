"""Testes para os módulos de tools."""
from typing import Any

import pytest
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.code_agent.states_outputs.states import DeepAgentState, Todo
from src.code_agent.tools import think_tavily, todos, tool_write_code


class TestThinkTavily:
    """Testes para o módulo think_tavily."""

    def test_web_search_returns_results(self, monkeypatch: Any):
        """Testa que web_search retorna resultados."""
        class DummyTavilyClient:
            def __init__(self, api_key: str | None = None):
                pass

            def search(self, query: str, max_results: int = 5, include_images: bool = False):
                return {
                    "results": [
                        {
                            "title": "Test Title",
                            "content": "Test content",
                            "url": "https://test.com"
                        }
                    ]
                }

        monkeypatch.setattr(think_tavily, "TavilyClient", DummyTavilyClient)
        monkeypatch.setenv("TAVILY_API_KEY", "test_key")

        result = think_tavily.web_search.invoke({"query": "test query"})

        assert isinstance(result, list)
        assert len(result) > 0
        assert "title" in result[0]
        assert "content" in result[0]
        assert "url" in result[0]

    def test_web_search_raises_error_when_no_api_key(self, monkeypatch: Any):
        """Testa que web_search levanta erro quando não há API key."""
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)

        with pytest.raises(ValueError, match="TAVILY_API_KEY not found"):
            think_tavily.web_search.invoke({"query": "test"})

    def test_web_search_handles_api_error(self, monkeypatch: Any):
        """Testa que web_search lida com erro da API."""
        class DummyTavilyClient:
            def __init__(self, api_key: str | None = None):
                pass

            def search(self, query: str, max_results: int = 5, include_images: bool = False):
                raise Exception("API Error")

        monkeypatch.setattr(think_tavily, "TavilyClient", DummyTavilyClient)
        monkeypatch.setenv("TAVILY_API_KEY", "test_key")

        result = think_tavily.web_search.invoke({"query": "test"})

        assert isinstance(result, list)
        assert len(result) > 0
        assert "Error" in result[0] or "error" in result[0].lower()

    def test_think_tool_returns_confirmation(self):
        """Testa que think_tool retorna confirmação."""
        result = think_tavily.think_tool.invoke({"reflection": "test reflection"})

        assert isinstance(result, str)
        assert "Reflection recorded" in result
        assert "test reflection" in result

    def test_think_response_returns_confirmation(self):
        """Testa que think_response retorna confirmação."""
        result = think_tavily.think_response.invoke({"reflection": "test analysis"})

        assert isinstance(result, str)
        assert "Analysis processed" in result
        assert "test analysis" in result


class TestTodos:
    """Testes para o módulo todos."""

    def test_write_todos_returns_command(self):
        """Testa que write_todos retorna Command."""
        todos_list: list[Todo] = [
            {"content": "Task 1", "status": "pending"},
            {"content": "Task 2", "status": "in_progress"},
        ]

        result = todos.write_todos.invoke({
            "todos": todos_list,
            "tool_call_id": "test_id"
        })

        assert isinstance(result, Command)
        assert hasattr(result, "update")
        update = result.update
        assert "todos" in update
        assert update["todos"] == todos_list
        assert "messages" in update

    def test_read_todos_returns_formatted_string(self, monkeypatch: Any):
        """Testa que read_todos retorna string formatada."""
        todos_list: list[Todo] = [
            {"content": "Task 1", "status": "pending"},
            {"content": "Task 2", "status": "completed"},
        ]

        state: DeepAgentState = {
            "messages": [],
            "todos": todos_list,
        }

        # Mock InjectedState para retornar o state
        def mock_read_todos(state_param, tool_call_id):
            return todos.read_todos.func(state_param, tool_call_id)

        result = mock_read_todos(state, "test_id")

        assert isinstance(result, str)
        assert "Task 1" in result
        assert "Task 2" in result
        assert "pending" in result or "⏳" in result
        assert "completed" in result or "✅" in result

    def test_read_todos_returns_message_when_empty(self, monkeypatch: Any):
        """Testa que read_todos retorna mensagem quando lista está vazia."""
        state: DeepAgentState = {
            "messages": [],
            "todos": [],
        }

        def mock_read_todos(state_param, tool_call_id):
            return todos.read_todos.func(state_param, tool_call_id)

        result = mock_read_todos(state, "test_id")

        assert isinstance(result, str)
        assert "No todos" in result or "no todos" in result.lower()


class TestToolWriteCode:
    """Testes para o módulo tool_write_code."""

    @pytest.mark.asyncio
    async def test_write_code_returns_command_on_success(self, monkeypatch: Any):
        """Testa que write_code retorna Command quando bem-sucedido."""
        class DummyGraph:
            async def ainvoke(self, state: Any):
                return {
                    "messages": [
                        HumanMessage(content="Generated code: print('hello')")
                    ]
                }

        monkeypatch.setattr(tool_write_code, "graph_build", DummyGraph())

        state: DeepAgentState = {
            "messages": [],
            "code_interactions": 0,
        }

        # Mock InjectedState para retornar o state
        def mock_write_code(query_param, state_param, tool_call_id):
            return tool_write_code.write_code.func(query_param, state_param, tool_call_id)

        result = mock_write_code("write hello world", state, "test_id")

        assert isinstance(result, Command)
        assert hasattr(result, "update")
        update = result.update
        assert "code_interactions" in update
        assert update["code_interactions"] == 1
        assert "messages" in update

    @pytest.mark.asyncio
    async def test_write_code_respects_interaction_limit(self, monkeypatch: Any):
        """Testa que write_code respeita o limite de interações."""
        state: DeepAgentState = {
            "messages": [],
            "code_interactions": 3,
        }

        def mock_write_code(query_param, state_param, tool_call_id):
            return tool_write_code.write_code.func(query_param, state_param, tool_call_id)

        result = mock_write_code("write code", state, "test_id")

        assert isinstance(result, Command)
        update = result.update
        assert "code_interactions" in update
        assert update["code_interactions"] == 3
        assert "messages" in update
        message = update["messages"][0]
        assert "limit" in message.content.lower() or "3" in message.content

    @pytest.mark.asyncio
    async def test_write_code_handles_errors(self, monkeypatch: Any):
        """Testa que write_code lida com erros."""
        class DummyGraph:
            async def ainvoke(self, state: Any):
                raise Exception("Graph error")

        monkeypatch.setattr(tool_write_code, "graph_build", DummyGraph())

        state: DeepAgentState = {
            "messages": [],
            "code_interactions": 0,
        }

        def mock_write_code(query_param, state_param, tool_call_id):
            return tool_write_code.write_code.func(query_param, state_param, tool_call_id)

        result = mock_write_code("write code", state, "test_id")

        assert isinstance(result, str)
        assert "Error" in result or "error" in result.lower()

