from typing import Any, Dict

from langchain_tavily import TavilySearch


def search_tool(query: str) -> Dict[str, Any]:
    """
    Tool for searching the internet for information.

    Args:
        query (str): The search query.

    Returns:
        Dict[str, Any]: The search results.
    """

    tool_tavily = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        exclude_domains=["medium.com", "youtube.com", "wikipedia.org", "linkedin.com"],
    )
    return tool_tavily.invoke(query)  # type:ignore


def think_tool(reflection: str) -> str:
    """Tool for strategic reflection on research progress and decision-making.

    Use this tool after each search to analyze results and plan next steps systematically.
    This creates a deliberate pause in the research workflow for quality decision-making.

    When to use:
    - After receiving search results: What key information did I find?
    - Before deciding next steps: Do I have enough to answer comprehensively?
    - When assessing research gaps: What specific information am I still missing?
    - Before concluding research: Can I provide a complete answer now?

    Reflection should address:
    1. Analysis of current findings - What concrete information have I gathered?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence/examples for a good answer?
    4. Strategic decision - Should I continue searching or provide my answer?

    Args:
        reflection: Your detailed reflection on research progress, findings, gaps, and next steps

    Returns:
        Confirmation that reflection was recorded for decision-making
    """
    return f"Reflection recorded: {reflection}"


def think_response(reflection: str) -> str:
    """Tool for strategic thinking and analysis before delivering final coding response.

    Use this tool to process all gathered information and plan the final response delivery.
    This creates a deliberate pause in the coding workflow for quality analysis and synthesis.

    When to use:
    - After collecting all necessary information about the coding task
    - Before writing the final code solution
    - When analyzing requirements and constraints
    - Before structuring the complete response

    Analysis should address:
    1. Requirements analysis - What exactly needs to be implemented?
    2. Solution approach - What's the best technical approach?
    3. Code structure - How should the solution be organized?
    4. Edge cases and considerations - What potential issues need handling?
    5. Explanation strategy - How to best explain the solution?
    6. Response completeness - Do I have all components for a full answer?

    Args:
        analysis: Your detailed analysis of the coding task, approach, implementation plan,
                 and response structure before delivering the final solution

    Returns:
        Confirmation that analysis was recorded for final response preparation
    """

    print("🤔 AGENTE PENSANDO...")
    print("-" * 50)
    print(reflection)
    print("-" * 50)
    print("✅ Análise concluída. Preparando resposta final...")

    return f"Analysis processed: Ready to deliver comprehensive coding solution based on: {reflection}"
