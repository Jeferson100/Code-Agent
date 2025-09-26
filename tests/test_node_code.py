import asyncio
from types import SimpleNamespace
from typing import Any

from src.code_agent.nodes import node_codes as node_codes_module


class DummyCodeOutput:
    def __init__(self, prefix: str = "p", imports: str = "", code: str = "print('ok')"):
        self.prefix = prefix
        self.imports = imports
        self.code = code


def test_node_code_returns_parsed_fields(monkeypatch: Any):
    # Mock llm_code.invoke to return an object with .content
    class DummyResp:
        def __init__(self, content: str):
            self.content = content

    def fake_invoke(_prompt: str):
        return DummyResp("{\"prefix\": \"p\", \"imports\": \"\", \"code\": \"print('ok')\"}")

    monkeypatch.setattr(node_codes_module, "llm_code", SimpleNamespace(invoke=fake_invoke))

    # Mock LlmRouter.llm_router to return dict
    class DummyRouter:
        def __init__(self, *_args: Any, **_kwargs: Any):
            pass

        async def llm_router(self):
            return {"prefix": "p", "imports": "", "code": "print('ok')"}

    monkeypatch.setattr(node_codes_module, "LlmRouter", DummyRouter)

    state = {"messages": ["msg"], "feedback": ""}

    async def run():
        return await node_codes_module.node_code(state)  # type: ignore[arg-type]

    result = asyncio.run(run())
    assert result == {"code": "print('ok')", "imports": "", "prefix": "p"}

