import os
from typing import Any

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

load_dotenv()

tavily_client = TavilyClient()


@tool(parse_docstring=True)
def web_search(
    query: str, max_results: int = 5, include_images: bool = False
) -> list[Any | dict[str, str]]:
    """Search the web for information on a specific topic.

    This tool performs web searches and returns relevant results
    for the given query. Use this when you need to gather information from
    the internet about any topic.

    Args:
        query: The search query string. Be specific and clear about what
               information you're looking for.
        max_results: The maximum number of search results to return.
        include_images: Whether to include images in the search results.

    Returns:
        Search results from search engine.

    Example:
        web_search("machine learning applications in healthcare")
    """
    params = {}
    api_key: str | None = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")
    params["api_key"] = api_key

    client = TavilyClient(api_key=api_key)

    try:
        response = client.search(
            query=query, max_results=max_results, include_images=include_images
        )

        results = []
        for r in response.get("results", []):
            results.append(
                {
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", ""),
                }
            )

        if include_images:
            for img_url in response.get("images", []):
                results.append({"image_url": img_url})

        return results

    except Exception as e:  # pylint: disable=broad-except
        return [f"An Error occurred: {e} with the Tavily API. Please try again later."]


@tool(parse_docstring=True)
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


@tool
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
