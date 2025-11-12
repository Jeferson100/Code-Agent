import operator
from typing import Annotated, List, Literal, NotRequired, Optional, TypedDict

from langchain_core.messages import BaseMessage


def file_reducer(left, right):
    """Merge two file dictionaries, with right side taking precedence.

    Used as a reducer function for the files field in agent state,
    allowing incremental updates to the virtual file system.

    Args:
        left: Left side dictionary (existing files)
        right: Right side dictionary (new/updated files)

    Returns:
        Merged dictionary with right values overriding left values
    """
    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


class StateCode(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    code: NotRequired[Optional[str]]
    feedback: NotRequired[Optional[str]]
    valid: NotRequired[Optional[bool]]
    interactions: NotRequired[Optional[int]]


class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows.

    Attributes:
        content: Short, specific description of the task
        status: Current state - pending, in_progress, or completed
    """

    content: str
    status: Literal["pending", "in_progress", "completed"]


class DeepAgentState(StateCode):
    """Extended agent state that includes task tracking and virtual file system.

    Inherits from LangGraph's AgentState and adds:
    - todos: List of Todo items for task planning and progress tracking
    - files: Virtual file system stored as dict mapping filenames to content
    """

    todos: NotRequired[list[Todo]]
    files: Annotated[NotRequired[dict[str, str]], file_reducer]
    remaining_steps: NotRequired[int]
    code_interactions: NotRequired[int]
