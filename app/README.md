# Agente de Codificação com LangGraph e Streamlit

Este projeto implementa um agente de IA para tarefas de codificação, utilizando a biblioteca **LangGraph** para orquestrar fluxos de trabalho complexos e uma interface web interativa construída com **Streamlit**.

## 📝 Descrição

O objetivo deste agente é automatizar e auxiliar em diversas tarefas do ciclo de vida de desenvolvimento de software. Ele é projetado para ser um assistente de codificação stateful (com estado), capaz de:

-   Gerar código a partir de especificações em linguagem natural.
-   Analisar e depurar código existente.
-   Refatorar código para melhorar a qualidade, legibilidade e performance.
-   Utilizar ferramentas externas, como busca na web (Tavily/Serper), para obter informações contextuais.

A arquitetura baseada em **LangGraph** permite que o agente execute tarefas em múltiplos passos, tome decisões, avalie os resultados e corrija seu próprio trabalho, criando um ciclo de feedback robusto. A interface com **Streamlit** oferece uma maneira amigável de interagir com o agente.

## ✨ Features

-   **Orquestração com LangGraph**: Criação de um grafo de estados para fluxos de trabalho não-lineares e iterativos.
-   **Interface Web com Streamlit**: Uma UI simples e reativa para interagir com o agente.
-   **Integração com LLMs**: Flexibilidade para usar modelos de linguagem poderosos, como os disponíveis via Groq.
-   **Uso de Ferramentas**: Capacidade de estender as funcionalidades do agente com ferramentas externas (ex: busca na web).
-   **Execução via CLI**: Um ponto de entrada (`app/graph_cli.py`) para compilar e interagir com o grafo diretamente do terminal.

## 📂 Estrutura do Projeto

```
.
├── app/
│   ├── app_code_streamlit.py   # Interface do usuário com Streamlit
│   └── graph_cli.py            # Ponto de entrada para a linha de comando
├── src/
│   ├── __init__.py             # Configura o path para importações absolutas
│   └── code_agent/
│       ├── __init__.py
│       └── build_graph/
│           └── graph.py        # Lógica de construção do grafo (LangGraph)
├── .env.example                # Arquivo de exemplo para variáveis de ambiente
├── requirements.txt            # Dependências do projeto
└── README.md                   # Esta documentação
```

## 🚀 Como Começar

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

-   Python 3.9+
-   Gerenciador de pacotes `pip`

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/AgenteCodificaoLangGraph.git
    cd AgenteCodificaoLangGraph
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    -   Copie o arquivo de exemplo `.env.example` para `.env`.
    -   Adicione suas chaves de API no arquivo `.env`. O projeto requer `GROQ_API_KEY` e `API_KEY_SERPER` (ou `TAVILY_API_KEY`, dependendo da ferramenta de busca configurada).
    ```bash
    cp .env.example .env
    ```
    **Arquivo `.env`:**
    ```
    GROQ_API_KEY="..."
    TAVILY_API_KEY="..."
    ```

### Execução

Você pode interagir com o agente através da interface Streamlit.

```bash
streamlit run app/app_code_streamlit.py
```

Acesse `http://localhost:8501` no seu navegador para começar a usar o agente.

## 🤝 Contribuição

Contribuições são muito bem-vindas! Se você tem ideias para melhorias, novas features ou encontrou um bug, por favor, abra uma *issue* ou envie um *pull request*.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.