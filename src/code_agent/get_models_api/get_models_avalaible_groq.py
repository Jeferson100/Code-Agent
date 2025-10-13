import asyncio
from typing import Literal

from groq import AsyncGroq, Groq
from pydantic import BaseModel, Field


class SupervisorResponse(BaseModel):
    valid: Literal[True, False] = Field(
        description="Valid from the supervisor, if not is need more interactions return True, else return False"
    )
    feedback: str = Field(description="Feedback from the supervisor")


class GetModelGroqStructuredResponse:
    def client(self) -> Groq:
        return Groq()

    def client_async(self) -> AsyncGroq:
        return AsyncGroq()

    def models_groq(self) -> list[str]:
        client_groq = self.client()
        models = client_groq.models.list()
        return [
            model.id
            for model in models.data
            if "thinking" not in model.id
            if "coder" not in model.id
        ]

    def get_models_groq_structured(self) -> list[str]:
        models_vailable_groq = self.models_groq()
        client_groq = self.client()
        model_groq_strured = []
        for model in models_vailable_groq:
            try:
                _ = client_groq.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that generates movie recommendations.",
                        },
                        {
                            "role": "user",
                            "content": "Suggest a sci-fi movie from the 1990s",
                        },
                    ],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "structured_response",
                            "schema": SupervisorResponse.model_json_schema(),
                        },
                    },
                )
                model_groq_strured.append(model)  # type:ignore
            except Exception as _:  # pylint: disable=broad-exception-caught
                pass
        return model_groq_strured  # type:ignore

    async def get_models_groq_structured_async(self) -> list[str]:
        models_available_groq = self.models_groq()
        client_groq = self.client_async()

        async def check_model(model: str) -> str | None:
            try:
                _ = await client_groq.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that generates movie recommendations.",
                        },
                        {
                            "role": "user",
                            "content": "Suggest a sci-fi movie from the 1990s",
                        },
                    ],
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "structured_response",
                            "schema": SupervisorResponse.model_json_schema(),
                        },
                    },
                )
                return model
            except Exception as _:  # pylint: disable=broad-exception-caught
                return None

        # Executa todas as verificações em paralelo
        results = await asyncio.gather(
            *[check_model(model) for model in models_available_groq]
        )

        model_groq_structured = [model for model in results if model is not None]

        return model_groq_structured
