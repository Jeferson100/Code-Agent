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

### 🛠️ Ferramentas Integradas no CodeAgentReact

O `CodeAgentReact` vem com um conjunto completo de ferramentas que permitem ao agente realizar tarefas complexas de programação de forma autônoma e eficiente:

#### 🔍 **web_search** - Busca Inteligente na Web
- **Descrição**: Realiza buscas na web usando a API Tavily para obter informações atualizadas e relevantes
- **Quando usar**: 
  - Quando precisa de informações sobre APIs, bibliotecas ou frameworks
  - Para buscar documentação atualizada
  - Para encontrar exemplos de código ou soluções
  - Quando precisa de contexto sobre tecnologias específicas
- **Parâmetros**:
  - `query`: String de busca (seja específico e claro)
  - `max_results`: Número máximo de resultados (padrão: 5)
  - `include_images`: Incluir imagens nos resultados (padrão: False)
- **Retorna**: Lista de resultados com título, conteúdo e URL

#### 🤔 **think_tool** - Reflexão Estratégica
- **Descrição**: Ferramenta para reflexão estratégica sobre o progresso da pesquisa e tomada de decisões
- **Quando usar**:
  - Após receber resultados de busca: "Que informações importantes encontrei?"
  - Antes de decidir próximos passos: "Tenho informações suficientes?"
  - Ao avaliar lacunas na pesquisa: "Que informações ainda faltam?"
  - Antes de concluir a pesquisa: "Posso fornecer uma resposta completa agora?"
- **Análise deve abordar**:
  1. Análise dos achados atuais
  2. Avaliação de lacunas
  3. Avaliação de qualidade das evidências
  4. Decisão estratégica sobre continuar ou responder
- **Retorna**: Confirmação de que a reflexão foi registrada

#### 📝 **write_todos** - Gerenciamento de Tarefas
- **Descrição**: Cria e gerencia listas estruturadas de tarefas (TODOs) para planejamento e rastreamento de progresso
- **Quando usar**:
  - No início de tarefas complexas com múltiplos passos
  - Quando o usuário fornece múltiplas tarefas
  - Para organizar e priorizar trabalho
  - Para evitar alucinações e manter foco
- **Estrutura**:
  - Cada TODO tem: `content` (descrição) e `status` (pending, in_progress, completed)
  - Limite: até 3 chamadas por sessão (plano inicial + atualização + revisão final)
- **Retorna**: Comando para atualizar o estado do agente com a nova lista de TODOs

#### 📖 **read_todos** - Leitura de Tarefas
- **Descrição**: Lê a lista atual de TODOs do estado do agente para manter contexto e foco
- **Quando usar**:
  - Ao mudar de contexto ou retomar trabalho
  - Para verificar progresso e tarefas pendentes
  - Antes de marcar uma tarefa como concluída
  - Para manter foco em tarefas complexas
- **Limite**: Até 5 chamadas por sessão
- **Retorna**: String formatada com a lista atual de TODOs, incluindo emojis de status (⏳ pending, 🔄 in_progress, ✅ completed)

#### 💻 **write_code** - Geração de Código Especializada
- **Descrição**: Ferramenta especializada para gerar, melhorar ou explicar código usando um modelo LLM especializado em programação
- **Modelo utilizado**: `qwen/qwen3-coder-480b-a35b-instruct` (via NVIDIA AI)
- **Quando usar**:
  - Para gerar código a partir de especificações em linguagem natural
  - Para refatorar ou melhorar código existente
  - Para explicar código complexo
  - Para criar funções, classes ou scripts completos
- **Limite**: Até 3 chamadas por sessão (para evitar uso excessivo)
- **Funcionalidades**:
  - Gera código com feedback iterativo
  - Inclui validação e supervisão automática
  - Retorna código formatado e documentado
- **Retorna**: Comando com código gerado formatado em blocos de código

#### 🔄 **Sistema de Workflow Integrado**
- O `write_code` utiliza internamente um workflow LangGraph completo que inclui:
  - **Geração de código**: Usa o modelo especializado para criar código
  - **Supervisão automática**: Valida e revisa o código gerado
  - **Feedback iterativo**: Permite correções e melhorias
  - **Limite de interações**: Máximo de 2 iterações para evitar loops infinitos

### 🔌 **Múltiplos Provedores LLM com Fallback Automático**
O sistema suporta múltiplos provedores de LLM com roteamento inteligente e fallback automático:
- **Groq**: Modelos rápidos e eficientes
- **HuggingFace**: Modelos open-source via Pydantic AI
- **NVIDIA AI Endpoints**: Modelos empresariais de alta qualidade
- **Cerebras**: Modelos especializados
- **Sistema de Fallback**: Tenta automaticamente o próximo provedor em caso de falha

### 🔗 **Fluxo de Trabalho das Ferramentas**

As ferramentas são projetadas para trabalhar em conjunto de forma inteligente:

1. **Planejamento** → `write_todos`: Cria plano de ação para tarefas complexas
2. **Pesquisa** → `web_search`: Busca informações necessárias na web
3. **Reflexão** → `think_tool`: Analisa resultados e decide próximos passos
4. **Verificação** → `read_todos`: Verifica progresso e mantém foco
5. **Execução** → `write_code`: Gera código especializado com validação
6. **Iteração** → O ciclo se repete conforme necessário até completar a tarefa

**Exemplo de Fluxo Automático:**
```
Usuário: "Crie uma API REST com FastAPI que autentica usuários"
  ↓
1. write_todos → Cria plano: [pesquisar FastAPI, criar estrutura, implementar auth]
  ↓
2. web_search → Busca "FastAPI authentication best practices"
  ↓
3. think_tool → Analisa: "Tenho informações suficientes sobre JWT e FastAPI"
  ↓
4. read_todos → Verifica: "Próxima tarefa: implementar autenticação"
  ↓
5. write_code → Gera código completo com validação
  ↓
6. read_todos → Marca tarefa como concluída
```

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
│   │   ├── __init__.py
│   │   └── graph.py                      # GraphBuilder - construtor do workflow
│   ├── 📁 creat_react_code_agent/        # Agente React 
│   │   ├── __init__.py
│   │   └── code_agent_react.py           # CodeAgentReact - agente reativo com ferramentas
│   ├── 📁 nodes/                         # Nós especializados do workflow
│   │   ├── __init__.py
│   │   ├── node_codes.py                 # Geração de código
│   │   ├── node_supervisor.py           # Supervisão e feedback
│   │   ├── node_return_message.py       # Formatação de respostas
│   │   └── should_continue.py           # Lógica de decisão (END/supervisor)
│   ├── 📁 get_routem_llm/                # Roteamento inteligente de LLMs
│   │   ├── __init__.py
│   │   ├── routem_llm.py                # Router principal com fallback automático
│   │   ├── get_llm.py                   # Cliente Groq (GetLlmResponse)
│   │   ├── router_groq.py               # Router Groq
│   │   ├── router_nvidia.py             # Router NVIDIA AI Endpoints
│   │   ├── router_cerebras.py           # Router Cerebras
│   │   └── router_pydantic_ai.py        # Router Pydantic AI (HuggingFace)
│   ├── 📁 get_models_api/                # APIs de modelos disponíveis
│   │   ├── __init__.py
│   │   ├── get_all_models.py            # Agregador de modelos
│   │   ├── get_models_avalaible_groq.py # Modelos Groq disponíveis
│   │   ├── get_models_nvidia.py         # Modelos NVIDIA disponíveis
│   │   └── get_models_avalaible_cerebras.py # Modelos Cerebras disponíveis
│   ├── 📁 states_outputs/                # Definições de estados e saídas
│   │   ├── __init_.py
│   │   ├── states.py                    # StateCode, DeepAgentState, Todo, file_reducer
│   │   └── output_structured.py         # Estruturas de saída Pydantic
│   │       └── SupervisorResponse, CodeOutput, SearchResponse
│   ├── 📁 prompts/                       # Templates de prompts
│   │   ├── __init__.py
│   │   └── prompts.py                   # Prompts para todos os agentes
│   │       └── PROMPT_CODE, SUPERVISOR_CODE, PROMP_AGENT_CODE, etc.
│   ├── 📁 tools/                         # Ferramentas externas do CodeAgentReact
│   │   ├── __init__.py
│   │   ├── think_tavily.py              # web_search, think_tool, think_response
│   │   ├── todos.py                     # write_todos, read_todos
│   │   └── tool_write_code.py           # write_code - geração de código especializada
│   └── 📁 utils/                         # Utilitários
│       └── get_today.py                 # Utilitário de data formatada
├── 📁 app/                               # Interfaces de usuário
│   ├── __init__.py
│   ├── app_code_streamlit.py            # Interface Streamlit
│   ├── app_chainlit.py                  # Interface Chainlit (chat)
│   ├── app_fastapi.py                   # API REST (FastAPI)
│   ├── deep_agent_code_cli.py           # CLI para agente profundo
│   ├── graph_cli.py                     # CLI para grafo básico
│   └── README.md                        # Documentação das interfaces
├── 📁 tests/                             # Testes automatizados (52+ testes)
│   ├── conftest.py                      # Configuração, mocks e stubs
│   ├── test_graph_builder.py            # Testes do GraphBuilder
│   ├── test_node_code.py                # Testes do node_codes
│   ├── test_node_supervisor.py          # Testes do node_supervisor
│   ├── test_node_return_message.py      # Testes do node_return_message
│   ├── test_should_continue.py          # Testes da lógica de decisão
│   ├── test_routem_llm.py               # Testes do roteamento LLM
│   ├── test_get_llm.py                  # Testes do cliente Groq
│   ├── test_tools.py                    # Testes das ferramentas
│   ├── test_output_structured.py        # Testes dos modelos Pydantic
│   ├── test_prompts_and_state.py        # Testes de prompts e estados
│   ├── test_code_agent_react.py         # Testes do CodeAgentReact
│   └── test_utils_get_today.py          # Testes de utilitários
├── 📁 notebooks/                         # Jupyter notebooks de exemplo
│   ├── agent_com_todo.ipynb             # Exemplo com sistema de TODOs
│   ├── avaliando_agent_phoenix.ipynb     # Avaliação com Phoenix
│   ├── avaliando_agente_langsmith.ipynb  # Avaliação com LangSmith
│   ├── chamando_agente_api.ipynb         # Exemplo de chamada via API
│   ├── criando_agente_codificacao.ipynb  # Criação de agentes
│   ├── deep_agent_langchain.ipynb        # Agente profundo com LangChain
│   ├── enable_human_intervention.ipynb   # Intervenção humana
│   ├── evaluate_agent.ipynb              # Avaliação de agentes
│   ├── examples_agentes_codigos.ipynb    # Exemplos de agentes de código
│   ├── long_term_memory_agent.ipynb       # Agente com memória de longo prazo
│   ├── models_apis.ipynb                 # Modelos e APIs
│   ├── nvidia_ai_endpoints.ipynb         # NVIDIA AI Endpoints
│   ├── plan-and-execute.ipynb            # Padrão plan-and-execute
│   ├── pydantic_fire.ipynb               # Pydantic AI
│   ├── requirements_resolved.txt         # Dependências resolvidas
│   └── utils.py                          # Utilitários para notebooks
├── 📁 data/                              # Dados e modelos
│   ├── all_models.json                  # Lista completa de modelos disponíveis
│   └── get_models.py                    # Script para obter modelos das APIs
├── 📁 image/                             # Imagens e assets
│   └── image.png                        # Imagem do projeto
├── 📄 pyproject.toml                     # Configuração do projeto (Poetry/uv)
├── 📄 pyrefly.toml                       # Configuração do PyRefly
├── 📄 requirements.txt                   # Dependências Python
├── 📄 uv.lock                            # Lock file do uv
├── 📄 docker-compose.yml                # Docker Compose
├── 📄 Dockerfile                        # Docker
├── 📄 Makefile                          # Comandos de automação
├── 📄 langgraph.json                    # Configuração do LangGraph
├── 📄 chainlit.md                       # Configuração do Chainlit
└── 📄 LICENSE                            # Licença MIT
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

### 🚀 Criando um Agente React Personalizado

O `CodeAgentReact` pode ser facilmente configurado e personalizado:

```python
from src.code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact

# Criar um agente básico
agent = CodeAgentReact(
    model="mistralai/mistral-small-3.1-24b-instruct-2503",
    model_provider="nvidia",
    checkpointer=True,  # Habilita persistência de estado
    temperature=0.0     # Temperatura para geração determinística
)

# Criar o grafo do agente
graph = agent.create_agent()

# Usar o agente
response = await graph.ainvoke({
    "messages": [{"role": "user", "content": "Crie uma função Python para calcular Fibonacci"}]
})
```

#### 🔧 Configurações Disponíveis

- **model**: Nome do modelo LLM a ser usado
- **model_provider**: Provedor do modelo (`nvidia`, `groq`, `huggingface`, etc.)
- **checkpointer**: 
  - `True`: Usa `MemorySaver` para persistência em memória
  - `BaseCheckpointSaver`: Instância customizada de checkpointer
  - `False`/`None`: Sem persistência de estado
- **temperature**: Controla a aleatoriedade (0.0 = determinístico, 1.0 = criativo)
- **additional_tools**: Lista de ferramentas adicionais para estender funcionalidades

#### 📚 Exemplo Completo com Todas as Ferramentas

```python
from src.code_agent.creat_react_code_agent.code_agent_react import CodeAgentReact

# Criar agente com checkpoint
agent = CodeAgentReact(
    model="mistralai/mistral-small-3.1-24b-instruct-2503",
    model_provider="nvidia",
    checkpointer=True,
    temperature=0.0
)

graph = agent.create_agent()

# Exemplo de uso: tarefa complexa que usa múltiplas ferramentas
response = await graph.ainvoke({
    "messages": [{
        "role": "user", 
        "content": """
        Preciso criar um sistema de autenticação JWT em Python. 
        Por favor:
        1. Pesquise sobre as melhores práticas de JWT
        2. Crie um plano de implementação
        3. Gere o código completo
        """
    }]
})

# O agente automaticamente:
# 1. Usará web_search para pesquisar sobre JWT
# 2. Usará think_tool para refletir sobre os resultados
# 3. Usará write_todos para criar um plano
# 4. Usará write_code para gerar o código
# 5. Usará read_todos para verificar o progresso
```

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

