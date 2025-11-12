from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from ..nodes.node_codes import node_code
from ..nodes.node_supervisor import node_supervisor
from ..nodes.should_continue import should_continue
from ..states_outputs.states import StateCode

load_dotenv()


class GraphBuilder:
    def __init__(self):
        self.workflow: StateGraph = StateGraph(StateCode)

    def build(self) -> StateGraph:  # type: ignore
        self.workflow.add_node("code", node_code)  # type:ignore

        self.workflow.add_node("supervisor", node_supervisor)  # type:ignore

        self.workflow.set_entry_point("code")  # type:ignore

        self.workflow.add_edge("code", "supervisor")  # type:ignore

        self.workflow.add_conditional_edges(  # type:ignore
            "code", should_continue, {"supervisor": "supervisor", "END": END}
        )  # type:ignore

        return self.workflow  # type: ignore

    def compile_graph(self):  # type: ignore
        graph = self.build()  # type: ignore
        graph_compiled = graph.compile()  # type: ignore
        return graph_compiled  # type: ignore
