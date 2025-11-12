import logging
from functools import cached_property
from typing import Any, List, Optional

from langchain.chat_models import init_chat_model
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent  # pylint: disable=E0401,E0611

from ..prompts.prompts import PROMP_AGENT_CODE, TODO_USAGE_INSTRUCTIONS
from ..states_outputs.states import DeepAgentState
from ..tools.think_tavily import think_tool, web_search
from ..tools.todos import read_todos, write_todos
from ..tools.tool_write_code import write_code
from ..utils.get_today import get_today_str

logger = logging.getLogger(__name__)


class CodeAgentReact:
    """
    Agente React para execução de código e gerenciamento de tarefas.

    Esta classe encapsula a criação e configuração de um agente React
    usando LangGraph, com suporte a múltiplas ferramentas e checkpoint.

    Attributes:
        model: Nome do modelo a ser utilizado
        model_provider: Provedor do modelo (ex: 'openai', 'anthropic')
        checkpointer: Instância de checkpointer para persistência de estado

    Example:
        >>> agent = CodeAgentReact(
        ...     model="gpt-4",
        ...     model_provider="openai",
        ...     checkpointer=True
        ... )
        >>> graph = agent.create_agent()
    """

    def __init__(
        self,
        model: str,
        model_provider: str,
        checkpointer: Optional[bool | BaseCheckpointSaver] = None,
        temperature: float = 0.0,
        additional_tools: Optional[List[Any]] = None,
    ):
        self._checkpointer: Optional[BaseCheckpointSaver] = None
        """
        Inicializa o CodeAgentReact.

        Args:
            model: Nome/identificador do modelo
            model_provider: Provedor do modelo
            checkpointer: Se True, usa MemorySaver. Se BaseCheckpointSaver,
                         usa a instância fornecida. Se None/False, sem checkpoint
            temperature: Temperatura para geração do modelo (default: 0.0)
            additional_tools: Lista de ferramentas adicionais (opcional)
        """
        self.model = model
        self.model_provider = model_provider
        self.temperature = temperature
        self.additional_tools = additional_tools or []

        if checkpointer is True:
            self._checkpointer = MemorySaver()
        elif isinstance(checkpointer, BaseCheckpointSaver):
            self._checkpointer = checkpointer
        else:
            self._checkpointer = None

        logger.info(
            "CodeAgentReact inicializado: provider=%s, checkpointer=%s",
            model_provider,
            bool(self._checkpointer),
        )

    @cached_property
    def llm(self):
        """
        Inicializa e retorna o modelo de chat.

        Usa cached_property para evitar reinicialização desnecessária.

        Returns:
            Instância do modelo de chat configurado
        """
        try:
            model_instance = init_chat_model(
                model=self.model,
                temperature=self.temperature,
                model_provider=self.model_provider,
            )
            logger.info(
                "Modelo provider=%s inicializado com sucesso", self.model_provider
            )
            return model_instance
        except Exception as e:
            logger.error("Erro ao inicializar modelo: %s", e)
            raise

    def create_tools(self) -> List[Any]:
        """
        Cria e retorna a lista de ferramentas disponíveis.

        Returns:
            Lista de ferramentas configuradas para o agente
        """
        base_tools = [
            think_tool,
            write_todos,
            read_todos,
            web_search,
            write_code,
        ]

        all_tools = base_tools + self.additional_tools

        return all_tools

    def _build_prompt(self) -> str:
        """
        Constrói o prompt completo para o agente.

        Returns:
            String com o prompt formatado
        """
        separator = "=" * 80
        current_date = get_today_str()

        prompt = (
            f"{TODO_USAGE_INSTRUCTIONS}\n"
            f"{separator}\n"
            f"{PROMP_AGENT_CODE.format(date=current_date)}"
            # f"{separator}\n"
            # f"{SUBAGENT_USAGE_INSTRUCTIONS.format(max_concurrent_research_units=max_concurrent_research_units, max_researcher_iterations=max_researcher_iterations)}\n"
        )

        return prompt

    def create_agent(self) -> Any:
        """
        Cria e retorna o agente React configurado.

        Returns:
            Instância do agente React pronto para uso

        Raises:
            Exception: Se houver erro na criação do agente
        """
        try:
            prompt = self._build_prompt()

            agent_code = create_react_agent(  # type: ignore
                self.llm,
                self.create_tools(),
                prompt=prompt,
                state_schema=DeepAgentState,
                checkpointer=self._checkpointer,
            )

            logger.info("Agente React criado com sucesso")
            return agent_code

        except Exception as e:
            logger.error("Erro ao criar agente: %s", e)
            raise

    def __repr__(self) -> str:
        """Representação em string do agente."""
        return (
            f"CodeAgentReact(model='{self.model}', "
            f"provider='{self.model_provider}', "
            f"checkpointer={bool(self._checkpointer)})"
        )
