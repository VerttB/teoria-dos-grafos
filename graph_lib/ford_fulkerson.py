from collections import deque
import matplotlib.pyplot as plt
import math
import networkx as nx


def executar_ford_fulkerson(G: nx.DiGraph):
    """
    Executa o flgoritmo de ford fulkerson em uma rede de fluxo direcionada e ponderada.

    Retorna: fluxo_maximo, historico_caminhos, tabela_fluxos, G_ext, s, t, fontes_originais, sorvedouros_originais
    """
    # Garante que o grafo não esteja vazio
    if G.number_of_nodes() == 0:
        raise ValueError("O grafo está vazio!")

    # Garante que seja um dígrafo
    if not isinstance(G, nx.DiGraph):
        raise ValueError("O Algoritmo de Ford-Fulkerson exige um dígrafo (nx.DiGraph)!")

    # Identifica fontes originais (grau de entrada == 0) e sorvedouros originais (grau de saída == 0)
    fontes_originais = [v for v in G.nodes() if G.in_degree(v) == 0]
    sorvedouros_originais = [v for v in G.nodes() if G.out_degree(v) == 0]

    # Cria cópia do grafo original para estender com super-fonte e super-sorvedouro fictícios
    G_ext = G.copy()

    s = "Super_Source"
    t = "Super_Sink"

    # Conecta a super-fonte fictícia às fontes originais com capacidade infinita
    for fonte in fontes_originais:
        G_ext.add_edge(s, fonte, weight=math.inf)

    # Conecta os sorvedouros originais ao sorvedouro maior fictício com capacidade infinita
    for sorvedouro in sorvedouros_originais:
        G_ext.add_edge(sorvedouro, t, weight=math.inf)

    capacidade = {}
    fluxo = {}

    for u, v, data in G_ext.edges(data=True):
        cap = data.get("weight", 0.0)
        capacidade[(u, v)] = float(cap)
        fluxo[(u, v)] = 0.0

    historico_caminhos = []
    iteracao = 1

    # Busca em largura (BFS) manual no grafo residual para encontrar o caminho aumentante
    def bfs_caminho_aumentante():
        # Monta lista de adjacência residual baseada na capacidade residual:
        # aresta direta (u, v)cap_res = C(u, v) - f(u, v)
        # aresta reversa (v, u)cap_res = f(u, v)
        adj_residual = {}
        for node in G_ext.nodes():
            adj_residual[node] = []

        nodes_set = set(G_ext.nodes())
        for u in nodes_set:
            for v in nodes_set:
                cap_direta = capacidade.get((u, v), 0.0) - fluxo.get((u, v), 0.0)
                if cap_direta > 1e-9:
                    adj_residual[u].append((v, cap_direta, True))

                cap_reversa = fluxo.get((v, u), 0.0)
                if cap_reversa > 1e-9:
                    adj_residual[u].append((v, cap_reversa, False))

        # Fila para explorar caminhos via BFS
        queue = deque([s])
        pai = {s: None}
        aresta_usada = {}

        while queue:
            atual = queue.popleft()
            if atual == t:
                break

            for vizinho, cap_res, is_direta in adj_residual[atual]:
                if vizinho not in pai:
                    pai[vizinho] = atual
                    aresta_usada[(atual, vizinho)] = (cap_res, is_direta)
                    queue.append(vizinho)

        if t not in pai:
            return None, 0.0

        # Reconstrói o caminho percorrido da super-fonte até o super-sorvedouro
        caminho = []
        no_atual = t
        gargalo = math.inf

        while no_atual != s:
            p = pai[no_atual]
            caminho.append(no_atual)
            cap_res, _ = aresta_usada[(p, no_atual)]
            if cap_res < gargalo:
                gargalo = cap_res
            no_atual = p

        caminho.append(s)
        caminho.reverse()

        return caminho, gargalo

    # Loop do algoritmo de Ford-Fulkerson
    while True:
        caminho, gargalo = bfs_caminho_aumentante()
        if caminho is None or gargalo <= 0:
            break

        # Aumenta o fluxo ao longo das arestas do caminho
        for i in range(len(caminho) - 1):
            u = caminho[i]
            v = caminho[i + 1]

            if (u, v) in capacidade:
                fluxo[(u, v)] += gargalo
            elif (v, u) in capacidade:
                fluxo[(v, u)] -= gargalo

        historico_caminhos.append(
            {"iteracao": iteracao, "caminho": caminho, "gargalo": gargalo}
        )
        iteracao += 1

    # Calcula o fluxo máximo total como o somatório dos fluxos que saem de s
    fluxo_maximo = sum(fluxo.get((s, v), 0.0) for v in G_ext.successors(s))

    # Tabela final de fluxos por aresta
    tabela_fluxos = []
    for u, v in G_ext.edges():
        tabela_fluxos.append(
            {
                "origem": u,
                "destino": v,
                "fluxo": fluxo[(u, v)],
                "capacidade": capacidade[(u, v)],
            }
        )

    return (
        fluxo_maximo,
        historico_caminhos,
        tabela_fluxos,
        G_ext,
        s,
        t,
        fontes_originais,
        sorvedouros_originais,
    )


def formatar_val(val):
    if val == math.inf or val == float("inf") or math.isinf(val):
        return "Inf"
    if isinstance(val, (int, float)) and float(val).is_integer():
        return str(int(val))
    return f"{val:.1f}"


def desenhar_e_salvar_fluxo_maximo(
    G_ext: nx.DiGraph,
    tabela_fluxos: list,
    s: str,
    t: str,
    fontes: list,
    sorvedouros: list,
    fluxo_maximo: float,
    caminho_saida: str,
):
    """
    Gera e salva a visualização da rede de fluxo destacando as arestas ativas.
    """
    fig, ax = plt.subplots(figsize=(11, 8), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")

    # Layout espacial (passando weight=None para ignorar os pesos math.inf no cálculo de molas)
    pos = nx.spring_layout(G_ext, seed=42, weight=None)

    dict_fluxos = {
        (item["origem"], item["destino"]): item["fluxo"] for item in tabela_fluxos
    }
    dict_caps = {
        (item["origem"], item["destino"]): item["capacidade"] for item in tabela_fluxos
    }

    edges_com_fluxo = []
    edges_sem_fluxo = []
    widths_com_fluxo = []

    for u, v in G_ext.edges():
        f = dict_fluxos.get((u, v), 0.0)
        c = dict_caps.get((u, v), 0.0)
        if f > 1e-9:
            edges_com_fluxo.append((u, v))
            w = 1.5 + (2.5 * (f / c if c > 0 and c != math.inf else 1.0))
            widths_com_fluxo.append(w)
        else:
            edges_sem_fluxo.append((u, v))

    color_map = []
    for node in G_ext.nodes():
        if node == s:
            color_map.append("#f59e0b")
        elif node == t:
            color_map.append("#8b5cf6")
        elif node in fontes:
            color_map.append("#fbbf24")
        elif node in sorvedouros:
            color_map.append("#c084fc")
        else:
            color_map.append("#e2e8f0")

    nx.draw_networkx_nodes(
        G_ext,
        pos,
        node_color=color_map,
        node_size=800,
        edgecolors="#334155",
        linewidths=1.5,
        ax=ax,
    )

    if edges_sem_fluxo:
        nx.draw_networkx_edges(
            G_ext,
            pos,
            edgelist=edges_sem_fluxo,
            edge_color="#cbd5e1",
            width=1.2,
            arrows=True,
            arrowsize=14,
            node_size=800,
            ax=ax,
        )

    if edges_com_fluxo:
        nx.draw_networkx_edges(
            G_ext,
            pos,
            edgelist=edges_com_fluxo,
            edge_color="#3b82f6",
            width=widths_com_fluxo,
            arrows=True,
            arrowsize=16,
            node_size=800,
            ax=ax,
        )

    nx.draw_networkx_labels(
        G_ext, pos, font_color="#0f172a", font_size=10, font_weight="bold", ax=ax
    )

    edge_labels = {}
    for u, v in G_ext.edges():
        f = dict_fluxos.get((u, v), 0.0)
        c = dict_caps.get((u, v), 0.0)
        edge_labels[(u, v)] = f"{formatar_val(f)}/{formatar_val(c)}"

    nx.draw_networkx_edge_labels(
        G_ext,
        pos,
        edge_labels=edge_labels,
        font_color="#334155",
        font_size=8,
        font_weight="normal",
        ax=ax,
    )

    titulo = f"Algoritmo de Ford-Fulkerson - Rede de Fluxo\nFluxo Máximo Total: {fluxo_maximo}"
    plt.title(titulo, fontsize=14, fontweight="bold", pad=20, color="#0f172a")
    ax.axis("off")

    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"-> Imagem salva em: {caminho_saida}")
