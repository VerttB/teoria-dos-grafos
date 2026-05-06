def has_node_in_edge(edges, node):
    """Verifica se um no esta presente em alguma aresta do grafo."""
    return node in edges


def get_edge_weight(G, edges):
    """Retorna o peso da aresta, se existir."""
    u, v = edges
    if G.has_edge(u, v):
        return G[u][v].get("weight", 1)
    return 1
