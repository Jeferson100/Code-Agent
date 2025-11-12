"""Testes para o módulo output_structured."""
import pytest
from pydantic import ValidationError

from src.code_agent.states_outputs.output_structured import (
    CodeOutput,
    SearchResponse,
    SupervisorResponse,
)


class TestSupervisorResponse:
    """Testes para SupervisorResponse."""

    def test_supervisor_response_creates_with_valid_and_feedback(self):
        """Testa que SupervisorResponse cria com valid e feedback."""
        response = SupervisorResponse(valid=True, feedback="Code is good")
        assert response.valid is True
        assert response.feedback == "Code is good"

    def test_supervisor_response_creates_with_false_valid(self):
        """Testa que SupervisorResponse cria com valid=False."""
        response = SupervisorResponse(valid=False, feedback="Needs work")
        assert response.valid is False
        assert response.feedback == "Needs work"

    def test_supervisor_response_validates_literal(self):
        """Testa que SupervisorResponse valida que valid é True ou False."""
        # Deve funcionar com True
        response1 = SupervisorResponse(valid=True, feedback="test")
        assert response1.valid is True

        # Deve funcionar com False
        response2 = SupervisorResponse(valid=False, feedback="test")
        assert response2.valid is False

    def test_supervisor_response_has_feedback_field(self):
        """Testa que SupervisorResponse tem campo feedback."""
        response = SupervisorResponse(valid=True, feedback="test feedback")
        assert hasattr(response, "feedback")
        assert response.feedback == "test feedback"


class TestCodeOutput:
    """Testes para CodeOutput."""

    def test_code_output_creates_with_code(self):
        """Testa que CodeOutput cria com código."""
        output = CodeOutput(code="print('hello')")
        assert output.code == "print('hello')"

    def test_code_output_has_default_imports(self):
        """Testa que CodeOutput tem imports padrão vazio."""
        output = CodeOutput(code="print('hello')")
        assert output.imports == ""

    def test_code_output_has_default_prefix(self):
        """Testa que CodeOutput tem prefix padrão vazio."""
        output = CodeOutput(code="print('hello')")
        assert output.prefix == ""

    def test_code_output_accepts_imports(self):
        """Testa que CodeOutput aceita imports."""
        output = CodeOutput(code="print('hello')", imports="import os")
        assert output.imports == "import os"

    def test_code_output_accepts_prefix(self):
        """Testa que CodeOutput aceita prefix."""
        output = CodeOutput(code="print('hello')", prefix="prefix")
        assert output.prefix == "prefix"

    def test_code_output_requires_code(self):
        """Testa que CodeOutput requer código."""
        with pytest.raises(ValidationError):
            CodeOutput()


class TestSearchResponse:
    """Testes para SearchResponse."""

    def test_search_response_creates_with_feedback_and_code(self):
        """Testa que SearchResponse cria com feedback e código."""
        response = SearchResponse(
            feedback="Search completed",
            code="result = search()"
        )
        assert response.feedback == "Search completed"
        assert response.code == "result = search()"

    def test_search_response_requires_feedback(self):
        """Testa que SearchResponse requer feedback."""
        with pytest.raises(ValidationError):
            SearchResponse(code="code")

    def test_search_response_requires_code(self):
        """Testa que SearchResponse requer código."""
        with pytest.raises(ValidationError):
            SearchResponse(feedback="feedback")

