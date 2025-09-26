import os
import sys

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.code_agent.build_graph.graph import GraphBuilder
from src.code_agent.states_outputs.states import StateCode

load_dotenv()

app_code = GraphBuilder().compile_graph()

config = {"configurable": {"thread_id": "1"}}

@cl.on_message
async def main(message: cl.Message):
    
    # Certificar-se de que o conteúdo é uma string
    if isinstance(message.content, str):
        human_message = HumanMessage(content=message.content)
    else:
        # Converter para string se necessário
        human_message = HumanMessage(content=str(message.content))
        
    inputs = {"messages": [human_message],
            "feedback": "", 
            "interactions": 0
                    
                    }

    input = StateCode(**inputs)
    
    response = await app_code.ainvoke(
        input,
        config=config,
        )

    if (
        "messages" in response
        and isinstance(response["messages"], list)
        and len(response["messages"]) > 0
    ):
        await cl.Message(content=response["messages"][-1].content).send()
    else:
        await cl.Message(content="Erro: Resposta inválida recebida").send()