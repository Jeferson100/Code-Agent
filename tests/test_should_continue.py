"""Testes para o módulo should_continue."""
from typing import cast

import pytest

from src.code_agent.nodes.should_continue import should_continue
from src.code_agent.states_outputs.states import StateCode


class TestShouldContinue:
    """Testes para a função should_continue."""

    def test_should_continue_when_valid_true_returns_end(self):
        """Testa que should_continue retorna 'END' quando valid é True."""
        state = cast(StateCode, {"valid": True, "interactions": 1, "messages": []})
        assert should_continue(state) == "END"

    def test_should_continue_when_interactions_gte_2_returns_end(self):
        """Testa que should_continue retorna 'END' quando interactions >= 2."""
        state = cast(StateCode, {"valid": False, "interactions": 2, "messages": []})
        assert should_continue(state) == "END"

    def test_should_continue_when_interactions_gt_2_returns_end(self):
        """Testa que should_continue retorna 'END' quando interactions > 2."""
        state = cast(StateCode, {"valid": False, "interactions": 3, "messages": []})
        assert should_continue(state) == "END"

    def test_should_continue_when_invalid_and_interactions_lt_2_returns_supervisor(self):
        """Testa que should_continue retorna 'supervisor' quando invalid e interactions < 2."""
        state = cast(StateCode, {"valid": False, "interactions": 1, "messages": []})
        assert should_continue(state) == "supervisor"

    def test_should_continue_when_invalid_and_interactions_0_returns_supervisor(self):
        """Testa que should_continue retorna 'supervisor' quando invalid e interactions = 0."""
        state = cast(StateCode, {"valid": False, "interactions": 0, "messages": []})
        assert should_continue(state) == "supervisor"

    def test_should_continue_handles_none_interactions(self):
        """Testa que should_continue trata interactions None como 0."""
        state = cast(StateCode, {"valid": False, "interactions": None, "messages": []})
        assert should_continue(state) == "supervisor"

    def test_should_continue_handles_missing_interactions(self):
        """Testa que should_continue trata ausência de interactions como 0."""
        state = cast(StateCode, {"valid": False, "messages": []})
        assert should_continue(state) == "supervisor"

    def test_should_continue_handles_none_valid(self):
        """Testa que should_continue trata valid None como False."""
        state = cast(StateCode, {"valid": None, "interactions": 1, "messages": []})
        assert should_continue(state) == "supervisor"

    def test_should_continue_handles_missing_valid(self):
        """Testa que should_continue trata ausência de valid como False."""
        state = cast(StateCode, {"interactions": 1, "messages": []})
        assert should_continue(state) == "supervisor"

