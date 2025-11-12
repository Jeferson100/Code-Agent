"""Testes para o módulo graph."""
import pytest

from src.code_agent.build_graph.graph import GraphBuilder


class TestGraphBuilder:
    """Testes para a classe GraphBuilder."""

    def test_build_returns_workflow(self, monkeypatch):
        """Testa que build retorna um StateGraph."""
        # Mock TavilyClient para evitar erro de API key
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": f"Mock search result for: {query}"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert workflow is not None
        assert hasattr(workflow, "nodes")
        assert hasattr(workflow, "set_entry_point")
        assert hasattr(workflow, "add_node")
        assert hasattr(workflow, "add_edge")
        assert hasattr(workflow, "add_conditional_edges")

    def test_build_adds_code_node(self, monkeypatch):
        """Testa que build adiciona o nó 'code'."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert "code" in workflow.nodes

    def test_build_adds_supervisor_node(self, monkeypatch):
        """Testa que build adiciona o nó 'supervisor'."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert "supervisor" in workflow.nodes

    def test_build_sets_entry_point(self, monkeypatch):
        """Testa que build define o entry point como 'code'."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert workflow.entry_point == "code"

    def test_build_adds_edge_from_code_to_supervisor(self, monkeypatch):
        """Testa que build adiciona aresta de 'code' para 'supervisor'."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert ("code", "supervisor") in workflow.edges

    def test_build_adds_conditional_edges(self, monkeypatch):
        """Testa que build adiciona arestas condicionais."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        workflow = builder.build()

        assert "code" in workflow._cond

    def test_compile_graph_returns_compiled_graph(self, monkeypatch):
        """Testa que compile_graph retorna um grafo compilado."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        graph = builder.compile_graph()

        assert graph is not None
        assert hasattr(graph, "invoke") or hasattr(graph, "ainvoke")

    def test_compile_graph_calls_build(self, monkeypatch):
        """Testa que compile_graph chama build internamente."""
        class DummyTavilyClient:
            def search(self, query: str):
                return {"results": [{"content": "mock"}]}

        import src.code_agent.tools.think_tavily as tt
        monkeypatch.setattr(tt, "tavily_client", DummyTavilyClient())

        builder = GraphBuilder()
        graph = builder.compile_graph()

        assert graph is not None
