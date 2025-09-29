from src.code_agent.build_graph.graph import GraphBuilder


def test_build_returns_workflow():
    builder = GraphBuilder()
    workflow = builder.build()
    assert workflow is not None


def test_compile_graph_returns_compiled_graph():
    builder = GraphBuilder()
    graph = builder.compile_graph()
    assert hasattr(graph, "invoke") or hasattr(graph, "ainvoke")

