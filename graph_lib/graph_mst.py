from networkx import DiGraph, Graph


def kruskal_mst(graph: Graph | DiGraph):
    """Implementação do algoritmo de Kruskal para encontrar a Árvore Geradora Mínima (MST) de um grafo."""
    if graph.is_directed():
        print("Kruskal não é aplicável a dígrafos.")
        return None

    if graph.number_of_nodes() == 0:
        print("Kruskal requer um grafo com vértices.")
        return None

    if graph.number_of_edges() == 0:
        print("Kruskal requer um grafo com arestas.")
        return None

    if not all("weight" in data for _, _, data in graph.edges(data=True)):
        print("Kruskal requer um grafo ponderado.")
        return None

    if not _is_connected(graph):
        print("Kruskal requer um grafo conexo para gerar uma MST.")
        return None

    sorted_edges = sorted(list(graph.edges(data=True)), key=lambda x: x[2]["weight"])
    groups = {}
    path = []
    for node in graph.nodes():
        groups[node] = node

    for edge in sorted_edges:
        node1, node2, _ = edge
        if _check_cycle(groups, node1, node2):
            print(f"Pulando aresta '{node1} - {node2}' para evitar ciclo.")
            continue

        path.append(edge)
        _union(groups, node1, node2)

        if len(path) == graph.number_of_nodes() - 1:
            break

    _gen_graph_image(graph, path)
    return path


def _find(groups, node):
    """Função auxiliar para encontrar o grupo de um nó."""
    if groups[node] != node:
        groups[node] = _find(groups, groups[node])
    return groups[node]


def _union(groups, node1, node2):
    """Função auxiliar para unir dois grupos."""
    root1 = _find(groups, node1)
    root2 = _find(groups, node2)
    if root1 != root2:
        groups[root2] = root1


def _check_cycle(groups, node1, node2):
    """Função auxiliar para verificar se a adição de uma aresta criaria um ciclo."""
    return _find(groups, node1) == _find(groups, node2)


def _is_connected(graph):
    """Função auxiliar para verificar se todos os vértices estão conectados."""
    visited = set()
    stack = [next(iter(graph.nodes()))]

    while stack:
        node = stack.pop()
        if node in visited:
            continue

        visited.add(node)
        stack.extend(
            neighbor for neighbor in graph.neighbors(node) if neighbor not in visited
        )

    return len(visited) == graph.number_of_nodes()


def _gen_graph_image(graph, mst_path):
    """Função auxiliar para gerar uma imagem do grafo."""
    import matplotlib.pyplot as plt
    import networkx as nx

    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="black",
        node_size=1000,
        font_size=12,
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=[(u, v) for u, v, _ in mst_path],
        width=2.5,
        edge_color="blue",
    )
    plt.savefig("mst_visualization.png")
    plt.close()
