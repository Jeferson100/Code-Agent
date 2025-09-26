import asyncio
import logging
from typing import Any, Dict, Optional, Type, Union

from groq import APIError
from pydantic import BaseModel

from .get_llm import GetLlmResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMRoutingError(Exception):
    """Exceção personalizada para falhas no roteamento de LLM."""


class LlmRouter:
    """
    Classe para roteamento automático entre diferentes modelos LLM com fallback
    """

    def __init__(
        self, messages: str, strutured_output: Optional[Type[BaseModel]] = None
    ):
        self.messages = messages
        self.strutured_output = strutured_output

        # Lista de modelos em ordem de prioridade
        self.groq_models = [
            "moonshotai/kimi-k2-instruct-0905",
            "moonshotai/kimi-k2-instruct",
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "openai/gpt-oss-120b",
        ]

        self.huggingface_models = [
            "Qwen/Qwen3-235B-A22B-Instruct-2507",
            "microsoft/DialoGPT-large",
            "meta-llama/Llama-4-Maverick-17B-128E",
        ]

    async def _try_groq_models(self) -> Union[Dict[str, Any], str]:
        """
        Tenta usar modelos Groq em ordem de prioridade
        """
        for model in self.groq_models:
            try:
                logger.info("Tentando modelo Groq: %s", model)
                llm_response = GetLlmResponse(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.llm_structured_groq()
                else:
                    result = await llm_response.llm_groq()

                logger.info("Sucesso com modelo Groq: %s", model)
                return result
            except APIError as e:
                logger.warning("Falha no modelo Groq %s: %s", model, e)
                continue

        raise LLMRoutingError("Todos os modelos Groq falharam")

    async def _try_huggingface_models(self) -> Any:
        """
        Tenta usar modelos HuggingFace em ordem de prioridade
        """
        for model in self.huggingface_models:
            try:
                logger.info("Tentando modelo HuggingFace: %s", model)
                llm_response = GetLlmResponse(
                    self.messages, model, self.strutured_output
                )

                if self.strutured_output:
                    result = await llm_response.llm_pydantic_structured()
                else:
                    result = await llm_response.llm_pydantic()

                logger.info("Sucesso com modelo HuggingFace: %s", model)
                return result

            except (ImportError, ValueError, RuntimeError) as e:
                logger.warning("Falha no modelo HuggingFace %s: %s", model, e)
                continue

        raise LLMRoutingError("Todos os modelos HuggingFace falharam")

    async def llm_router(self) -> Union[Dict[str, Any], str, Any]:
        """
        Método principal que implementa o sistema de fallback
        """
        logger.info("Iniciando roteamento LLM")

        # Primeira tentativa: Modelos Groq
        try:
            return await self._try_groq_models()
        except LLMRoutingError as groq_error:
            logger.warning("Todos os modelos Groq falharam: %s", groq_error)

            # Segunda tentativa: Modelos HuggingFace
            try:
                return await self._try_huggingface_models()
            except LLMRoutingError as hf_error:
                logger.error("Todos os modelos HuggingFace falharam: %s", hf_error)

                # Se tudo falhar, lança exceção detalhada
                raise LLMRoutingError(
                    f"Todos os provedores falharam. "
                    f"Groq: {groq_error}, HuggingFace: {hf_error}"
                ) from hf_error

    def llm_router_sync(self) -> Union[Dict[str, Any], str, Any]:
        """
        Versão síncrona do roteador LLM
        """
        return asyncio.run(self.llm_router())

    async def get_structured_response(
        self, output_model: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """
        Obtém resposta estruturada e valida com o modelo Pydantic
        """
        if not self.strutured_output:
            # Atualiza temporariamente para usar saída estruturada
            original_structured = self.strutured_output
            self.strutured_output = output_model

            try:
                result = await self.llm_router()
                return (
                    output_model(**result)
                    if isinstance(result, dict)
                    else output_model()
                )

            finally:
                self.strutured_output = original_structured  # type:ignore

        else:
            result = await self.llm_router()
            return (
                output_model(**result) if isinstance(result, dict) else output_model()
            )

    def add_groq_model(self, model_name: str, priority: int = 0):
        """
        Adiciona um novo modelo Groq à lista
        """
        if priority == 0:
            self.groq_models.append(model_name)
        else:
            self.groq_models.insert(priority, model_name)

    def add_huggingface_model(self, model_name: str, priority: int = 0):
        """
        Adiciona um novo modelo HuggingFace à lista
        """
        if priority == 0:
            self.huggingface_models.append(model_name)
        else:
            self.huggingface_models.insert(priority, model_name)
