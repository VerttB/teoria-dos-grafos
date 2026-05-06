import networkx as nx

from .graph_edges import get_edge_weight


def graph_to_adjacency_matrix(G: nx.Graph | nx.DiGraph):
    """Converte um grafo para sua matriz de adjacencia."""
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
    """Converte um grafo para sua matriz de incidencia."""
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


def print_matrix(matrix):
    """Imprime uma matriz de forma legivel."""
    if isinstance(matrix, dict):
        for key, value in matrix.items():
            print(f"{key}: {value}")
        return

    for row in matrix:
        print("|", end="")
        for column in row:
            print(column, end="\t")

        print("|")
