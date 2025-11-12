import asyncio
from typing import Annotated

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState  # pylint: disable=E0401,E0611
from langgraph.types import Command

from ..build_graph.graph import GraphBuilder
from ..states_outputs.states import DeepAgentState, StateCode

graph = GraphBuilder()

graph_build = graph.compile_graph()


@tool
def write_code(
    query: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command | str:
    """
    Tool for generating or improving code.

    Args:
        query (str):
            A natural language instruction or request describing the code
            to be generated, refactored, or explained.
            Example: "Write a Python function to calculate factorial using recursion."

    Returns:
        DeepAgentState:
            A state dictionary containing the agent’s latest response message.
            The structure includes:
            - "messages": list of conversation messages, where the last one
              holds the generated code or explanation.

    """
    code_interactions = state.get("code_interactions", 0)

    try:
        if code_interactions < 3:
            new_code_interactions = code_interactions + 1

            response = asyncio.run(
                graph_build.ainvoke(
                    StateCode(
                        messages=[HumanMessage(role="user", content=query)],
                        interactions=0,
                        feedback="",
                    )
                )
            )

            last_message = response["messages"][-1]
            content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

            formatted_content = f"```n{content}\n```"

            return Command(
                update={
                    "code_interactions": new_code_interactions,
                    "messages": [
                        ToolMessage(
                            content=formatted_content, tool_call_id=tool_call_id
                        )
                    ],
                }
            )
        else:
            message = (
                "Code interaction limit reached."
                "You have already used the 3 allowed calls for code generation."
                "Please review the generated code or make a new request in another tools."
            )

            return Command(
                update={
                    "code_interactions": code_interactions,
                    "messages": [
                        ToolMessage(content=message, tool_call_id=tool_call_id)
                    ],
                }
            )

    except Exception as e:  # pylint: disable=broad-except
        return f"An Error occurred: {e} with the write_code. Please try again later."
