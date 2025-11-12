"""Testes para os módulos prompts e states."""
from typing import Any, Dict

import pytest

from src.code_agent import prompts
from src.code_agent.states_outputs import states as states_mod


class TestPrompts:
    """Testes para os prompts."""

    def test_prompts_exist_and_are_strings(self):
        """Testa que todos os prompts existem e são strings."""
        assert isinstance(prompts.PROMPT_CODE, str)
        assert isinstance(prompts.SUPERVISOR_CODE, str)
        assert isinstance(prompts.RETURN_MESSAGES_PROMPT, str)
        assert isinstance(prompts.PROMPT_AGENT_PESQUISADOR, str)
        assert isinstance(prompts.TODO_USAGE_INSTRUCTIONS, str)
        assert isinstance(prompts.PROMP_AGENT_CODE_2, str)
        assert isinstance(prompts.PROMP_AGENT_CODE, str)
        assert isinstance(prompts.WRITE_TODOS_DESCRIPTION, str)
        assert isinstance(prompts.WRITE_TODOS_DESCRIPTION_2, str)
        assert isinstance(prompts.RESEARCHER_INSTRUCTIONS, str)
        assert isinstance(prompts.SUBAGENT_USAGE_INSTRUCTIONS, str)

    def test_prompt_code_contains_placeholders(self):
        """Testa que PROMPT_CODE contém placeholders esperados."""
        assert "{messages}" in prompts.PROMPT_CODE
        assert "{feedback}" in prompts.PROMPT_CODE

    def test_supervisor_code_contains_placeholders(self):
        """Testa que SUPERVISOR_CODE contém placeholders esperados."""
        assert "{messages}" in prompts.SUPERVISOR_CODE
        assert "{code}" in prompts.SUPERVISOR_CODE

    def test_return_messages_prompt_contains_placeholders(self):
        """Testa que RETURN_MESSAGES_PROMPT contém placeholders esperados."""
        assert "{messages}" in prompts.RETURN_MESSAGES_PROMPT
        assert "{code}" in prompts.RETURN_MESSAGES_PROMPT
        assert "{feedback}" in prompts.RETURN_MESSAGES_PROMPT

    def test_prompt_agent_code_contains_date_placeholder(self):
        """Testa que PROMP_AGENT_CODE contém placeholder de data."""
        assert "{date}" in prompts.PROMP_AGENT_CODE

    def test_researcher_instructions_contains_date_placeholder(self):
        """Testa que RESEARCHER_INSTRUCTIONS contém placeholder de data."""
        assert "{date}" in prompts.RESEARCHER_INSTRUCTIONS


class TestStates:
    """Testes para os estados."""

    def test_file_reducer_merges_dicts_right_precedence(self):
        """Testa que file_reducer mescla dicts com precedência à direita."""
        left: Dict[str, Any] = {"a": 1, "b": 2}
        right: Dict[str, Any] = {"b": 3, "c": 4}
        reducer = getattr(states_mod, "file_reducer")
        merged = reducer(left, right)
        assert merged == {"a": 1, "b": 3, "c": 4}

    def test_file_reducer_handles_none_left(self):
        """Testa que file_reducer lida com left None."""
        right: Dict[str, Any] = {"a": 1, "b": 2}
        reducer = getattr(states_mod, "file_reducer")
        merged = reducer(None, right)
        assert merged == right

    def test_file_reducer_handles_none_right(self):
        """Testa que file_reducer lida com right None."""
        left: Dict[str, Any] = {"a": 1, "b": 2}
        reducer = getattr(states_mod, "file_reducer")
        merged = reducer(left, None)
        assert merged == left

    def test_file_reducer_handles_both_none(self):
        """Testa que file_reducer lida com ambos None."""
        reducer = getattr(states_mod, "file_reducer")
        merged = reducer(None, None)
        assert merged is None

    def test_state_code_has_required_fields(self):
        """Testa que StateCode tem os campos esperados."""
        from src.code_agent.states_outputs.states import StateCode

        # Verifica que StateCode é um TypedDict
        assert hasattr(StateCode, "__annotations__")
        annotations = StateCode.__annotations__
        assert "messages" in annotations
        assert "code" in annotations
        assert "feedback" in annotations
        assert "valid" in annotations
        assert "interactions" in annotations

    def test_todo_has_required_fields(self):
        """Testa que Todo tem os campos esperados."""
        from src.code_agent.states_outputs.states import Todo

        assert hasattr(Todo, "__annotations__")
        annotations = Todo.__annotations__
        assert "content" in annotations
        assert "status" in annotations

    def test_deep_agent_state_inherits_from_state_code(self):
        """Testa que DeepAgentState herda de StateCode."""
        from src.code_agent.states_outputs.states import DeepAgentState, StateCode

        # Verifica que DeepAgentState tem todos os campos de StateCode
        state_code_annotations = StateCode.__annotations__
        deep_agent_annotations = DeepAgentState.__annotations__

        for key in state_code_annotations:
            assert key in deep_agent_annotations

        # Verifica campos adicionais
        assert "todos" in deep_agent_annotations
        assert "files" in deep_agent_annotations
        assert "remaining_steps" in deep_agent_annotations
        assert "code_interactions" in deep_agent_annotations
