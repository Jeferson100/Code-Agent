from typing import Any, Dict, List

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from ..prompts.prompts import return_messages_prompt
from ..states_outputs.states import StateCode
from ..tools.think_tavily import think_response


async def return_messages(state: StateCode) -> Dict[str, List[Any]]:
    messages = state.get("messages")

    code = state.get("code")

    feedback = state.get("feedback")

    if messages:
        messages = messages[-1]

    return_messagem_prompt_format = return_messages_prompt.format(
        messages=messages, code=code, feedback=feedback
    )

    llm_init = init_chat_model("moonshotai/kimi-k2-instruct", model_provider="groq")

    agent_response = create_react_agent(  # type: ignore
        llm_init, [think_response], prompt=return_messagem_prompt_format
    )

    # response = await router_structured.llm_router()
    response = await agent_response.ainvoke({"messages": messages})  # type: ignore

    if isinstance(response, dict):
        return {"messages": [response["messages"][-1]]}

    return {"messages": [response]}
