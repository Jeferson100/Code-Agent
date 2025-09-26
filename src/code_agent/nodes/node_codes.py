from typing import Any, Dict, List

from langchain.chat_models import init_chat_model

from ..get_routem_llm.routem_llm import LlmRouter
from ..prompts.prompts import prompt_code
from ..states_outputs.output_structured import CodeOutput
from ..states_outputs.states import StateCode

llm_code = init_chat_model(
    "qwen/qwen3-coder-480b-a35b-instruct", model_provider="nvidia"
)


async def node_code(state: StateCode) -> Dict[str, str]:
    messages: List[Any] = state.get("messages", [])

    if messages:
        messages = messages[-1]

    feedback = state.get("feedback", "")

    prompt_code_format = prompt_code.format(messages=messages, feedback=feedback)

    response = llm_code.invoke(prompt_code_format)

    router_structured = LlmRouter(response.content, CodeOutput)  # type:ignore

    response_code_formatted = await router_structured.llm_router()

    # Lida com ambos os casos: dict ou objeto Pydantic
    if isinstance(response_code_formatted, CodeOutput):
        code = response_code_formatted.code
        imports = response_code_formatted.imports
        prefix = response_code_formatted.prefix

    elif isinstance(response_code_formatted, dict):
        code = response_code_formatted.get("code", "")  # type:ignore
        imports = response_code_formatted.get("imports", "")  # type:ignore
        prefix = response_code_formatted.get("prefix", "")  # type:ignore
    else:
        code, imports, prefix = "", "", ""

    return {"code": code, "imports": imports, "prefix": prefix}
