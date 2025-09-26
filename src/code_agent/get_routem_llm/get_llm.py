import json
import logging
from typing import Any, Dict, Optional, Type

from dotenv import load_dotenv
from groq import AsyncGroq
from pydantic import BaseModel

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# client = Groq()
client = AsyncGroq()


class GetLlmResponse:
    """
    Classe para obter respostas de diferentes provedores LLM
    """

    def __init__(
        self,
        messages: str,
        model_llm: str,
        strutured_output: Optional[Type[BaseModel]] = None,
    ):
        self.messages = messages
        self.strutured_output = strutured_output
        self.model_llm = model_llm

    async def llm_structured_groq(self) -> Dict[str, Any]:
        """
        Chama modelo Groq com saída estruturada

        """

        if self.strutured_output is None:
            raise ValueError(
                "structured_output precisa estar definido para usar essa função."
            )

        response = await client.chat.completions.create(
            model=self.model_llm,
            messages=[
                {
                    "role": "user",
                    "content": self.messages,
                },  # Corrigido: usar self.messages
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "structured_response",
                    "schema": self.strutured_output.model_json_schema(),
                },
            },
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)

    async def llm_groq(self) -> str:
        """
        Chama modelo Groq sem saída estruturada
        """
        response = await client.chat.completions.create(
            model=self.model_llm,
            messages=[
                {
                    "role": "user",
                    "content": self.messages,
                },  # Corrigido: usar self.messages
            ],
        )
        return response.choices[0].message.content or ""

    async def llm_pydantic_structured(self) -> Any:
        """
        Chama modelo HuggingFace via Pydantic AI com saída estruturada
        """
        try:
            from pydantic_ai import Agent
            from pydantic_ai.models.huggingface import HuggingFaceModel

            if self.strutured_output is None:
                raise ValueError(
                    "structured_output precisa estar definido para usar essa função."
                )

            model = HuggingFaceModel(self.model_llm)
            agent = Agent(
                model, output_type=self.strutured_output
            )  # No change needed here after fixing the type hint

            async with agent.run_stream(self.messages) as response:
                async for profile in response.stream_output():
                    return profile

        except ImportError as exc:
            raise ImportError(
                "pydantic_ai não está instalado. Instale com: pip install pydantic-ai"
            ) from exc
        except Exception as e:
            logger.error("Erro no llm_pydantic_structured: %s", e)
            raise e

    async def llm_pydantic(self) -> Any:
        """
        Chama modelo HuggingFace via Pydantic AI sem saída estruturada
        """
        try:
            from pydantic_ai import Agent
            from pydantic_ai.models.huggingface import HuggingFaceModel

            model = HuggingFaceModel(self.model_llm)
            agent = Agent(model)

            async with agent.run_stream(
                self.messages
            ) as response:  # Corrigido: usar self.messages
                async for profile in response.stream_output():
                    return profile

        except ImportError as exc:
            raise ImportError(
                "pydantic_ai não está instalado. Instale com: pip install pydantic-ai"
            ) from exc
        except Exception as e:
            logger.error("Erro no llm_pydantic: %s", e)
            raise e
