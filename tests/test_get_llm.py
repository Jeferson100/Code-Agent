import asyncio
from typing import Any

from src.code_agent.get_routem_llm.get_llm import GetLlmResponse


def test_get_llm_groq_and_structured(monkeypatch: Any):
    # Stub AsyncGroq client inside module
    class DummyChoices:
        def __init__(self, content: str):
            self.message = type("M", (), {"content": content})()

    class DummyCompletions:
        async def create(self, **kwargs: Any):
            # Return structured content for structured calls, empty for raw calls
            if "response_format" in kwargs:
                content = '{"a":1}'
            else:
                content = ""
            return type("R", (), {"choices": [DummyChoices(content)]} )()

    class DummyChat:
        def __init__(self):
            self.completions = DummyCompletions()

    class DummyClient:
        def __init__(self):
            self.chat = DummyChat()

    import src.code_agent.get_routem_llm.get_llm as gl
    monkeypatch.setattr(gl, "client", DummyClient())

    class DummyModel:
        @classmethod
        def model_json_schema(cls):
            return {"type": "object", "properties": {"a": {"type": "number"}}}

    g = GetLlmResponse("hi", "x", strutured_output=DummyModel)  # type: ignore[arg-type]

    async def run_struct():
        return await g.llm_structured_groq()

    async def run_raw():
        return await g.llm_groq()

    assert asyncio.run(run_struct()) == {"a": 1}
    assert asyncio.run(run_raw()) == ""


