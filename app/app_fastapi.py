from dotenv import load_dotenv


from fastapi import FastAPI
from fastapi.responses import JSONResponse

from langchain_core.messages import HumanMessage
from src.code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact

load_dotenv()


app = FastAPI(
    title="Agente de Codificação",
    description="Api para agente de codificação com langchain e fastapi",
    version="0.0.1",
)

@app.get("/")
async def root():
    """
    Rota raiz que retorna informações básicas sobre a API
    """
    return JSONResponse(
        {
            "message": "Bem-vindo à API do Agente de Codificação",
            "endpoints": {
                "docs": "/docs",
                "chatbot": "/chatbot/{message}",
            },
            "exemplo": '/chatbot/ "Escreva um código em Python que imprima o quadrado de 5" ',
        }
    )
    
@app.get("/chatbot/{message}")
async def chatbot(message: str):
    """
    Endpoint do chatbot que recebe uma mensagem e retorna a resposta do LangGraph.
    """
    
    code_agent = CodeAgentReact(model="qwen/qwen3-next-80b-a3b-instruct", model_provider="nvidia", checkpointer=True)
    
    app_code = code_agent.create_agent()

    # Configuração para a thread específica (pode ser dinâmica se necessário)
    config = {"configurable": {"thread_id": "1"}}

    # Estado inicial para a invocação do grafo
    inputs = {"messages": [HumanMessage(content=message)],
                    }
    
    
    response = await app_code.ainvoke(
        inputs,
        config=config,
    )

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_main:app", host="0.0.0.0", port=3000, reload=True)