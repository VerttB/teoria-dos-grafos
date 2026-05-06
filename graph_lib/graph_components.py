import networkx as nx

from .graph_traversal import get_dfs_order


def find_sccs_kosaraju(G: nx.DiGraph):
    """Identifica componentes fortemente conexos usando Kosaraju-Sharir."""
    order_stack = get_dfs_order(G)
    G_rev = G.reverse(copy=True)

    visited = set()
    sccs = []

    def dfs_collect_scc(node, current_scc):
        visited.add(node)
        current_scc.append(node)
        for neighbor in G_rev.neighbors(node):
            if neighbor not in visited:
                dfs_collect_scc(neighbor, current_scc)

    while order_stack:
        node = order_stack.pop()
        if node not in visited:
            scc = []
            dfs_collect_scc(node, scc)
            sccs.append(scc)

    return sccs
