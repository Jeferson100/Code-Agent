import asyncio
from typing import Dict, List, Any
import json
from .get_models_avalaible_groq import GetModelGroqStructuredResponse
from .get_models_avalaible_cerebras import GetModelCerebrasStructuredResponse
from .get_models_nvidia import GetModelsNvidia

class GetModels:
    def __init__(self) -> None:
        self.nvidia = GetModelsNvidia()
        self.groq = GetModelGroqStructuredResponse()
        self.cerebras = GetModelCerebrasStructuredResponse()
        
    async def nvidia_structured(self) -> List[Dict[str, Any]]:
        nvidia_structured = await asyncio.to_thread(self.nvidia.get_models_nvidia_structured)
        list_nvidia_structured = [{"model": model, "provider": "nvidia"} for model in nvidia_structured] # type: ignore #
        return list_nvidia_structured # type: ignore
    
    async def nvidia_tools(self) -> List[Dict[str, str]]:
        nvidia_tools = await asyncio.to_thread(self.nvidia.get_models_nvidia_tools)
        list_nvidia_tools = [{"model": model, "provider": "nvidia"} for model in nvidia_tools] # type: ignore
        return list_nvidia_tools # type: ignore
    
    async def nvidia_coder(self) -> List[Dict[str, str]]:
        nvidia_coder = await asyncio.to_thread(self.nvidia.get_models_nvidia_coder)
        list_nvidia_coder = [{"model": model, "provider": "nvidia"} for model in nvidia_coder]# type: ignore
        return list_nvidia_coder# type: ignore
    
    async def nvidia_chat(self) -> List[Dict[str, str]]:
        nvidia_chat = await asyncio.to_thread(self.nvidia.get_models_nvidia_chat)
        list_nvidia_chat = [{"model": model, "provider": "nvidia"} for model in nvidia_chat]# type: ignore
        return list_nvidia_chat# type: ignore
    
    async def groq_structured(self) -> List[Dict[str, str]]:
        groq_structured = await asyncio.to_thread(self.groq.get_models_groq_structured)
        list_groq_structured = [{"model": model, "provider": "groq"} for model in groq_structured]
        return list_groq_structured
        
    async def cerebras_structured(self) -> List[Dict[str, str]]:
        cerebras_structured = await asyncio.to_thread(self.cerebras.get_models_cerebras_structured)
        list_cerebras_structured = [{"model": model, "provider": "cerebras"} for model in cerebras_structured]# type: ignore
        return list_cerebras_structured# type: ignore
    
    async def all_model_nvidia(self) -> List[Dict[str, str]]:
        all_model_nvidia = await asyncio.to_thread(self.nvidia.name_all_models_nvidia)
        list_all_model_nvidia = [{"model": model, "provider": "nvidia"} for model in all_model_nvidia]# type: ignore
        return list_all_model_nvidia# type: ignore
    
    async def all_model_groq(self) -> List[Dict[str, str]]:
        all_model_groq = await asyncio.to_thread(self.groq.models_groq)
        list_all_model_groq = [{"model": model, "provider": "groq"} for model in all_model_groq]
        return list_all_model_groq
    
    async def all_models_cerebras(self) -> List[Dict[str, str]]:
        all_model_cerebras = await asyncio.to_thread(self.cerebras.models_cerebras)
        list_all_model_cerebras = [{"model": model, "provider": "cerebras"} for model in all_model_cerebras]
        return list_all_model_cerebras
    
    async def get_all_models_async(self) -> Dict[str, List[Dict[str, str]] | BaseException]:
        """Busca todos os modelos de forma assíncrona"""
        results = await asyncio.gather(
            self.nvidia_structured(),
            self.nvidia_tools(),
            self.nvidia_coder(),
            self.nvidia_chat(),
            self.groq_structured(),
            self.cerebras_structured(),
            self.all_model_nvidia(),
            self.all_model_groq(),
            self.all_models_cerebras(),
            return_exceptions=True
        )
        
        return {
            "nvidia_structured": results[0] if not isinstance(results[0], Exception) else results[0],
            "nvidia_tools": results[1] if not isinstance(results[1], Exception) else results[1],
            "nvidia_coder": results[2] if not isinstance(results[2], Exception) else results[2],
            "nvidia_chat": results[3] if not isinstance(results[3], Exception) else results[3],
            "groq_structured": results[4] if not isinstance(results[4], Exception) else results[4],
            "cerebras_structured": results[5] if not isinstance(results[5], Exception) else results[5],
            "all_nvidia": results[6] if not isinstance(results[6], Exception) else results[6],
            "all_groq": results[7] if not isinstance(results[7], Exception) else results[7],
            "all_cerebras": results[8] if not isinstance(results[8], Exception) else results[8]
        }
        
    async def salvar_modelos(self, path:str)-> None:
        all_models = await self.get_all_models_async()
        with open(f"{path}/all_models.json", "w") as f:
            json.dump(all_models, f, indent=4)
        print("Dados salvos com sucess!")
        
    

