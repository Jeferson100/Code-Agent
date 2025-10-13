from src.code_agent.build_graph.graph import GraphBuilder


def test_build_returns_workflow(monkeypatch):
    # Mock TavilyClient to avoid API key error
    class DummyTavilyClient:
        def search(self, query: str):
            return {"results": [{"content": f"Mock search result for: {query}"}]}
    
    import src.code_agent.tools.think_tavily as tt
    monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())
    
    builder = GraphBuilder()
    workflow = builder.build()
    assert workflow is not None


def test_compile_graph_returns_compiled_graph(monkeypatch):
    # Mock TavilyClient to avoid API key error
    class DummyTavilyClient:
        def search(self, query: str):
            return {"results": [{"content": f"Mock search result for: {query}"}]}
    
    import src.code_agent.tools.think_tavily as tt
    monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())
    
    builder = GraphBuilder()
    graph = builder.compile_graph()
    assert hasattr(graph, "invoke") or hasattr(graph, "ainvoke")

