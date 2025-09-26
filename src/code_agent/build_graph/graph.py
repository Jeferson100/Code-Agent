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
        self.workflow = StateGraph(StateCode)

    def build(self):
        self.workflow.add_node("code", node_code)

        self.workflow.add_node("supervisor", node_supervisor)

        self.workflow.add_node("check", python_repl)

        self.workflow.add_node("search", node_search)

        self.workflow.add_node("return_messages", return_messages)

        self.workflow.set_entry_point("code")

        self.workflow.add_edge("code", "check")

        self.workflow.add_edge("check", "supervisor")

        self.workflow.add_edge("search", "code")

        self.workflow.add_edge("return_messages", END)

        self.workflow.add_conditional_edges(
            "supervisor",
            should_continue,
            {"code": "code", "search": "search", "return_messages": "return_messages"},
        )

        return self.workflow

    def compile_graph(self):
        graph = self.build()
        memory = MemorySaver()
        graph_compiled = graph.compile(checkpointer=memory)
        return graph_compiled
