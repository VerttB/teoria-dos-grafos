import networkx as nx

from .graph_edges import get_edge_weight


def _vertices_are_valid(G, start_node, end_node):
    if start_node not in G:
        print(f"Erro: O no '{start_node}' nao existe no grafo.")
        return False

    if end_node not in G:
        print(f"Erro: O no '{end_node}' nao existe no grafo.")
        return False

    return True


def _relaxable_edges(G):
    for u, v in G.edges():
        yield u, v
        if not isinstance(G, nx.DiGraph):
            yield v, u


def _has_negative_weight(G):
    for u, v in G.edges():
        if get_edge_weight(G, (u, v)) < 0:
            return True
    return False


def djisktra_shortest_path(G: nx.Graph | nx.DiGraph, start_node, end_node):
    """Encontra o caminho mais curto entre start_node e end_node com Dijkstra."""
    print("Running Dijkstra's algorithm...")
    if not _vertices_are_valid(G, start_node, end_node):
        return None

    if _has_negative_weight(G):
        print(
            "Erro: O algoritmo de Dijkstra nao suporta arestas com "
            "peso negativo."
        )
        return None

    distances = {node: float("inf") for node in G.nodes()}
    parents = {node: None for node in G.nodes()}
    distances[start_node] = 0
    queue = [(0, start_node)]

    while queue:
        distance, node = queue.pop()

        for neighbor in G.neighbors(node):
            weight = get_edge_weight(G, (node, neighbor))
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
    if not _vertices_are_valid(G, start_node, end_node):
        return None

    distances = {node: float("inf") for node in G.nodes()}
    parents = {node: None for node in G.nodes()}
    distances[start_node] = 0
    edges = list(_relaxable_edges(G))

    for _ in range(len(G.nodes()) - 1):
        changed = False
        for u, v in edges:
            weight = get_edge_weight(G, (u, v))
            if distances[u] != float("inf") and distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                parents[v] = u
                changed = True

        if not changed:
            break

    for u, v in edges:
        weight = get_edge_weight(G, (u, v))
        if distances[u] != float("inf") and distances[u] + weight < distances[v]:
            print("Negative weight cycle detected.")
            return None

    if parents[end_node] is None and end_node != start_node:
        print(f"Erro: O no '{end_node}' nao e alcancavel a partir de '{start_node}'.")
        return None

    build_path(parents, end_node)
    print(
        f"Caminho mais curto de '{start_node}' para '{end_node}': {' -> '.join(build_path(parents, end_node))}"
    )
    return distances[end_node]


def build_path(parents, end_node):
    path = []
    while end_node is not None:
        path.append(end_node)
        end_node = parents[end_node]
    path.reverse()
    return path
