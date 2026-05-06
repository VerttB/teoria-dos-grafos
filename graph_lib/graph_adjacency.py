import networkx as nx


def graph_to_adjacent_list(G: nx.Graph | nx.DiGraph):
    """Converte um grafo para sua lista de adjacencias."""
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
