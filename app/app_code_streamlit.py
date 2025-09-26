import os
from contextlib import contextmanager

import streamlit as st

import asyncio
from langchain_core.messages import HumanMessage


st.set_page_config(
    page_title="Agent of Code",
    page_icon="imagem/logo_robo.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Agent de code",
    },
)  

@contextmanager
def temp_env_vars(**kwargs):
    """
    Context manager que cria variáveis de ambiente temporárias.
    Restaura os valores originais ao sair do contexto.
    """
    # Salva valores originais
    original_values = {}
    for key in kwargs:
        original_values[key] = os.environ.get(key)

    # Define novos valores
    for key, value in kwargs.items():
        if value is not None:
            os.environ[key] = str(value)
        elif key in os.environ:
            del os.environ[key]

    try:
        yield
    finally:
        # Restaura valores originais
        for key, original_value in original_values.items():
            if original_value is not None:
                os.environ[key] = original_value
            elif key in os.environ:
                del os.environ[key]

if (
    "groq_api" in st.session_state
    and st.session_state.groq_api
    or os.getenv("GROQ_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do GROQ.")

if (
    "tavily_api" in st.session_state
    and st.session_state.tavily_api
    or os.getenv("TAVILY_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do Tavily.")
    
if (
    "nvidia_api" in st.session_state
    and st.session_state.nvidia_api
    or os.getenv("NVIDIA_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API da NVIDIA.")
    
if (
    "huggingface_api" in st.session_state
    and st.session_state.huggingface_api
    or os.getenv("HUGGINGFACE_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do HuggingFace."
)

if (
    "pydantic_api" in st.session_state
    and st.session_state.pydantic_api
    or os.getenv("PYDANTIC_API_KEY")
):
    pass
else:
    st.warning("Por favor, defina a chave API do Pydantic.")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
messages = st.session_state.chat_history

def clear_messages():
    if "chat_history" in st.session_state:
        del st.session_state["chat_history"]
    st.rerun()
    
st.title("Agente de Codificação")

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

mensagem_usuario = st.chat_input("Faça sua pergunta:")
with st.sidebar:
    st.markdown("# Login APIs:")
    st.write(
        """Para utilizar o Bot, primeiro faça o cadastro gratuito nos site abaixo e 
        depois gere as chaves API necessária:"""
    )
    
    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        st.markdown(
            """
        [![Groq API](https://img.shields.io/badge/Create%20Groq%20API%20Key-blue?style=flat&logo=groq)](https://console.groq.com/keys)
        """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
        [![Tavily](https://img.shields.io/badge/Create%20Tavily%20API%20Key-blue?style=flat&logo=groq)](https://app.tavily.com/home)
        """,
            unsafe_allow_html=True,
        )
        
    with col3:
    
        st.markdown(
            """
        [![Nvidia](https://img.shields.io/badge/Create%20Nvidia%20API%20Key-blue?style=flat&logo=groq)](https://org.ngc.nvidia.com/setup/api-key)
        """,
            unsafe_allow_html=True,
        )
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
            st.markdown(
                """
            [![HuggingFace](https://img.shields.io/badge/Create%20HuggingFace%20API%20Key-blue?style=flat&logo=groq)](https://huggingface.co/settings/tokens)
            """,
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown(
            """
        [![Pydantic](https://img.shields.io/badge/Create%20Pydantic%20API%20Key-blue?style=flat&logo=groq)](https://pydantic-docs.helpmanual.io/usage/settings/)
        """,
            unsafe_allow_html=True,
        )

    if "groq_api" not in st.session_state:
        st.session_state["groq_api"] = None

    if "tavily_api" not in st.session_state:
        st.session_state["tavily_api"] = None

    if "nvidia_api" not in st.session_state:
        st.session_state["nvidia_api"] = None
    
    if "huggingface_api" not in st.session_state:
        st.session_state["huggingface_api"] = None
        
    if "pydantic_api" not in st.session_state:
        st.session_state["pydantic_api"] = None

    try:
        if os.getenv("GROQ_API_KEY") is not None:
            groq_api = os.getenv("GROQ_API_KEY")
            st.success("API key GROQ ja existe!", icon="✅")
        else:
            # Pede a chave apenas se ainda não estiver salva
            api_key = st.text_input(
                "Enter GROQ API token:",
                value=st.session_state.groq_api,
                type="password",
            )

            if api_key:
                st.session_state.groq_api = api_key
                st.success("API key GROQ configurada com sucesso!", icon="✅")

        if os.getenv("API_KEY_TAVLIY") is not None:
            tavily_api = os.getenv("API_KEY_TAVLIY")
            st.success("API key Tavily ja existe!", icon="✅")

        else:
            # Pede a chave apenas se ainda não estiver salva
            tavily_api = st.text_input(
                "Enter Tavily API token:",
                value=st.session_state.tavily_api,
                type="password",
            )

            if tavily_api:
                st.session_state.tavily_api = tavily_api
                st.success("API key Tavily configurada com sucesso!", icon="✅")

        if os.getenv("NVIDIA_API_KEY") is not None:
            nvidia_api = os.getenv("NVIDIA_API_KEY")
            st.success("API key NVIDIA ja existe!", icon="✅")

        else:
            # Pede a chave apenas se ainda não estiver salva
            nvidia_api = st.text_input(
                "Enter NVIDIA API token:",
                value=st.session_state.nvidia_api,
                type="password",
            )

            if nvidia_api:
                st.session_state.nvidia_api = nvidia_api
                st.success("API key NVIDIA configurada com sucesso!", icon="✅")

        if os.getenv("HUGGINGFACE_API_KEY") is not None:
            huggingface_api = os.getenv("HUGGINGFACE_API_KEY")
            st.success("API key HuggingFace ja existe!", icon="✅")

        else:
            # Pede a chave apenas se ainda não estiver salva
            huggingface_api = st.text_input(
                "Enter HuggingFace API token:",
                value=st.session_state.huggingface_api,
                type="password",
            )            

            if huggingface_api:
                st.session_state.huggingface_api = huggingface_api
                st.success("API key HuggingFace configurada com sucesso!", icon="✅")

        if os.getenv("PYDANTIC_API_KEY") is not None:
            pydantic_api = os.getenv("PYDANTIC_API_KEY")
            st.success("API key Pydantic ja existe!", icon="✅")

        else:
            # Pede a chave apenas se ainda não estiver salva
            pydantic_api = st.text_input(
                "Enter Pydantic API token:",
                value=st.session_state.pydantic_api,
                type="password",
            )

            if pydantic_api:
                st.session_state.pydantic_api = pydantic_api
                st.success("API key Pydantic configurada com sucesso!", icon="✅")

    except ValueError as e:
        st.error(f"Erro ao utilizar a API: {e}")
        st.stop()

    st.markdown("---")
    
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button(
            "Limpar Mémoria",
            help="Limpa o histórico de mensagens",
            key="limpar_memoria_tecnica",
        ):
            clear_messages()
    with col2:
        if "chat_history" in st.session_state:
            dados_memoria = st.session_state["chat_history"]
            # Converter a lista de dicionários em uma string formatada
            dados_formatados = "\n\n".join(
                [
                    f"**{msg['role'].capitalize()}**: {msg['content']}"
                    for msg in dados_memoria
                ]
            )
            st.download_button(
                label="Download histórico",
                data=dados_formatados,
                file_name="dados_llm.md",
                mime="text/markdown",
                help="Histórico de converças!",
            )
        else:
            st.warning("Nenhum dado disponível para download.")

    st.sidebar.markdown("---")

    st.markdown("# Contatos")

    st.sidebar.markdown(
        """
        <div style="display: inline-block; margin-right: 10px;">
            <a href="https://github.com/Jeferson100/Agente-investimento">
                <img src="https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github">
            </a>
        </div>
        <div style="display: inline-block;">
            <a href="https://www.linkedin.com/in/jefersonsehnem/">
                <img src="https://img.shields.io/badge/linkedin-0077b5?style=for-the-badge&logo=linkedin&logocolor=white">
            </a>
        </div>
    """,
        unsafe_allow_html=True,
    )
    
if mensagem_usuario:
    messages.append({"role": "user", "content": mensagem_usuario})
    with st.chat_message("user"):
        st.markdown(mensagem_usuario)

    # Verificar se as API keys estão configuradas
    groq_key = st.session_state.get("groq_api")
    
    tavily_key = st.session_state.get("tavily_api")
    
    nvidia_key = st.session_state.get("nvidia_api")
    
    huggingface_key = st.session_state.get("huggingface_api")
    
    pydantic_key = st.session_state.get("pydantic_api")

    if not groq_key or not tavily_key or not nvidia_key or not huggingface_key or not pydantic_key:
        # Mostrar erro na interface do usuário
        error_msg = "❌ **Erro: APIs não configuradas**\n\n"
        if not groq_key:
            error_msg += "- GROQ API Key não encontrada\n"
        if not tavily_key:
            error_msg += "- Tavily API Key não encontrada\n"
        if not nvidia_key:
            error_msg += "- Nvidia API Key não encontrada\n"
        if not huggingface_key:
            error_msg += "- Huggingface API Key não encontrada\n"
        if not pydantic_key:
            error_msg += "- Pydantic API Key não encontrada\n"
        error_msg += "\n👆 Configure as chaves na barra lateral para continuar."

        with st.chat_message("assistant"):
            st.error(error_msg)

        messages.append({"role": "assistant", "content": error_msg})
        st.stop()  # Para a execução aqui

    try:
        with st.spinner("🤖 Processando sua solicitação..."):
            # Usar contexto temporário para toda a operação
            with temp_env_vars(GROQ_API_KEY=groq_key, TAVILY_API_KEY=tavily_key, NVIDIA_API_KEY=nvidia_key, HUGGINGFACE_API_KEY=huggingface_key, PYDANTIC_API_KEY=pydantic_key):
                # Importar dentro do contexto
                from src.code_agent.build_graph.graph import GraphBuilder
                from src.code_agent.states_outputs.states import StateCode

                app_code = GraphBuilder().compile_graph()
    
                config = {"configurable": {"thread_id": "1"}}

                # Estado inicial para a invocação do grafo
                inputs = {"messages": [HumanMessage(content=
                    mensagem_usuario
                 
                )],
                "feedback": "", 
                "interactions": 0
                    
                    }

                input = StateCode(**inputs)

                # Executar o grafo usando asyncio.run
                response = asyncio.run(
                    app_code.ainvoke(input, config=config)  # type: ignore
                )

                # Extrair a resposta
                if (
                    response
                    and "messages" in response
                    and len(response["messages"]) > 1
                ):
                    response_text = response["messages"][1].content
                else:
                    response_text = (
                        "❌ Erro: Não foi possível obter resposta do agente."
                    )

                # Mostrar resposta
                with st.chat_message("assistant"):
                    st.write(response_text)

                messages.append({"role": "assistant", "content": response_text})

    except ImportError as e:  # pylint: disable=broad-exception-caught
        error_msg = f"❌ **Erro de Importação**: {str(e)}\n\nVerifique se o módulo `agente_investimento` está disponível."
        with st.chat_message("assistant"):
            st.error(error_msg)
        messages.append({"role": "assistant", "content": error_msg})

    except Exception as e:  # pylint: disable=broad-exception-caught
        error_msg = f"❌ **Erro ao processar**: {str(e)}\n\nTente novamente ou verifique suas configurações."
        with st.chat_message("assistant"):
            st.error(error_msg)
        messages.append({"role": "assistant", "content": error_msg})

        # Log do erro para debug (opcional - remover em produção)
        if st.checkbox("Mostrar detalhes do erro"):
            st.exception(e)