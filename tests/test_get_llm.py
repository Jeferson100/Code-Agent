"""Testes para o módulo get_llm."""
import asyncio
import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from src.code_agent.get_routem_llm.get_llm import GetLlmResponse


class DummyModel(BaseModel):
    """Modelo dummy para testes."""
    a: int


class TestGetLlmResponse:
    """Testes para a classe GetLlmResponse."""

    @pytest.mark.asyncio
    async def test_llm_structured_groq_returns_parsed_json(self, monkeypatch: Any):
        """Testa que llm_structured_groq retorna JSON parseado."""
        class DummyChoices:
            def __init__(self, content: str):
                self.message = type("M", (), {"content": content})()

        class DummyCompletions:
            async def create(self, **kwargs: Any):
                content = '{"a": 42}'
                return type("R", (), {"choices": [DummyChoices(content)]})()

        class DummyChat:
            def __init__(self):
                self.completions = DummyCompletions()

        class DummyClient:
            def __init__(self):
                self.chat = DummyChat()

        import src.code_agent.get_routem_llm.get_llm as gl
        monkeypatch.setattr(gl, "client", DummyClient())

        g = GetLlmResponse("hi", "model", strutured_output=DummyModel)

        result = await g.llm_structured_groq()

        assert result == {"a": 42}
        assert isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_llm_groq_returns_string(self, monkeypatch: Any):
        """Testa que llm_groq retorna string."""
        class DummyChoices:
            def __init__(self, content: str):
                self.message = type("M", (), {"content": content})()

        class DummyCompletions:
            async def create(self, **kwargs: Any):
                content = "Hello, world!"
                return type("R", (), {"choices": [DummyChoices(content)]})()

        class DummyChat:
            def __init__(self):
                self.completions = DummyCompletions()

        class DummyClient:
            def __init__(self):
                self.chat = DummyChat()

        import src.code_agent.get_routem_llm.get_llm as gl
        monkeypatch.setattr(gl, "client", DummyClient())

        g = GetLlmResponse("hi", "model")

        result = await g.llm_groq()

        assert result == "Hello, world!"
        assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_llm_structured_groq_raises_error_when_no_structured_output(self):
        """Testa que llm_structured_groq levanta erro quando structured_output não está definido."""
        g = GetLlmResponse("hi", "model", strutured_output=None)

        with pytest.raises(ValueError, match="structured_output precisa estar definido"):
            await g.llm_structured_groq()

    @pytest.mark.asyncio
    async def test_llm_structured_groq_handles_empty_content(self, monkeypatch: Any):
        """Testa que llm_structured_groq lida com conteúdo vazio."""
        class DummyChoices:
            def __init__(self, content: str):
                self.message = type("M", (), {"content": content})()

        class DummyCompletions:
            async def create(self, **kwargs: Any):
                content = None
                return type("R", (), {"choices": [DummyChoices(content)]})()

        class DummyChat:
            def __init__(self):
                self.completions = DummyCompletions()

        class DummyClient:
            def __init__(self):
                self.chat = DummyChat()

        import src.code_agent.get_routem_llm.get_llm as gl
        monkeypatch.setattr(gl, "client", DummyClient())

        g = GetLlmResponse("hi", "model", strutured_output=DummyModel)

        result = await g.llm_structured_groq()

        assert result == {}

    @pytest.mark.asyncio
    async def test_llm_groq_handles_empty_content(self, monkeypatch: Any):
        """Testa que llm_groq lida com conteúdo vazio."""
        class DummyChoices:
            def __init__(self, content: str):
                self.message = type("M", (), {"content": content})()

        class DummyCompletions:
            async def create(self, **kwargs: Any):
                content = None
                return type("R", (), {"choices": [DummyChoices(content)]})()

        class DummyChat:
            def __init__(self):
                self.completions = DummyCompletions()

        class DummyClient:
            def __init__(self):
                self.chat = DummyChat()

        import src.code_agent.get_routem_llm.get_llm as gl
        monkeypatch.setattr(gl, "client", DummyClient())

        g = GetLlmResponse("hi", "model")

        result = await g.llm_groq()

        assert result == ""

    @pytest.mark.asyncio
    async def test_llm_pydantic_structured_returns_result(self, monkeypatch: Any):
        """Testa que llm_pydantic_structured retorna resultado."""
        class DummyAgent:
            def run_sync(self, messages: str):
                return DummyModel(a=10)

        class DummyModelClass:
            def __init__(self, model: str):
                pass

        def fake_huggingface_model(model: str):
            return DummyModelClass(model)

        def fake_agent(model, output_type):
            return DummyAgent()

        with patch("src.code_agent.get_routem_llm.get_llm.HuggingFaceModel", fake_huggingface_model):
            with patch("src.code_agent.get_routem_llm.get_llm.Agent", fake_agent):
                g = GetLlmResponse("hi", "model", strutured_output=DummyModel)
                result = await g.llm_pydantic_structured()

                assert isinstance(result, DummyModel)
                assert result.a == 10

    @pytest.mark.asyncio
    async def test_llm_pydantic_structured_raises_error_when_no_structured_output(self):
        """Testa que llm_pydantic_structured levanta erro quando structured_output não está definido."""
        g = GetLlmResponse("hi", "model", strutured_output=None)

        with pytest.raises(ValueError, match="structured_output precisa estar definido"):
            await g.llm_pydantic_structured()

    @pytest.mark.asyncio
    async def test_llm_pydantic_returns_result(self, monkeypatch: Any):
        """Testa que llm_pydantic retorna resultado."""
        class DummyStream:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *args):
                pass

            async def stream_output(self):
                yield {"mock": "stream_response"}

        class DummyAgent:
            async def run_stream(self, messages: str):
                return DummyStream()

        class DummyModelClass:
            def __init__(self, model: str):
                pass

        def fake_huggingface_model(model: str):
            return DummyModelClass(model)

        def fake_agent(model):
            return DummyAgent()

        with patch("src.code_agent.get_routem_llm.get_llm.HuggingFaceModel", fake_huggingface_model):
            with patch("src.code_agent.get_routem_llm.get_llm.Agent", fake_agent):
                g = GetLlmResponse("hi", "model")
                result = await g.llm_pydantic()

                assert result == {"mock": "stream_response"}
