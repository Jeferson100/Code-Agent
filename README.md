# 🤖 Agente de Codificação Inteligente com LangGraph

|||
|-----------|-----------|
| **Testing**  | [![Unit Test](https://github.com/Jeferson100/Code-Agent/actions/workflows/teste.yml/badge.svg)](https://github.com/Jeferson100/Code-Agent/actions/workflows/teste.yml)|
| **Package**  | ![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=flat&logo=python) ![LangGraph](https://img.shields.io/badge/LangGraph-0.6.7-green?style=flat) ![LangChain](https://img.shields.io/badge/LangChain-0.3.27-green?style=flat) ![Groq](https://img.shields.io/badge/Groq-API-green?style=flat) ![Tavily](https://img.shields.io/badge/Tavily-Search-yellow?style=flat) ![Pydantic AI](https://img.shields.io/badge/Pydantic%20AI-0.8.1-purple?style=flat) ![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-green?style=flat&logo=streamlit) ![Chainlit](https://img.shields.io/badge/Chainlit-2.8.1-blue?style=flat) ![FastAPI](https://img.shields.io/badge/FastAPI-0.116.2-red?style=flat&logo=fastapi) ||
| **App Streamlit** | <p align=""><a href="https://code-agent-2.streamlit.app/" target="_blank"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App"/></a></p> ||
| | |

Um Deep Agente de IA para assistência em programação, construído com **LangChain** para orquestração de fluxos de trabalho complexos, múltiplos provedores de LLM e interfaces de usuário modernas.

## 📋 Visão Geral

Este projeto implementa um **sistema de agentes de codificação stateful** que combina múltiplos modelos de linguagem (LLMs) com ferramentas externas para criar um assistente de programação inteligente e autônomo. O sistema oferece duas abordagens principais:

## ✨ Características Principais

### 🧠 Capacidades do Agente
- 🎯 **Gerar código** a partir de especificações em linguagem natural
- 🔍 **Analisar e depurar** código existente com feedback iterativo
- 🔧 **Refatorar código** para melhorar qualidade e performance
- 🌐 **Buscar informações** na web para contexto adicional
- ⚡ **Executar e validar** código Python em tempo real
- 🔄 **Auto-correção** através de ciclos de feedback supervisionados
- 📝 **Gerenciar tarefas** com sistema integrado de TODOs
- 🤔 **Reflexão estratégica** antes de entregar respostas

### 🛠️ Ferramentas Integradas
- **Tavily Search**: Busca de informação na web, usando Tavily como motor de busca de conteúdo.
- **Sistema de TODOs**: Sistema de gerenciamento de tarefas. Tem como objetivo ajudar o agente a organizar e priorizar suas tarefas e evitar alucinações.
- **Geração de Código**: Ferramenta especializada para criação de código. Utiliza o modelo de LLM `qwen/qwen3-coder-480b-a35b-instruct` para gerar o código.
- **Reflexão Estratégica**: Utiliza uma ferramenta para realizar reflexões estratégicas antes de entregar respostas.
- **Múltiplos LLMs**: Groq, HuggingFace, NVIDIA AI, Cerebras, Pydantic AI

### 🎨 Múltiplas Interfaces
- **Streamlit**: Interface web interativa e responsiva
- **Chainlit**: Chat interface moderna e conversacional
- **FastAPI**: API REST para integração com outros sistemas
- **CLI**: Interface de linha de comando
- **Docker**: Execução em containers Docker

## 📁 Estrutura do Projeto

```
AgenteCodificaoLangGraph/
├── 📁 src/code_agent/                    # Código principal do agente
│   ├── 📁 build_graph/                   # Construção do grafo LangGraph
│   │   └── graph.py                      # GraphBuilder - construtor do workflow
│   ├── 📁 creat_react_code_agent/        # Agente React (nova implementação)
│   │   └── code_agent_react.py          # CodeAgentReact - agente reativo
│   ├── 📁 nodes/                         # Nós especializados do workflow
│   │   ├── node_codes.py                 # Geração de código
│   │   ├── node_supervisor.py           # Supervisão e feedback
│   │   ├── node_return_message.py       # Formatação de respostas
│   │   └── should_continue.py           # Lógica de decisão
│   ├── 📁 get_routem_llm/                # Roteamento inteligente de LLMs
│   │   ├── routem_llm.py                # Router principal com fallback
│   │   ├── get_llm.py                   # Cliente Groq
│   │   ├── router_groq.py               # Router Groq
│   │   ├── router_nvidia.py             # Router NVIDIA AI Endpoints
│   │   ├── router_cerebras.py           # Router Cerebras
│   │   └── router_pydantic_ai.py        # Router Pydantic AI
│   ├── 📁 get_models_api/                # APIs de modelos disponíveis
│   │   ├── get_all_models.py            # Agregador de modelos
│   │   ├── get_models_avalaible_groq.py # Modelos Groq
│   │   ├── get_models_nvidia.py         # Modelos NVIDIA
│   │   └── get_models_avalaible_cerebras.py # Modelos Cerebras
│   ├── 📁 states_outputs/                # Definições de estados e saídas
│   │   ├── states.py                    # StateCode, DeepAgentState, Todo
│   │   └── output_structured.py         # Estruturas de saída Pydantic
│   ├── 📁 prompts/                       # Templates de prompts
│   │   └── prompts.py                   # Prompts para todos os agentes
│   ├── 📁 tools/                         # Ferramentas externas
│   │   ├── think_tavily.py              # Busca web e reflexão
│   │   ├── todos.py                     # Sistema de gerenciamento de TODOs
│   │   └── tool_write_code.py           # Ferramenta de geração de código
│   └── 📁 utils/                         # Utilitários
│       └── get_today.py                 # Utilitário de data
├── 📁 app/                               # Interfaces de usuário
│   ├── app_code_streamlit.py            # Interface Streamlit
│   ├── app_chainlit.py                  # Interface Chainlit
│   ├── app_fastapi.py                   # API REST
│   └── graph_cli.py                     # Interface CLI
├── 📁 tests/                             # Testes automatizados (14 testes)
│   ├── conftest.py                      # Configuração e mocks
│   ├── test_graph_builder.py            # Testes do GraphBuilder
│   ├── test_node_*.py                   # Testes dos nós
│   ├── test_routem_llm.py               # Testes do roteamento
│   ├── test_get_llm.py                  # Testes do cliente Groq
│   └── test_*.py                        # Outros testes
├── 📁 notebooks/                         # Jupyter notebooks de exemplo
│   ├── agent_com_todo.ipynb             # Exemplo com sistema de TODOs
│   ├── avaliando_agente.ipynb           # Avaliação do agente
│   ├── criando_agente_codificacao.ipynb # Criação de agentes
│   └── *.ipynb                          # Outros exemplos
├── 📁 data/                              # Dados e modelos
│   ├── all_models.json                  # Lista de modelos disponíveis
│   └── get_models.py                    # Script para obter modelos
├── 📄 pyproject.toml                     # Configuração do projeto
├── 📄 requirements.txt                   # Dependências
├── 📄 docker-compose.yml                # Docker Compose
├── 📄 Dockerfile                        # Docker
└── 📄 Makefile                          # Comandos de automação
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.12+
- Chaves de API (Groq, Tavily, HuggingFace, NVIDIA AI Endpoints, Cerebras, Pydantic AI)

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/AgenteCodificaoLangGraph.git
cd AgenteCodificaoLangGraph
```

### 2. Instale as Dependências
```bash
# Criando ambiente virtual com uv
uv venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalando dependências
uv pip install -e .
```

### 3. Configure as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# LLM APIs
GROQ_API_KEY="sua_chave_groq_aqui"
TAVILY_API_KEY="sua_chave_tavily_aqui"
HUGGINGFACE_API_TOKEN="seu_token_huggingface_aqui"
NVIDIA_API_KEY="sua_chave_nvidia_aqui"
CEREBRAS_API_KEY="sua_chave_cerebras_aqui"
PYDANTIC_API_KEY="sua_chave_pydantic_aqui"
```

## 🎮 Como Usar

### 🐳 Executando com Docker

```bash
# Build e execução
docker build -t agente-codificacao-app .
docker run -p 3000:3000 agente-codificacao-app

# Ou com Docker Compose
docker-compose build
docker-compose up
```

### 🚀 Interface Streamlit

<p align=""><a href="https://code-agent-2.streamlit.app/" target="_blank"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Streamlit App"/></a></p> 


**Local**:
```bash
streamlit run app/app_code_streamlit.py
```
Acesse `http://localhost:8501` no seu navegador.

### 💬 Interface Chainlit (Chat)

```bash
chainlit run app/app_chainlit.py
```
Acesse `http://localhost:8000` no seu navegador.

### 🔌 API REST (FastAPI)

```bash
uvicorn app.app_fastapi:app --reload --port 8000
```
Acesse `http://localhost:8000/docs` para a documentação interativa.

## 📊 Tecnologias Utilizadas

### Core Framework
- **LangGraph 0.6.7**: Orquestração de workflows
- **LangChain 0.3.27**: Framework de LLMs
- **Pydantic AI 0.8.1**: Integração com HuggingFace

### Provedores LLM
- **Groq 0.31.0**: Modelos de linguagem rápidos
- **HuggingFace**: Modelos open-source
- **NVIDIA AI Endpoints**: Modelos empresariais
- **Cerebras**: Modelos especializados
- **Tavily 0.7.12**: Busca inteligente na web

### Interfaces
- **Streamlit 1.50.0**: Interface web
- **Chainlit 2.8.1**: Chat interface
- **FastAPI 0.116.2**: API REST
- **Uvicorn**: Servidor ASGI

### Desenvolvimento
- **Pytest 7.1.3**: Testes unitários
- **Ruff 0.9.6**: Linting e formatação
- **MyPy 1.15.0**: Verificação de tipos
- **PyRefly 0.34.0**: Análise de código


## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 📞 Contatos

| GitHub | LinkedIn |
|--------|---------|
| [![GitHub](https://img.shields.io/badge/github-100000?style=for-the-badge&logo=github)](https://github.com/Jeferson100) | [![LinkedIn](https://img.shields.io/badge/linkedin-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/jefersonsehnem/) |

