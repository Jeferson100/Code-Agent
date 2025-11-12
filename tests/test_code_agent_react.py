"""Testes para o módulo code_agent_react."""
from typing import Any
from unittest.mock import MagicMock, patch

from src.code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact


class TestCodeAgentReact:
    """Testes para a classe CodeAgentReact."""

    def test_init_sets_attributes(self, monkeypatch: Any):
        """Testa que __init__ define atributos corretamente."""
        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider",
                checkpointer=False,
                temperature=0.5
            )

            assert agent.model == "test-model"
            assert agent.model_provider == "test-provider"
            assert agent.temperature == 0.5
            assert agent._checkpointer is None

    def test_init_with_checkpointer_true(self, monkeypatch: Any):
        """Testa que __init__ cria MemorySaver quando checkpointer=True."""
        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            with patch("src.code_agent.creat_react_code_agent.code_agent_react.MemorySaver") as mock_memory:
                agent = CodeAgentReact(
                    model="test-model",
                    model_provider="test-provider",
                    checkpointer=True
                )

                mock_memory.assert_called_once()
                assert agent._checkpointer is not None

    def test_init_with_checkpointer_instance(self, monkeypatch: Any):
        """Testa que __init__ usa instância de checkpointer quando fornecida."""
        mock_checkpointer = MagicMock()

        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider",
                checkpointer=mock_checkpointer
            )

            assert agent._checkpointer == mock_checkpointer

    def test_create_tools_returns_list(self, monkeypatch: Any):
        """Testa que create_tools retorna lista de ferramentas."""
        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider"
            )

            tools = agent.create_tools()

            assert isinstance(tools, list)
            assert len(tools) > 0

    def test_create_tools_includes_additional_tools(self, monkeypatch: Any):
        """Testa que create_tools inclui ferramentas adicionais."""
        additional_tool = MagicMock()

        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider",
                additional_tools=[additional_tool]
            )

            tools = agent.create_tools()

            assert additional_tool in tools

    def test_build_prompt_includes_date(self, monkeypatch: Any):
        """Testa que _build_prompt inclui data."""
        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            with patch("src.code_agent.creat_react_code_agent.code_agent_react.get_today_str", return_value="Mon Jan 1, 2024"):
                agent = CodeAgentReact(
                    model="test-model",
                    model_provider="test-provider"
                )

                prompt = agent._build_prompt()

                assert isinstance(prompt, str)
                assert "Mon Jan 1, 2024" in prompt

    def test_create_agent_returns_agent(self, monkeypatch: Any):
        """Testa que create_agent retorna agente."""
        mock_llm = MagicMock()
        mock_agent = MagicMock()

        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model", return_value=mock_llm):
            with patch("src.code_agent.creat_react_code_agent.code_agent_react.create_react_agent", return_value=mock_agent):
                agent = CodeAgentReact(
                    model="test-model",
                    model_provider="test-provider"
                )

                result = agent.create_agent()

                assert result == mock_agent

    def test_repr_returns_string(self, monkeypatch: Any):
        """Testa que __repr__ retorna string."""
        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model"):
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider",
                checkpointer=True
            )

            repr_str = repr(agent)

            assert isinstance(repr_str, str)
            assert "test-model" in repr_str
            assert "test-provider" in repr_str

    def test_llm_property_caches_result(self, monkeypatch: Any):
        """Testa que propriedade llm cacheia resultado."""
        mock_llm = MagicMock()

        with patch("src.code_agent.creat_react_code_agent.code_agent_react.init_chat_model", return_value=mock_llm) as mock_init:
            agent = CodeAgentReact(
                model="test-model",
                model_provider="test-provider"
            )

            # Primeira chamada
            llm1 = agent.llm
            # Segunda chamada (deve usar cache)
            llm2 = agent.llm

            assert llm1 == llm2
            # init_chat_model deve ser chamado apenas uma vez devido ao cache
            assert mock_init.call_count == 1

