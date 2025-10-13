import os
import sys

# Disable autoloading of external pytest plugins (e.g., hydra), which can break test startup
os.environ.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")

# Ensure project root is on sys.path for `src` imports when running via different CWDs
ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(ROOT, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ------------------------------------------------------------
# Lightweight stubs for external dependencies to keep tests offline
# ------------------------------------------------------------
import types  # noqa: E402


def ensure_module(name: str) -> types.ModuleType:
    if name in sys.modules:
        return sys.modules[name]
    mod = types.ModuleType(name)
    sys.modules[name] = mod
    return mod


# dotenv
dotenv = ensure_module("dotenv")
def _noop_load_dotenv() -> None:  # type: ignore[override]
    return None
setattr(dotenv, "load_dotenv", _noop_load_dotenv)


# groq
groq = ensure_module("groq")
class _APIError(Exception):
    pass
class _AsyncGroq:  # minimal stub used in get_llm
    class _Chat:
        class _Completions:
            class _ChoicesMsg:
                def __init__(self, content: str = "{}"):
                    self.message = types.SimpleNamespace(content=content)

            def create(self, **_kwargs):  # type: ignore[override]
                return types.SimpleNamespace(choices=[self._ChoicesMsg("")])

        def __init__(self):
            self.completions = self._Completions()

    def __init__(self):
        self.chat = self._Chat()

setattr(groq, "APIError", _APIError)
setattr(groq, "AsyncGroq", _AsyncGroq)


# langgraph.graph
lg_graph = ensure_module("langgraph.graph")
class _END:  # sentinel
    pass
class _StateGraph:
    def __init__(self, _state_type):
        self.nodes = set()
        self.edges = set()
        self._cond = {}
        self.entry_point = None

    def add_node(self, name, _fn):
        self.nodes.add(name)

    def set_entry_point(self, name):
        self.entry_point = name

    def add_edge(self, a, b):
        self.edges.add((a, b))

    def add_conditional_edges(self, name, _cond_fn, mapping):
        self._cond[name] = mapping

    def compile(self, checkpointer=None):  # noqa: ARG002
        return types.SimpleNamespace(invoke=lambda x: x, ainvoke=None)

setattr(lg_graph, "END", _END)
setattr(lg_graph, "StateGraph", _StateGraph)


# langgraph.checkpoint.memory
lg_mem = ensure_module("langgraph.checkpoint.memory")
class _MemorySaver:
    pass
setattr(lg_mem, "MemorySaver", _MemorySaver)


# langgraph.prebuilt
lg_prebuilt = ensure_module("langgraph.prebuilt")
def _create_react_agent(_llm, _tools, prompt=None):  # noqa: ARG002
    class _Agent:
        async def ainvoke(self, _payload):  # noqa: ARG002
            return {"messages": [types.SimpleNamespace(content="ok")]}
    return _Agent()
setattr(lg_prebuilt, "create_react_agent", _create_react_agent)


# langchain.chat_models
lc_chat = ensure_module("langchain.chat_models")
def _init_chat_model(*_args, **_kwargs):  # noqa: D401, ARG002
    class _LLM:
        def invoke(self, _prompt):  # noqa: ARG002
            return types.SimpleNamespace(content="{}")
    return _LLM()
setattr(lc_chat, "init_chat_model", _init_chat_model)


# langchain_experimental.utilities
lc_exp = ensure_module("langchain_experimental.utilities")
class _PythonREPL:
    def run(self, code: str):
        # naive exec; suitable for simple tests
        local_ns: dict = {}
        exec(code, {}, local_ns)
        return ""
setattr(lc_exp, "PythonREPL", _PythonREPL)


# tavily
tavily = ensure_module("tavily")
class _TavilyClient:
    def search(self, query: str):
        return {"results": [{"content": f"Mock search result for: {query}"}]}
setattr(tavily, "TavilyClient", _TavilyClient)


# cerebras
cerebras = ensure_module("cerebras")
cerebras_cloud = ensure_module("cerebras.cloud")
cerebras_cloud_sdk = ensure_module("cerebras.cloud.sdk")

class _AsyncCerebras:
    def __init__(self, *args, **kwargs):
        pass
    
    async def generate(self, *args, **kwargs):
        return {"choices": [{"text": "mock response"}]}

setattr(cerebras_cloud_sdk, "AsyncCerebras", _AsyncCerebras)


# pydantic_ai
pydantic_ai = ensure_module("pydantic_ai")
pydantic_ai_models = ensure_module("pydantic_ai.models")
pydantic_ai_models_huggingface = ensure_module("pydantic_ai.models.huggingface")

class _HuggingFaceModel:
    def __init__(self, *args, **kwargs):
        pass

class _Agent:
    def __init__(self, *args, **kwargs):
        pass
    
    def run_sync(self, *args, **kwargs):
        return {"mock": "response"}
    
    async def run_stream(self, *args, **kwargs):
        class _Stream:
            async def __aenter__(self):
                return self
            
            async def __aexit__(self, *args):
                pass
            
            async def stream_output(self):
                yield {"mock": "stream_response"}
        
        return _Stream()

setattr(pydantic_ai_models_huggingface, "HuggingFaceModel", _HuggingFaceModel)
setattr(pydantic_ai, "Agent", _Agent)