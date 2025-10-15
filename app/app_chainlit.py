import os
import sys

import chainlit as cl
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact

load_dotenv()

app = CodeAgentReact(model="qwen/qwen3-next-80b-a3b-instruct", model_provider="nvidia", checkpointer=True)

app_code = app.create_agent()

config = {"configurable": {"thread_id": "1"}, "recursion_limit" : 10}

@cl.on_message
def main(message: cl.Message):
    
    # Certificar-se de que o conteúdo é uma string
    if isinstance(message.content, str):
        human_message = HumanMessage(content=message.content)
    else:
        # Converter para string se necessário
        human_message = HumanMessage(content=str(message.content))
        
    inputs = {"messages": [human_message],}
    
    response = app_code.invoke(
        inputs,
        config=config,
        )

    if (
        "messages" in response
        and isinstance(response["messages"], list)
        and len(response["messages"]) > 0
    ):
        cl.Message(content=response["messages"][-1].content).send()
    else:
        cl.Message(content="Erro: Resposta inválida recebida").send()