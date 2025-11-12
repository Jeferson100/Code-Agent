"""Testes para o módulo routem_llm."""
import asyncio
from typing import Any

import pytest
from pydantic import BaseModel

from src.code_agent.get_routem_llm.routem_llm import AllProvidersFailedError, LlmRouter


class DummyModel(BaseModel):
    """Modelo dummy para testes."""
    value: str


class TestLlmRouter:
    """Testes para a classe LlmRouter."""

    @pytest.mark.asyncio
    async def test_llm_router_tries_cerebras_first(self, monkeypatch: Any):
        """Testa que llm_router tenta Cerebras primeiro."""
        calls: list[str] = []

        class DummyCerebras:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def get_response_cerebras_async(self):
                calls.append("cerebras")
                return '{"result": "cerebras"}'

            async def get_response_cerebras_structured_async(self):
                calls.append("cerebras_structured")
                return DummyModel(value="cerebras")

        class DummyNvidia:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_nvidia(self):
                calls.append("nvidia")
                return "nvidia"

            async def llm_nvidia_structured(self):
                calls.append("nvidia_structured")
                return DummyModel(value="nvidia")

        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                calls.append("groq")
                return "groq"

            async def llm_structured_groq(self):
                calls.append("groq_structured")
                return {"result": "groq"}

        class DummyHF:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_pydanticai(self):
                calls.append("hf")
                return "hf"

            async def llm_structured_pydanticai(self):
                calls.append("hf_structured")
                return DummyModel(value="hf")

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rc(*a: Any, **k: Any):
            return DummyCerebras()

        def _rn(*a: Any, **k: Any):
            return DummyNvidia()

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        def _rh(*a: Any, **k: Any):
            return DummyHF()

        monkeypatch.setattr(rl, "RouterCerebras", _rc)
        monkeypatch.setattr(rl, "RouterNvidia", _rn)
        monkeypatch.setattr(rl, "RouterGroq", _rg)
        monkeypatch.setattr(rl, "RouterPydanticAI", _rh)

        router = LlmRouter("msg")

        result = await router.llm_router()

        assert "cerebras" in calls or "cerebras_structured" in calls
        assert result is not None

    @pytest.mark.asyncio
    async def test_llm_router_falls_back_to_nvidia_on_cerebras_failure(self, monkeypatch: Any):
        """Testa que llm_router faz fallback para Nvidia quando Cerebras falha."""
        calls: list[str] = []

        class DummyCerebras:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def get_response_cerebras_async(self):
                calls.append("cerebras")
                raise RuntimeError("cerebras failed")

            async def get_response_cerebras_structured_async(self):
                calls.append("cerebras_structured")
                raise RuntimeError("cerebras failed")

        class DummyNvidia:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_nvidia(self):
                calls.append("nvidia")
                return "nvidia success"

            async def llm_nvidia_structured(self):
                calls.append("nvidia_structured")
                return DummyModel(value="nvidia")

        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                calls.append("groq")
                return "groq"

        class DummyHF:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_pydanticai(self):
                calls.append("hf")
                return "hf"

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rc(*a: Any, **k: Any):
            return DummyCerebras()

        def _rn(*a: Any, **k: Any):
            return DummyNvidia()

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        def _rh(*a: Any, **k: Any):
            return DummyHF()

        monkeypatch.setattr(rl, "RouterCerebras", _rc)
        monkeypatch.setattr(rl, "RouterNvidia", _rn)
        monkeypatch.setattr(rl, "RouterGroq", _rg)
        monkeypatch.setattr(rl, "RouterPydanticAI", _rh)

        router = LlmRouter("msg")

        result = await router.llm_router()

        assert "cerebras" in calls or "cerebras_structured" in calls
        assert "nvidia" in calls or "nvidia_structured" in calls
        assert result == "nvidia success" or isinstance(result, DummyModel)

    @pytest.mark.asyncio
    async def test_llm_router_falls_back_through_all_providers(self, monkeypatch: Any):
        """Testa que llm_router faz fallback através de todos os provedores."""
        calls: list[str] = []

        class DummyCerebras:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def get_response_cerebras_async(self):
                calls.append("cerebras")
                raise RuntimeError("fail")

        class DummyNvidia:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_nvidia(self):
                calls.append("nvidia")
                raise RuntimeError("fail")

        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                calls.append("groq")
                return "groq success"

        class DummyHF:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_pydanticai(self):
                calls.append("hf")
                return "hf"

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rc(*a: Any, **k: Any):
            return DummyCerebras()

        def _rn(*a: Any, **k: Any):
            return DummyNvidia()

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        def _rh(*a: Any, **k: Any):
            return DummyHF()

        monkeypatch.setattr(rl, "RouterCerebras", _rc)
        monkeypatch.setattr(rl, "RouterNvidia", _rn)
        monkeypatch.setattr(rl, "RouterGroq", _rg)
        monkeypatch.setattr(rl, "RouterPydanticAI", _rh)

        router = LlmRouter("msg")

        result = await router.llm_router()

        assert "cerebras" in calls
        assert "nvidia" in calls
        assert "groq" in calls
        assert result == "groq success"

    @pytest.mark.asyncio
    async def test_llm_router_raises_error_when_all_providers_fail(self, monkeypatch: Any):
        """Testa que llm_router levanta erro quando todos os provedores falham."""
        class DummyCerebras:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def get_response_cerebras_async(self):
                raise RuntimeError("cerebras failed")

        class DummyNvidia:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_nvidia(self):
                raise RuntimeError("nvidia failed")

        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                raise RuntimeError("groq failed")

        class DummyHF:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_pydanticai(self):
                raise RuntimeError("hf failed")

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rc(*a: Any, **k: Any):
            return DummyCerebras()

        def _rn(*a: Any, **k: Any):
            return DummyNvidia()

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        def _rh(*a: Any, **k: Any):
            return DummyHF()

        monkeypatch.setattr(rl, "RouterCerebras", _rc)
        monkeypatch.setattr(rl, "RouterNvidia", _rn)
        monkeypatch.setattr(rl, "RouterGroq", _rg)
        monkeypatch.setattr(rl, "RouterPydanticAI", _rh)

        router = LlmRouter("msg")

        with pytest.raises(AllProvidersFailedError):
            await router.llm_router()

    @pytest.mark.asyncio
    async def test_llm_router_uses_structured_output_when_provided(self, monkeypatch: Any):
        """Testa que llm_router usa structured_output quando fornecido."""
        calls: list[str] = []

        class DummyCerebras:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def get_response_cerebras_structured_async(self):
                calls.append("cerebras_structured")
                return DummyModel(value="success")

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rc(*a: Any, **k: Any):
            return DummyCerebras()

        monkeypatch.setattr(rl, "RouterCerebras", _rc)

        router = LlmRouter("msg", strutured_output=DummyModel(value="dummy"))

        result = await router.llm_router()

        assert "cerebras_structured" in calls
        assert isinstance(result, DummyModel) or isinstance(result, dict)

    @pytest.mark.asyncio
    async def test_try_groq_models_returns_on_success(self, monkeypatch: Any):
        """Testa que try_groq_models retorna resultado quando bem-sucedido."""
        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                return "groq success"

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        monkeypatch.setattr(rl, "RouterGroq", _rg)

        router = LlmRouter("msg", groq_models=["model1"])

        result = await router.try_groq_models()

        assert result == "groq success"

    @pytest.mark.asyncio
    async def test_try_groq_models_continues_on_failure(self, monkeypatch: Any):
        """Testa que try_groq_models continua tentando quando um modelo falha."""
        call_count = 0

        class DummyGroq:
            def __init__(self, *_a: Any, **_k: Any):
                pass

            async def llm_groq(self):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise RuntimeError("model1 failed")
                return "groq success"

        import src.code_agent.get_routem_llm.routem_llm as rl

        def _rg(*a: Any, **k: Any):
            return DummyGroq()

        monkeypatch.setattr(rl, "RouterGroq", _rg)

        router = LlmRouter("msg", groq_models=["model1", "model2"])

        result = await router.try_groq_models()

        assert result == "groq success"
        assert call_count == 2
