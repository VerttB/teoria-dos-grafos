import networkx as nx
import matplotlib.pyplot as plt


def heuristica_conjunto_estavel(G: nx.Graph) -> set:
    """
    Implementação da heurística gulosa de grau mínimo para encontrar um Conjunto Estável Maximal.

    Lógica:
    1. Copia o grafo original para um subgrafo de trabalho H.
    2. A cada iteração, escolhe o vértice v de grau mínimo no subgrafo restante H.
    3. Adiciona v à solução S.
    4. Remove v e todos os seus vizinhos de H.
    5. Repete até H estar vazio.
    """
    S = set()
    H = G.copy()

    while H.number_of_nodes() > 0:
        v = min(H.nodes, key=H.degree)
        S.add(v)
        vizinhos = list(H.neighbors(v))
        H.remove_node(v)
        H.remove_nodes_from(vizinhos)

    return S


def calcular_cobertura_vertices(G: nx.Graph, conjunto_estavel: set) -> set:
    """
    Identifica a cobertura de vértices pegando o complemento do conjunto estável
    em relação ao conjunto total de vértices -> v.
    """
    return set(G.nodes) - conjunto_estavel


def calcular_clique(G: nx.Graph) -> set:
    """
    Calcula um clique maximal executando a função de conjunto estável ),
    mas passando como argumento o grafo complementar.
    """
    G_comp = nx.complement(G)
    return heuristica_conjunto_estavel(G_comp)


def desenhar_e_salvar_solucao(
    G: nx.Graph, pos, solucao: set, tipo: str, caminho_saida: str
):
    """
    Gera e salva a visualização do grafo destacando os vértices e arestas da solução encontrada.
    Cores:
    - conjunto_estavel: nós da solução em verde, demais em cinza.
    - clique: nós da solução em vermelho, arestas internas do clique em vermelho, demais em cinza.
    - cobertura: nós da solução em azul, demais em cinza.
    """
    fig, ax = plt.subplots(figsize=(9, 7), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")

    nodes_sol = list(solucao)
    nodes_out = [v for v in G.nodes() if v not in solucao]

    if tipo == "conjunto_estavel":
        cor_sol = "#10b981"
        titulo = f"Conjunto Estável Maximal (Tamanho: {len(solucao)})"
        nx.draw_networkx_edges(G, pos, edge_color="#d1d5db", width=1.0, ax=ax)

    elif tipo == "cobertura":
        cor_sol = "#3b82f6"
        titulo = f"Cobertura de Vértices (Tamanho: {len(solucao)})"
        nx.draw_networkx_edges(G, pos, edge_color="#d1d5db", width=1.0, ax=ax)

    elif tipo == "clique":
        cor_sol = "#ef4444"
        titulo = f"Clique Maximal (Tamanho: {len(solucao)})"

        edges_clique = []
        edges_out = []
        for u, v in G.edges():
            if u in solucao and v in solucao:
                edges_clique.append((u, v))
            else:
                edges_out.append((u, v))

        nx.draw_networkx_edges(
            G, pos, edgelist=edges_out, edge_color="#d1d5db", width=1.0, ax=ax
        )
        nx.draw_networkx_edges(
            G, pos, edgelist=edges_clique, edge_color="#ef4444", width=2.5, ax=ax
        )
    else:
        raise ValueError(f"Tipo desconhecido: {tipo}")

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodes_out,
        node_color="#e5e7eb",
        node_size=850,
        edgecolors="#9ca3af",
        linewidths=1.0,
        ax=ax,
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodes_sol,
        node_color=cor_sol,
        node_size=850,
        edgecolors="#1e293b",
        linewidths=1.5,
        ax=ax,
    )

    labels_out = {v: str(v) for v in nodes_out}
    labels_sol = {v: str(v) for v in nodes_sol}

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels_out,
        font_color="#4b5563",
        font_size=10,
        font_weight="normal",
        ax=ax,
    )
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels_sol,
        font_color="white",
        font_size=10,
        font_weight="bold",
        ax=ax,
    )

    plt.title(titulo, fontsize=14, fontweight="bold", pad=15, color="#1e293b")
    ax.axis("off")

    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)
