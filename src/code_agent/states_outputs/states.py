import operator
from typing import Annotated, Any, List, Literal, TypedDict


class StateCode(TypedDict):
    messages: Annotated[List[Any], operator.add]
    feedback: str
    valid: Literal[True, False]
    interactions: int
    error_message: str
    code: str
    imports: str
    prefix: str
