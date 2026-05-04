import networkx as nx


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


def _graph_dfs_rec(
    G: nx.Graph | nx.DiGraph,
    start_node,
    destination_node,
    max_depth: int,
    depth: int,
    possible_paths: list,
    path: list = None,
):
    """
    Função recursiva para encontrar caminhos sem repetição de vértices.
    """
    if path is None:
        path = []

    path.append(start_node)

    if start_node == destination_node:
        possible_paths.append(list(path))
        path.pop()
        return

    if depth < max_depth:
        for neighbor in G.neighbors(start_node):
            if neighbor not in path:
                _graph_dfs_rec(
                    G,
                    neighbor,
                    destination_node,
                    max_depth,
                    depth + 1,
                    possible_paths,
                    path,
                )

    path.pop()


def graph_dfs(G, start_node, destination_node, max_depth):
    """
    Encontra e exibe todos os caminhos de u até v com comprimento <= k.
    Retorna o número total de caminhos (trilhas simples) encontrados.
    """
    possible_paths = []
    _graph_dfs_rec(
        G=G,
        start_node=start_node,
        destination_node=destination_node,
        max_depth=max_depth,
        depth=0,
        possible_paths=possible_paths,
        path=[],
    )

    print(
        f"\nCaminhos encontrados de '{start_node}' até '{destination_node}' com comprimento máximo {max_depth}):"
    )
    for i, p in enumerate(possible_paths, 1):
        print(f"Caminho {i}: {' -> '.join(p)} (comprimento: {len(p) - 1})")

    if not possible_paths:
        print("Nenhum caminho encontrado.")

    return len(possible_paths)


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


def check_sequence(G: nx.Graph | nx.DiGraph, S: list):
    """
    Verifica as propriedades de uma sequência de vértices S no grafo G.
    """
    if not S:
        print("Sequência vazia.")
        return

    for v in S:
        if v not in G:
            print(f"Erro: O vértice '{v}' não existe no grafo.")
            return

    is_walk = True
    seen_edges = []
    is_directed = isinstance(G, nx.DiGraph)

    for i in range(len(S) - 1):
        u, v = S[i], S[i + 1]
        if not G.has_edge(u, v):
            is_walk = False
            break
        if is_directed:
            edge = (u, v)
        else:
            edge = tuple(sorted((u, v)))
        seen_edges.append(edge)

    if not is_walk:
        print(f"A sequência {S}:")
        print(
            "- Não é um passeio válido sequência de vertices não está presente em todas as arestas."
        )
        return

    is_path = len(set(S)) == len(S)

    is_trail = len(set(seen_edges)) == len(seen_edges)

    is_circuit = is_trail and S[0] == S[-1] and len(S) > 1

    print(f"A sequência {S}:")
    print("- É um passeio válido: Sim")
    print(f"- É um caminho (sem repetição de vértices): {'Sim' if is_path else 'Não'}")
    print(f"- É uma trilha (sem repetição de arestas): {'Sim' if is_trail else 'Não'}")
    print(f"- É um circuito (trilha fechada): {'Sim' if is_circuit else 'Não'}")


def get_dfs_order(G: nx.DiGraph):
    """
    Executa uma busca em profundidade em todo o grafo e retorna os nós em ordem de fim.
    Variáveis Usadas:
    - visited: Set para rastrear os nós já visitados e evitar ciclos infinitos.
    - stack: Lista que armazena os nós na ordem em que terminam sua exploração
    """
    visited = set()
    stack = []

    def dfs(node):
        """
        Visitando nós do grafo
        """
        visited.add(node)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in G.nodes():
        """
        Entra na recusão apenas em nós não visitados, evitando ciclos sem fim
        """
        if node not in visited:
            dfs(node)

    return stack


def find_sccs_kosaraju(G: nx.DiGraph):
    """
    Implementa o algoritmo de Kosaraju-Sharir para identificar componentes fortemente conexos (SCCs).
    - Pega a ordem de término dos nós usando a funcão get_dfs_post_order.
    - Transpõe o grafo para obter o grafo reverso.
    - Realiza uma DFS no grafo reverso seguindo a ordem inversa de término para coletar os nós de cada SCC.
    Variáveis Utilizadas:
    - visited: Set para rastrear os nós já visitados e evitar ciclos infinitos.
    - order_stack: Lista que armazena os nós na ordem em que terminam sua exploração
    - G_rev: grafo invertido
    - sccs: Lista de componentes fortemente conexos
    """
    order_stack = get_dfs_order(G)

    G_rev = G.reverse(copy=True)

    visited = set()
    sccs = []

    def dfs_collect_scc(node, current_scc):
        """Função auxiliar para coletar todos os nós alcancaveis em um grafo, entra apenas em nós não visitados para evitar ciclos sem fim"""
        visited.add(node)
        current_scc.append(node)
        for neighbor in G_rev.neighbors(node):
            if neighbor not in visited:
                dfs_collect_scc(neighbor, current_scc)

    while order_stack:
        """
            Visitando nós e verificando os componentes conexos
        """
        node = order_stack.pop()
        if node not in visited:
            scc = []
            dfs_collect_scc(node, scc)
            sccs.append(scc)

    return sccs


def djisktra_shortest_path(G: nx.Graph | nx.DiGraph, start_node, end_node):
    """Encontra o caminho mais curto entre start_node e end_node usando o algoritmo de Dijkstra."""
    distances = {node: float("inf") for node in G.nodes()}
    parents = {node: None for node in G.nodes()}
    distances[start_node] = 0
    queue = [(0, start_node)]
    while queue:
        distance, node = queue.pop()

        for neighbor in G.neighbors(node):
            weight = get_edge_weight(G, (node, neighbor))
            if weight < 0:
                print(
                    "Erro: O algoritmo de Dijkstra não suporta arestas com peso negativo."
                )
                return None
            new_distance = distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                queue.append((new_distance, neighbor))
                parents[neighbor] = node
        queue.sort(reverse=True)  # Ordena para pegar o menor primeiro
    path = []
    print("Parentes e sua chave", parents, parents.keys())
    for node in list(parents.keys()):
        if node == end_node:
            while node is not None:
                path.append(node)
                node = parents[node]
            path.reverse()
            print(
                f"Caminho mais curto de '{start_node}' para '{end_node}': {' -> '.join(path)}"
            )

    return distances[end_node]


def bellman_ford_shortest_path(G: nx.Graph | nx.DiGraph, start_node, end_node):
    distances = {node: float("inf") for node in G.nodes()}
    parents = {node: None for node in G.nodes()}
    distances[start_node] = 0
    queue = [(0, start_node)]
    for i in range(len(G.nodes()) - 1):
        for u, v in G.edges():
            weight = get_edge_weight(G, (u, v))
            if distances[u] + weight < distances[v]:
                if i == len(G.nodes()) - 2:
                    return [-1]

                distances[v] = distances[u] + weight
                parents[v] = u

    return distances[end_node]
