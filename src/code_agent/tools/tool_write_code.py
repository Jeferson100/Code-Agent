import asyncio

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from ..build_graph.graph import GraphBuilder
from ..states_outputs.states import DeepAgentState, StateCode


@tool
def write_code(query: str) -> DeepAgentState:
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
    graph_build = GraphBuilder().compile_graph()

    response = asyncio.run(
        graph_build.ainvoke(
            StateCode(
                messages=[HumanMessage(role="user", content=query)],
                interactions=0,
                feedback="",
                valid=False,
                code="",
            )
        )
    )

    return {
        "messages": [response["messages"][-1]],
        "feedback": response["feedback"],
        "valid": response["valid"],
        "interactions": response["interactions"],
        "code": response.get("code", ""),
    }
