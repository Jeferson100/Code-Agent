"""Testes para o módulo node_codes."""
from types import SimpleNamespace
from typing import Any

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.code_agent.nodes import node_codes as node_codes_module
from src.code_agent.states_outputs.output_structured import CodeOutput
from src.code_agent.states_outputs.states import StateCode


class TestNodeCode:
    """Testes para a função node_code."""

    @pytest.mark.asyncio
    async def test_node_code_returns_parsed_fields_from_dict(self, monkeypatch: Any):
        """Testa que node_code retorna campos parseados quando o router retorna dict."""
        # Mock llm_code.invoke
        class DummyResp:
            def __init__(self, content: str):
                self.content = content

        def fake_invoke(_prompt: str):
            return DummyResp('{"prefix": "p", "imports": "import os", "code": "print(\'ok\')"}')

        monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

        # Mock LlmRouter
        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"prefix": "p", "imports": "import os", "code": "print('ok')"}

        monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "feedback": "",
        }

        result = await node_codes_module.node_code(state)

        assert result["code"] == "print('ok')"
        assert result["imports"] == "import os"
        assert result["prefix"] == "p"
        assert isinstance(result["messages"], list)
        assert len(result["messages"]) == 1
        assert isinstance(result["messages"][0], AIMessage)

    @pytest.mark.asyncio
    async def test_node_code_returns_parsed_fields_from_pydantic(self, monkeypatch: Any):
        """Testa que node_code retorna campos parseados quando o router retorna Pydantic."""
        # Mock llm_code.invoke
        class DummyResp:
            def __init__(self, content: str):
                self.content = content

        def fake_invoke(_prompt: str):
            return DummyResp('{"prefix": "p", "imports": "", "code": "x = 1"}')

        monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

        # Mock LlmRouter retornando objeto Pydantic
        code_output = CodeOutput(code="x = 1", imports="", prefix="p")

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return code_output

        monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "feedback": "some feedback",
        }

        result = await node_codes_module.node_code(state)

        assert result["code"] == "x = 1"
        assert result["imports"] == ""
        assert result["prefix"] == "p"

    @pytest.mark.asyncio
    async def test_node_code_handles_empty_response(self, monkeypatch: Any):
        """Testa que node_code lida com resposta vazia ou inválida."""
        class DummyResp:
            def __init__(self, content: str):
                self.content = content

        def fake_invoke(_prompt: str):
            return DummyResp("")

        monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return None

        monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "feedback": "",
        }

        result = await node_codes_module.node_code(state)

        assert result["code"] == ""
        assert result["imports"] == ""
        assert result["prefix"] == ""

    @pytest.mark.asyncio
    async def test_node_code_uses_last_message(self, monkeypatch: Any):
        """Testa que node_code usa apenas a última mensagem."""
        class DummyResp:
            def __init__(self, content: str):
                self.content = content

        def fake_invoke(prompt: str):
            # Verifica que o prompt contém apenas a última mensagem
            assert "test message 2" in prompt
            return DummyResp('{"code": "result"}')

        monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"code": "result", "imports": "", "prefix": ""}

        monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [
                HumanMessage(content="test message 1"),
                HumanMessage(content="test message 2"),
            ],
            "feedback": "",
        }

        result = await node_codes_module.node_code(state)
        assert result["code"] == "result"

    @pytest.mark.asyncio
    async def test_node_code_includes_feedback_in_prompt(self, monkeypatch: Any):
        """Testa que node_code inclui feedback no prompt."""
        captured_prompt = []

        class DummyResp:
            def __init__(self, content: str):
                self.content = content

        def fake_invoke(prompt: str):
            captured_prompt.append(prompt)
            return DummyResp('{"code": "result"}')

        monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"code": "result", "imports": "", "prefix": ""}

        monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "feedback": "fix the bug",
        }

        await node_codes_module.node_code(state)

        assert len(captured_prompt) == 1
        assert "fix the bug" in captured_prompt[0]
