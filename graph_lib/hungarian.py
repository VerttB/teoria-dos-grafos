import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment


def resolver_emparelhamento_hungaro(G: nx.Graph):
    """
    Resolve o emparelhamento de custo mínimo em um grafo bipartido ponderado
    utilizando o algoritmo Húngaro (via scipy.optimize.linear_sum_assignment).

    Retorna: (matching_edges, custo_total, nodes_A, nodes_B)
      - matching_edges: lista de tuplas (u, v) representando as arestas do emparelhamento ótimo.
      - custo_total: soma dos pesos das arestas do emparelhamento.
      - nodes_A: lista ordenada de vértices do conjunto de partição A.
      - nodes_B: lista ordenada de vértices do conjunto de partição B.
    """
    if G.number_of_nodes() == 0:
        raise ValueError("O grafo está vazio!")

    if not nx.is_bipartite(G):
        raise ValueError("O grafo fornecido não é bipartido!")

    color = nx.bipartite.color(G)
    A = sorted([n for n, c in color.items() if c == 0])
    B = sorted([n for n, c in color.items() if c == 1])

    n, m = len(A), len(B)

    # calcula big M para arestas inexistentes
    pesos = [data.get("weight", 1.0) for _, _, data in G.edges(data=True)]
    soma_pesos = sum(abs(p) for p in pesos)
    M = (soma_pesos * 10) + 1000.0

    cost_matrix = np.full((n, m), M)
    for i, u in enumerate(A):
        for j, v in enumerate(B):
            if G.has_edge(u, v):
                cost_matrix[i, j] = G[u][v].get("weight", 1.0)

    # executa o algoritmo húngaro para encontrar a melhor atribuição
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    matching_edges = []
    custo_total = 0.0

    for r, c in zip(row_ind, col_ind):
        val_custo = cost_matrix[r, c]
        if val_custo < M / 2:
            u = A[r]
            v = B[c]
            matching_edges.append((u, v))
            custo_total += val_custo

    return matching_edges, custo_total, A, B


def desenhar_e_salvar_emparelhamento(
    G: nx.Graph,
    matching_edges: list,
    A: list,
    B: list,
    custo_total: float,
    caminho_saida: str,
):
    """
    Gera e salva a visualização do grafo bipartido ponderado, destacando o emparelhamento ótimo.

    Formatação estipulada:
    - Arestas do emparelhamento em Azul Royal (#3b82f6), espessas.
    - Demais arestas em Cinza (#cbd5e1), finas.
    - Nós em cores neutras e rótulos de nós visíveis.
    - Pesos das arestas visíveis.
    """
    fig, ax = plt.subplots(figsize=(10, 8), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")

    pos = nx.bipartite_layout(G, A)

    # cria um conjunto das arestas do emparelhamento para busca rápida
    matching_set = set()
    for u, v in matching_edges:
        matching_set.add(tuple(sorted((u, v))))

    edges_matching = []
    edges_other = []

    # Separa as arestas em emparelhadas (azul) e não emparelhadas (cinza)
    for u, v in G.edges():
        edge_sorted = tuple(sorted((u, v)))
        if edge_sorted in matching_set:
            edges_matching.append((u, v))
        else:
            edges_other.append((u, v))

    nx.draw_networkx_edges(
        G, pos, edgelist=edges_other, edge_color="#cbd5e1", width=1.5, ax=ax
    )
    nx.draw_networkx_edges(
        G, pos, edgelist=edges_matching, edge_color="#3b82f6", width=4.0, ax=ax
    )

    # Desenha os nós da partição A em azul claro
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=A,
        node_color="#dbeafe",
        node_size=900,
        edgecolors="#2563eb",
        linewidths=1.5,
        ax=ax,
    )
    # Desenha os nós da partição B em verde claro
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=B,
        node_color="#dcfce7",
        node_size=900,
        edgecolors="#16a34a",
        linewidths=1.5,
        ax=ax,
    )
    # Desenha os identificadores/nomes nos nós
    nx.draw_networkx_labels(
        G, pos, font_color="#1e293b", font_size=11, font_weight="bold", ax=ax
    )

    # Obtém e formata os pesos das arestas para exibir no gráfico
    edge_labels = nx.get_edge_attributes(G, "weight")
    formatted_labels = {}
    for edge, w in edge_labels.items():
        if isinstance(w, (int, float)) and float(w).is_integer():
            formatted_labels[edge] = int(w)
        else:
            formatted_labels[edge] = w

    # Desenha os pesos sobre as arestas correspondentes
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=formatted_labels,
        font_color="#475569",
        font_size=9,
        font_weight="normal",
        rotate=True,
        ax=ax,
    )

    # Adiciona o título com o custo total do emparelhamento
    titulo = f"Emparelhamento Ótimo de Custo Mínimo\nCusto Total: {custo_total}"
    plt.title(titulo, fontsize=14, fontweight="bold", pad=20, color="#1e293b")
    ax.axis("off")

    # Salva a imagem gerada e fecha a figura
    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"-> Imagem de saída salva: {caminho_saida}")
