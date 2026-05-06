import networkx as nx


def _graph_dfs_rec(
    G: nx.Graph | nx.DiGraph,
    start_node,
    destination_node,
    max_depth: int,
    depth: int,
    possible_paths: list,
    path: list = None,
):
    """Funcao recursiva para encontrar caminhos sem repeticao de vertices."""
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
    Encontra e exibe todos os caminhos de u ate v com comprimento <= k.
    Retorna o numero total de caminhos simples encontrados.
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
        f"\nCaminhos encontrados de '{start_node}' ate '{destination_node}' "
        f"com comprimento maximo {max_depth}):"
    )
    for i, p in enumerate(possible_paths, 1):
        print(f"Caminho {i}: {' -> '.join(p)} (comprimento: {len(p) - 1})")

    if not possible_paths:
        print("Nenhum caminho encontrado.")

    return len(possible_paths)


def get_dfs_order(G: nx.DiGraph):
    """Executa uma DFS e retorna os nos em ordem de finalizacao."""
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)

    for node in G.nodes():
        if node not in visited:
            dfs(node)

    return stack
