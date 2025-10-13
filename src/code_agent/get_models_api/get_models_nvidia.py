from typing import Any

from langchain_nvidia_ai_endpoints import ChatNVIDIA


class GetModelsNvidia:
    def client(self) -> ChatNVIDIA:
        return ChatNVIDIA()

    def models_nvidia(self) -> list[Any]:
        client_nvidia = self.client()
        models = client_nvidia.available_models
        return models

    def name_all_models_nvidia(self) -> list[Any]:
        models_vailable_nvidia = self.models_nvidia()
        models = [model.id for model in models_vailable_nvidia]
        return models

    def get_models_nvidia_structured(self) -> list[Any]:
        models_vailable_nvidia = self.models_nvidia()
        model_nvidia_strured = [
            model.id
            for model in models_vailable_nvidia
            if model.supports_structured_output
        ]
        return model_nvidia_strured

    def get_models_nvidia_tools(self) -> list[Any]:
        models_vailable_nvidia = self.models_nvidia()
        model_nvidia_tools = [
            model.id for model in models_vailable_nvidia if model.supports_tools
        ]
        return model_nvidia_tools

    def get_models_nvidia_coder(self) -> list[Any]:
        models_vailable_nvidia = self.models_nvidia()
        model_nvidia_coder = [
            model.id for model in models_vailable_nvidia if "code" in model.id
        ]
        return model_nvidia_coder

    def get_models_nvidia_chat(self) -> list[Any]:
        models_vailable_nvidia = self.models_nvidia()
        model_nvidia_chat = [
            model.id for model in models_vailable_nvidia if model.model_type == "chat"
        ]
        model_nvidia_chat_sem_code = [
            model for model in model_nvidia_chat if "code" not in model
        ]
        return model_nvidia_chat_sem_code
