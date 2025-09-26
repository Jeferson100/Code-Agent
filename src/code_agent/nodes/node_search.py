from typing import Dict

from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent

from ..prompts.prompts import prompt_agent_pesquisador
from ..states_outputs.states import StateCode
from ..tools.think_tavily import search_tool, think_tool


async def node_search(state: StateCode) -> Dict[str, str]:
    messages = state.get("messages")

    if messages:
        messages = messages[-1]

    code = state.get("code")
    error_message = state.get("error_message")
    feedback = state.get("feedback")

    prompt_agent_pesquisador_format = prompt_agent_pesquisador.format(
        messages=messages, error_message=error_message, code=code, feedback=feedback
    )

    llm_init = init_chat_model("moonshotai/kimi-k2-instruct", model_provider="groq")

    agente_search = create_react_agent(
        llm_init,
        [search_tool, think_tool],
        prompt=prompt_agent_pesquisador_format,
    )

    response = await agente_search.ainvoke({"messages": [messages]})

    return {"feedback": response["messages"][-1].content}
