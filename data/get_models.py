from code_agent.get_models_api.get_all_models import GetModels
import asyncio


async def get_all_models(path:str = "./data")-> None:
    get_models = GetModels()
    await get_models.salvar_modelos(path)

    print("Dados salvos com sucess!")

if __name__ == "__main__":
    asyncio.run(get_all_models())



