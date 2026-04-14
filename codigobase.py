import networkx as nx
import matplotlib.pyplot as plt
import os


def ler_grafo_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e cria um grafo/dígrafo (ponderado ou não).

    Formato esperado:
    1ª linha: [G|D] [N|W]
        G = Grafo não direcionado
        D = Dígrafo
        N = Não ponderado
        W = Ponderado
    Demais linhas:
        Se não ponderado: u v
        Se ponderado:     u v w
    """
    try:
        with open(nome_arquivo, "r") as f:
            linhas = [linha.strip() for linha in f if linha.strip()]

        if not linhas:
            print("Arquivo vazio!")
            return None, False

        # Definição do tipo de grafo
        tipo, peso = linhas[0].split()
        if tipo == "G":
            G = nx.Graph()
        elif tipo == "D":
            G = nx.DiGraph()
        else:
            raise ValueError("Primeiro caractere deve ser 'G' ou 'D'.")

        ponderado = peso == "W"

        # Leitura das arestas
        for linha in linhas[1:]:
            partes = linha.split()
            if ponderado:
                if len(partes) != 3:
                    raise ValueError("Esperado formato 'u v w' para grafos ponderados.")
                u, v, w = partes
                adicionar_aresta(G, u, v, w, ponderado)
            else:
                if len(partes) != 2:
                    raise ValueError(
                        "Esperado formato 'u v' para grafos não ponderados."
                    )
                u, v = partes
                adicionar_aresta(G, u, v, ponderado)  # peso padrão 1

        print(
            f"Grafo criado ({'dígrafo' if tipo == 'D' else 'grafo'}, "
            f"{'ponderado' if ponderado else 'não ponderado'}) com "
            f"{G.number_of_nodes()} vértices e {G.number_of_edges()} arestas."
        )
        return G, ponderado

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return None, False


def adicionar_vertice(G, v):
    """Adiciona um vértice ao grafo, se não existir."""
    if v not in G:
        G.add_node(v)
        print(f"Vértice '{v}' adicionado.")
    else:
        print(f"Vértice '{v}' já existe.")


def adicionar_aresta(G, u, v, w=1, ponderado=False):
    """Adiciona uma aresta ao grafo."""
    if ponderado:
        G.add_edge(u, v, weight=float(w))
        print(f"Aresta '{u} - {v}' com peso {w} adicionada.")
    else:
        G.add_edge(u, v)
        print(f"Aresta '{u} - {v}' adicionada.")


def visualizar_grafo(G, ponderado=False):
    """Desenha o grafo (ou dígrafo) com ou sem pesos."""
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="black",
        node_size=1000,
        font_size=12,
        arrows=isinstance(G, nx.DiGraph),
        arrowsize=20,
    )

    # Se for ponderado, mostrar pesos
    if ponderado:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.savefig("visualizacao_grafo.png")


def graph_to_adjacency_matrix(G: nx.Graph | nx.DiGraph):
    """Converte um grafo para sua matriz de adjacência."""

    matrix = []
    nodes_list = list(G.nodes())
    number_of_nodes = len(nodes_list)
    for i in range(number_of_nodes):
        row = []
        for j in range(number_of_nodes):
            if G.has_edge(nodes_list[i], nodes_list[j]):
                row.append(get_edge_weight(G, (nodes_list[i], nodes_list[j])))
            else:
                row.append(0)
        matrix.append(row)
    return matrix


def graph_to_incidence_matrix(G):
    """Converte um grafo para sua matriz de incidência."""
    edges_list = list(G.edges())
    nodes_list = list(G.nodes())
    matrix = []

    for node in nodes_list:
        row = []
        for u, v in edges_list:
            if isinstance(G, nx.DiGraph):
                if node == u:
                    row.append(-1)
                elif node == v:
                    row.append(1)
                else:
                    row.append(0)
            else:
                if node == u or node == v:
                    row.append(1)
                else:
                    row.append(0)
        matrix.append(row)

    return matrix


def graph_to_adjacent_list(G: nx.Graph | nx.DiGraph):
    """Converte um grafo para sua lista de adjacências."""
    adj = {}
    nodes_list = list(G.nodes())
    for node in nodes_list:
        adj[node] = []
        for node2 in nodes_list:
            if node == node2:
                continue
            if G.has_edge(node, node2):
                adj[node].append(node2)

    return adj


def has_node_in_edge(edges, node):
    """Verifica se um nó está presente em alguma aresta do grafo."""
    return node in edges


def get_edge_weight(G, edges):
    """Retorna o peso da aresta, se existir. Nome corrigido."""
    u, v = edges
    if G.has_edge(u, v):
        return G[u][v].get("weight", 1)
    return 1


def graph_dfs_rec(
    G: nx.Graph | nx.DiGraph,
    start_node,
    destination_node,
    max_depth: int,
    depth: int,
    possible_paths: list,
    possible_trails: list,
    path: list = None,
    trail: list[frozenset] = None,
):
    path.append(start_node)
    print(f"Visitando nodo {start_node}, profundidade {depth}...")
    print(f"Caminho atual: {path}")

    if start_node == destination_node:
        possible_paths.append(list(path))

        possible_trails.append(list(trail))

    if depth >= max_depth:
        path.pop()
        print(
            f"Profundidade máxima {max_depth} atingida em nodo {start_node}, retornando..."
        )
        return

    for neighbor in G.neighbors(start_node):
        edge = frozenset({start_node, neighbor})
        if edge not in trail:
            trail.append(edge)
            graph_dfs_rec(
                G,
                start_node=neighbor,
                destination_node=destination_node,
                depth=depth + 1,
                max_depth=max_depth,
                possible_paths=possible_paths,
                possible_trails=possible_trails,
                path=path,
                trail=trail,
            )
            trail.pop()

    path.pop()
    print(f"Retornando do nodo {start_node}, caminho atual: {path}")
    return


def graph_dfs(G, start_node, destination_node, max_depth):
    possible_paths = []
    possible_trails = []
    graph_dfs_rec(
        G=G,
        start_node=start_node,
        destination_node=destination_node,
        max_depth=max_depth,
        depth=0,
        possible_paths=possible_paths,
        possible_trails=possible_trails,
        path=[],
        trail=[],
    )
    formated = [[tuple(sorted(edge)) for edge in trail] for trail in possible_trails]

    return possible_paths, formated


def print_matrix(matrix):
    """Imprime uma matriz de forma legível."""
    if isinstance(matrix, dict):
        for key, value in matrix.items():
            print(f"{key}: {value}")
        return

    for row in matrix:
        print("|", end="")
        for column in row:
            print(column, end="\t")

        print("|")


# -------------------------------
# Exemplo de uso do programa
# -------------------------------
if __name__ == "__main__":
    # Ler grafo a partir de arquivo
    system_dir = "/home/massa/codigosPython/TGrafos/base_grafos/"
    nome_arquivo = "grafo.txt"  # Arquivo de entrada
    file = os.path.join(system_dir, nome_arquivo)
    # usar caminho completo se existir, caso contrário tentar arquivo local
    path = file if os.path.exists(file) else nome_arquivo
    G, ponderado = ler_grafo_arquivo(path)

    if G is None:
        print("Nenhum grafo carregado. Encerrando.")
        exit(1)

    # Adicionar vértice manualmente
    #    adicionar_vertice(G, "E")

    # Adicionar aresta manualmente
    #    adicionar_aresta(G, "E", "A")

    visualizar_grafo(G, ponderado)
    # print("Matriz de Adjacência:")
    # print_matrix(graph_to_adjacency_matrix(G))

    # print("Matriz de Incidência:")
    # print_matrix(graph_to_incidence_matrix(G))

    # print("Lista de Adjacências:")
    # print_matrix(graph_to_adjacent_list(G))

    print("Busca em Profundidade (DFS) de A para D, profundidade máxima 3:")
    paths, trails = graph_dfs(G, "A", "A", 4)
    print("Caminhos encontrados:")
    for path in paths:
        print(path)
    print("Trilhas encontradas:")
    for trail in trails:
        print(trail)
