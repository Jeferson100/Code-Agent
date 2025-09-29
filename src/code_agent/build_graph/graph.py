from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from ..nodes.node_codes import node_code
from ..nodes.node_python import python_repl
from ..nodes.node_return_message import return_messages
from ..nodes.node_search import node_search
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

        self.workflow.add_node("check", python_repl)  # type:ignore

        self.workflow.add_node("search", node_search)  # type:ignore

        self.workflow.add_node("return_messages", return_messages)  # type:ignore

        self.workflow.set_entry_point("code")  # type:ignore

        self.workflow.add_edge("code", "check")  # type:ignore

        self.workflow.add_edge("check", "supervisor")  # type:ignore

        self.workflow.add_edge("search", "code")  # type:ignore

        self.workflow.add_edge("return_messages", END)  # type:ignore

        self.workflow.add_conditional_edges(  # type:ignore
            "supervisor",
            should_continue,
            {"code": "code", "search": "search", "return_messages": "return_messages"},
        )

        return self.workflow  # type: ignore

    def compile_graph(self):  # type: ignore
        graph = self.build()  # type: ignore
        memory = MemorySaver()  # type: ignore
        graph_compiled = graph.compile(checkpointer=memory)  # type: ignore
        return graph_compiled  # type: ignore
