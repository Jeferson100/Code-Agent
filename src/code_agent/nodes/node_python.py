from typing import Any, Dict, List, Optional

from langchain_experimental.utilities import PythonREPL

from ..states_outputs.states import StateCode


def python_repl(state: StateCode) -> Optional[Dict[str, List[Any]]]:
    """
    Use this function to execute Python code and get the results.
    """
    repl = PythonREPL()

    print("---CHECKING CODE---")

    # State
    messages: List[Any] = state.get("messages", [])

    if not messages:
        messages = messages[-1]

    code = state.get("code")

    imports = state.get("imports")

    messages_erro = []

    # Check imports
    if imports:
        try:
            print("Running the Python REPL tool")
            print(imports + "\n" + code)
            result = repl.run(imports + "\n" + code)
            print(result)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Failed to execute. Error: {e!r}")
            return {
                "error_message": messages_erro,
            }

    else:
        try:
            print("Running the Python REPL tool")
            print(code)
            result = repl.run(code)
            print(result)
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(f"Failed to execute. Error: {e!r}")
            return {
                "error_message": messages_erro,
            }
