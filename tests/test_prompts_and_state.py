from typing import Dict, Any
from src.code_agent.prompts import prompts
import src.code_agent.states_outputs.states as states_mod


def test_prompts_exist_and_are_strings():
    assert isinstance(prompts.PROMPT_CODE, str)
    assert isinstance(prompts.SUPERVISOR_CODE, str)
    assert isinstance(prompts.RETURN_MESSAGES_PROMPT, str)


def test_file_reducer_merges_dicts_right_precedence():
    left: Dict[str, Any] = {"a": 1, "b": 2}
    right: Dict[str, Any] = {"b": 3, "c": 4}
    reducer = getattr(states_mod, "file_reducer")
    merged = reducer(left, right)
    assert merged == {"a": 1, "b": 3, "c": 4}


