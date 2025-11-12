"""Testes para o módulo node_supervisor."""
import asyncio
from typing import Any

import pytest
from langchain_core.messages import HumanMessage

from src.code_agent.nodes import node_supervisor as supervisor_module
from src.code_agent.states_outputs.output_structured import SupervisorResponse
from src.code_agent.states_outputs.states import StateCode


class TestNodeSupervisor:
    """Testes para a função node_supervisor."""

    @pytest.mark.asyncio
    async def test_node_supervisor_returns_feedback_and_valid_from_dict(self, monkeypatch: Any):
        """Testa que node_supervisor retorna feedback e valid quando router retorna dict."""
        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"feedback": "Code looks good", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
            "interactions": 0,
        }

        result = await supervisor_module.node_supervisor(state)

        assert result["feedback"] == "Code looks good"
        assert result["valid"] is True
        assert result["interactions"] == 1

    @pytest.mark.asyncio
    async def test_node_supervisor_returns_feedback_and_valid_from_pydantic(self, monkeypatch: Any):
        """Testa que node_supervisor retorna feedback e valid quando router retorna Pydantic."""
        supervisor_response = SupervisorResponse(valid=False, feedback="Needs improvement")

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return supervisor_response

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "x = 1",
            "interactions": 0,
        }

        result = await supervisor_module.node_supervisor(state)

        assert result["feedback"] == "Needs improvement"
        assert result["valid"] is False
        assert result["interactions"] == 1

    @pytest.mark.asyncio
    async def test_node_supervisor_increments_interactions(self, monkeypatch: Any):
        """Testa que node_supervisor incrementa o contador de interações."""
        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"feedback": "ok", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
            "interactions": 5,
        }

        result = await supervisor_module.node_supervisor(state)

        assert result["interactions"] == 6

    @pytest.mark.asyncio
    async def test_node_supervisor_handles_none_interactions(self, monkeypatch: Any):
        """Testa que node_supervisor trata interactions None como 0."""
        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                return {"feedback": "ok", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
        }

        result = await supervisor_module.node_supervisor(state)

        assert result["interactions"] == 1

    @pytest.mark.asyncio
    async def test_node_supervisor_uses_last_message(self, monkeypatch: Any):
        """Testa que node_supervisor usa apenas a última mensagem."""
        captured_prompt = []

        class DummyRouter:
            def __init__(self, prompt: str, *_args: Any, **_kwargs: Any):
                self.prompt = prompt

            async def llm_router(self):
                captured_prompt.append(self.prompt)
                return {"feedback": "ok", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [
                HumanMessage(content="first message"),
                HumanMessage(content="last message"),
            ],
            "code": "print('ok')",
            "interactions": 0,
        }

        await supervisor_module.node_supervisor(state)

        assert len(captured_prompt) == 1
        assert "last message" in captured_prompt[0]

    @pytest.mark.asyncio
    async def test_node_supervisor_includes_code_in_prompt(self, monkeypatch: Any):
        """Testa que node_supervisor inclui o código no prompt."""
        captured_prompt = []

        class DummyRouter:
            def __init__(self, prompt: str, *_args: Any, **_kwargs: Any):
                self.prompt = prompt

            async def llm_router(self):
                captured_prompt.append(self.prompt)
                return {"feedback": "ok", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "def hello():\n    print('world')",
            "interactions": 0,
        }

        await supervisor_module.node_supervisor(state)

        assert len(captured_prompt) == 1
        assert "def hello():" in captured_prompt[0]
        assert "print('world')" in captured_prompt[0]

    @pytest.mark.asyncio
    async def test_node_supervisor_retries_on_invalid_response(self, monkeypatch: Any):
        """Testa que node_supervisor tenta novamente quando a resposta é inválida."""
        call_count = []

        class DummyRouter:
            def __init__(self, *_args: Any, **_kwargs: Any):
                pass

            async def llm_router(self):
                call_count.append(1)
                # Primeira chamada retorna resposta inválida, segunda retorna válida
                if len(call_count) == 1:
                    return {"invalid_key": "value"}
                return {"feedback": "ok", "valid": True}

        monkeypatch.setattr(supervisor_module, "LlmRouter", DummyRouter)

        state: StateCode = {
            "messages": [HumanMessage(content="test")],
            "code": "print('ok')",
            "interactions": 0,
        }

        result = await supervisor_module.node_supervisor(state)

        assert len(call_count) == 2
        assert result["feedback"] == "ok"
        assert result["valid"] is True
