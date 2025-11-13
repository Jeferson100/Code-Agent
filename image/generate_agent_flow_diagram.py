"""
Script para gerar diagrama do fluxo do CodeAgentReact
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Configuração da figura
fig, ax = plt.subplots(1, 1, figsize=(18, 14))
ax.set_xlim(0, 12)
ax.set_ylim(0, 12)
ax.axis('off')

# Cores
color_user = '#4A90E2'  # Azul
color_agent = '#50C878'  # Verde
color_tool = '#FF6B6B'  # Vermelho
color_decision = '#FFD93D'  # Amarelo
color_flow = "#0B0A0C"  # Roxo
color_loop = '#E17055'  # Laranja
color_cetas_tools = "#200AAE"  # Laranja

# Função para criar caixas arredondadas
def create_box(ax, x, y, width, height, text, color, text_color='white', fontsize=10):
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.15",
        edgecolor='black',
        facecolor=color,
        linewidth=2.5
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', 
            color=text_color, fontsize=fontsize, weight='bold', wrap=True)

# Função para criar setas
def create_arrow(ax, x1, y1, x2, y2, label='', color='black', style='->', offset=0.3):
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        mutation_scale=25,
        color=color,
        linewidth=2.5,
        zorder=1
    )
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x, mid_y + offset, label, ha='center', va='bottom',
                fontsize=9, bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                edgecolor=color, linewidth=1.5, alpha=0.9), weight='bold')

# === NÓS PRINCIPAIS ===

# Usuário
create_box(ax, 6, 10.5, 2.5, 1, 'Usuario\n(Input)', color_user)

# Agente ReAct (LLM) - Central
create_box(ax, 6, 8, 3.5, 1.5, 'CodeAgentReact\n(LLM + ReAct Pattern)\nReasoning + Acting', color_agent, fontsize=11)

# === FERRAMENTAS (Organizadas em grupos) ===

# Grupo 1: Planejamento e Reflexão (esquerda)
create_box(ax, 1.5, 6.5, 2, 1, 'think_tool\nReflexao Estrategica', color_tool, fontsize=9)

create_box(ax, 1.5, 4.5, 2, 1, 'write_todos\nCriar/Atualizar TODOs', color_tool, fontsize=9)

create_box(ax, 1.5, 2.5, 2, 1, 'read_todos\nLer TODOs Atuais', color_tool, fontsize=9)

# Grupo 2: Execução (direita)
create_box(ax, 10.5, 6.5, 2, 1, 'web_search\nBusca Web (Tavily API)', color_tool, fontsize=9)

create_box(ax, 10.5, 4.5, 2, 1, 'write_code\nGerar Codigo\n', color_tool, fontsize=9)

# Resposta Final
create_box(ax, 6, 1, 2.5, 1, 'Resposta Final\npara Usuario', color_user)

# === SETAS E FLUXOS ===

# Fluxo principal: Usuário -> Agente
create_arrow(ax, 6, 10, 6, 9, '1. Mensagem', color_flow, offset=0.4)

# Agente -> Ferramentas (Think Tool)
create_arrow(ax, 4.0, 8, 2.5, 6.5, '', color_cetas_tools, offset=0.3)

# Agente -> Ferramentas (Write Todos)
create_arrow(ax, 4.0, 8, 2.5, 5, '', color_cetas_tools, offset=0.3)


# Agente -> Ferramentas (Read Todos)
create_arrow(ax, 4.0, 8, 2.5, 3, '', color_cetas_tools, offset=0.3)

# Agente -> Ferramentas (Web Search)
create_arrow(ax, 8, 8, 9.5, 7, '', color_cetas_tools, offset=0.3)

# Agente -> Ferramentas (Write Code)
create_arrow(ax, 8, 8, 9.5, 4.5, '', color_cetas_tools, offset=0.3)

# Loop de volta ao agente (ciclo ReAct)
#create_arrow(ax, 3, 8.5, 3, 9.5, '', color_loop, style='->', offset=0)
#create_arrow(ax, 3, 9.5, 4.5, 9.5, '3. Loop ReAct\n(Reasoning)', color_loop, offset=0.5)
#create_arrow(ax, 4.5, 9.5, 4.5, 8.5, '', color_loop, style='->', offset=0)

# Agente -> Resposta Final
create_arrow(ax, 6, 7.2, 6, 2.5, '4. Resposta Final', color_flow, offset=0.4)

# Título
ax.text(6, 11.8, 'Fluxo do CodeAgentReact - Padrão ReAct (Reasoning + Acting)', 
        ha='center', va='top', fontsize=18, weight='bold')

# Subtítulo explicativo
ax.text(9.5, 11.3, 'O agente decide dinamicamente qual ferramenta usar baseado no contexto', 
        ha='center', va='top', fontsize=11, style='italic', color='gray')

# Legenda
legend_elements = [
    mpatches.Patch(color=color_user, label='Usuario/Entrada'),
    mpatches.Patch(color=color_agent, label='Agente (LLM)'),
    mpatches.Patch(color=color_tool, label='Ferramentas Disponiveis'),
    mpatches.Patch(color=color_flow, label='Fluxo Principal'),
    mpatches.Patch(color=color_loop, label='Ciclo ReAct'),
]

ax.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.95, 
          edgecolor='black', fancybox=True)

# Notas detalhadas
notes = """PADRAO REACT:
1. REASONING: Agente analisa a mensagem e decide qual acao tomar
2. ACTING: Executa a ferramenta escolhida (se necessario)
3. OBSERVATION: Recebe resultado da ferramenta
4. LOOP: Retorna ao passo 1 ate ter informacao suficiente
5. RESPONSE: Gera resposta final para o usuario

FERRAMENTAS:
• think_tool: Reflexao estrategica após cada ferramenta ser usada
• write_todos: Criar/atualizar lista de tarefas 
• read_todos: Ler lista atual de tarefas 
• web_search: Buscar informações na web 
• write_code: Gerar codigo usando grafo interno 

O agente pode chamar multiplas ferramentas."""

ax.text(0.28, 10, notes, ha='left', va='top', fontsize=9,
        bbox=dict(boxstyle='round,pad=0.8', facecolor='#FFF9E6', 
        edgecolor='#FFD93D', linewidth=2, alpha=0.95))

# Adicionar seta circular indicando o ciclo
circle_path = mpatches.Circle((6, 8.5), 2.5, fill=False, edgecolor=color_loop, 
                         linewidth=2, linestyle='--', alpha=0.5, zorder=0)
ax.add_patch(circle_path)
ax.text(6, 6, 'Ciclo ReAct', ha='center', va='center', fontsize=10, 
        style='italic', color=color_loop, weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('code_agent_react_flow.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig('code_agent_react_flow.svg', format='svg', bbox_inches='tight', facecolor='white')
print("Diagrama gerado: code_agent_react_flow.png e code_agent_react_flow.svg")
plt.close()
