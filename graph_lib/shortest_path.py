import networkx as nx

from .graph_edges import get_edge_weight


def djisktra_shortest_path(G: nx.Graph | nx.DiGraph, start_node, end_node):
    """Encontra o caminho mais curto entre start_node e end_node com Dijkstra."""
    print("Running Dijkstra's algorithm...")
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
                    "Erro: O algoritmo de Dijkstra nao suporta arestas com "
                    "peso negativo."
                )
                return None
            new_distance = distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                queue.append((new_distance, neighbor))
                parents[neighbor] = node
        queue.sort(reverse=True)

    if parents[end_node] is None and end_node != start_node:
        print(f"Erro: O no '{end_node}' nao e alcancavel a partir de '{start_node}'.")
        return None

    path = build_path(parents, end_node)
    print(
        f"Caminho mais curto de '{start_node}' para '{end_node}': {' -> '.join(path)}"
    )
    return distances[end_node]


def bellman_ford_shortest_path(G: nx.Graph | nx.DiGraph, start_node, end_node):
    """Encontra o caminho mais curto entre start_node e end_node com Bellman-Ford."""
    print("Running Bellman-Ford algorithm...")
    distances = {node: float("inf") for node in G.nodes()}
    parents = {node: None for node in G.nodes()}
    distances[start_node] = 0

    for i in range(len(G.nodes()) - 1):
        for u, v in G.edges():
            weight = get_edge_weight(G, (u, v))
            if distances[u] + weight < distances[v]:
                if i == len(G.nodes()) - 2:
                    return [-1]

                distances[v] = distances[u] + weight
                parents[v] = u

    if parents[end_node] is None and end_node != start_node:
        print(f"Erro: O no '{end_node}' nao e alcancavel a partir de '{start_node}'.")
        return None

    build_path(parents, end_node)

    return distances[end_node]


def build_path(parents, end_node):
    path = []
    while end_node is not None:
        path.append(end_node)
        end_node = parents[end_node]
    path.reverse()
    return path
