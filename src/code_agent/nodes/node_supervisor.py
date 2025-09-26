from typing import Any, Dict

from ..get_routem_llm.routem_llm import LlmRouter
from ..prompts.prompts import supervisor_code
from ..states_outputs.output_structured import SupervisorResponse
from ..states_outputs.states import StateCode


async def node_supervisor(state: StateCode) -> Dict[str, Any]:
    print("Entrei no supervisor")

    print("state", state["messages"])

    messages = state.get("messages")

    if messages:
        messages = messages[-1]

    interactions = state.get("interactions", 0)

    error_message = state.get("error_message", "")

    if interactions:
        interactions += 1
    else:
        interactions = 1

    code = state["code"]

    prompt_supervisor_format = supervisor_code.format(
        messages=messages, code=code, error=error_message
    )

    router_structured = LlmRouter(prompt_supervisor_format, SupervisorResponse)

    response = await router_structured.llm_router()

    if (
        isinstance(response, dict)
        and "valid" not in response.keys()
        and "feedback" not in response.keys()
    ):
        response = await router_structured.llm_router()

    if isinstance(response, dict):
        feedback = response["feedback"]  # type:ignore
        valid = response["valid"]  # type:ignore
    else:
        feedback = response.feedback  # type:ignore
        valid = response.valid  # type:ignore
    return {"feedback": feedback, "valid": valid, "interactions": interactions}
