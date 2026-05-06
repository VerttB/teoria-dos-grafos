import types as _types

from . import graph_adjacency as _graph_adjacency
from . import graph_components as _graph_components
from . import graph_edges as _graph_edges
from . import graph_matrix as _graph_matrix
from . import graph_traversal as _graph_traversal
from . import graph_validation as _graph_validation
from . import shortest_path as _shortest_path


graph_tools = _types.SimpleNamespace(
    graph_to_adjacency_matrix=_graph_matrix.graph_to_adjacency_matrix,
    graph_to_incidence_matrix=_graph_matrix.graph_to_incidence_matrix,
    graph_to_adjacent_list=_graph_adjacency.graph_to_adjacent_list,
    has_node_in_edge=_graph_edges.has_node_in_edge,
    get_edge_weight=_graph_edges.get_edge_weight,
    graph_dfs=_graph_traversal.graph_dfs,
    graph_dfs_rec=_graph_traversal._graph_dfs_rec,
    print_matrix=_graph_matrix.print_matrix,
    check_sequence=_graph_validation.check_sequence,
    get_dfs_order=_graph_traversal.get_dfs_order,
    find_sccs_kosaraju=_graph_components.find_sccs_kosaraju,
    djisktra_shortest_path=_shortest_path.djisktra_shortest_path,
    bellman_ford_shortest_path=_shortest_path.bellman_ford_shortest_path,
    build_path=_shortest_path.build_path,
)

__all__ = ["graph_tools"]
