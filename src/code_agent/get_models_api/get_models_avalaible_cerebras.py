import asyncio
from cerebras.cloud.sdk import Cerebras, AsyncCerebras
from pydantic import BaseModel, Field
from typing import Literal, Any
from dotenv import load_dotenv

load_dotenv()


class SupervisorResponse(BaseModel):
    valid: Literal[True, False] = Field(description="Valid from the supervisor, if not is need more interactions return True, else return False")
    feedback: str = Field(description="Feedback from the supervisor")


class GetModelCerebrasStructuredResponse:
    def client(self) -> Cerebras:
        return Cerebras()
    
    def client_async(self) -> AsyncCerebras:
        return AsyncCerebras()
    
    def models_cerebras(self) -> list[str]:
        client_cerebras = self.client()
        models = client_cerebras.models.list()
        return [model.id for model in models.data if not "thinking" in model.id if not "coder" in model.id]
    
    def get_models_cerebras_structured(self) -> list[Any]:
        models_vailable_cerebras = self.models_cerebras()
        client_cerebras = self.client()
        model_cerebras_strured = []
        for model in models_vailable_cerebras:
            try:
                _ = client_cerebras.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates movie recommendations."},
                        {"role": "user", "content": "Suggest a sci-fi movie from the 1990s"}
                    ],
                    response_format={
                        "type": "json_schema", 
                        "json_schema": {
                            "name": "structured_response",
                            "strict": True,
                            "schema": SupervisorResponse.model_json_schema()
                        }
                    }
                )
                model_cerebras_strured.append(model) # type:ignore
            except Exception as _:
                pass
        return  model_cerebras_strured # type:ignore
    
    async def get_models_cerebras_structured_async(self) -> list[str]:
        
        models_vailable_cerebras = self.models_cerebras()
        client_cerebras = self.client_async()
        async def check_model(model: str) -> str | None:
            try:
                _ = await client_cerebras.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates movie recommendations."},
                        {"role": "user", "content": "Suggest a sci-fi movie from the 1990s"}
                    ],
                    response_format={
                        "type": "json_schema", 
                        "json_schema": {
                            "name": "structured_response",
                            "strict": True,
                            "schema": SupervisorResponse.model_json_schema()
                        }
                    }
                )
                return model
            except Exception as _:
                return None
        
        # Executa todas as verificações em paralelo
        results = await asyncio.gather(*[check_model(model) for model in models_vailable_cerebras])
        
        model_cerebras_structured = [model for model in results if model is not None]
        
        return model_cerebras_structured