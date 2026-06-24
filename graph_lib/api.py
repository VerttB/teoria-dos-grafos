import types as _types

from . import graph_adjacency as _graph_adjacency
from . import graph_components as _graph_components
from . import graph_edges as _graph_edges
from . import graph_matrix as _graph_matrix
from . import graph_traversal as _graph_traversal
from . import graph_validation as _graph_validation
from . import shortest_path as _shortest_path
from . import graph_mst as _graph_mst
from . import graph_planarity as _graph_planarity
from . import graph_heuristics as _graph_heuristics
from . import common as _common

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
    kruskal_mst=_graph_mst.kruskal_mst,
    test_planarity=_graph_planarity.test_planarity,
    get_planar_positions=_graph_planarity.get_planar_positions,
    extract_kuratowski=_graph_planarity.extract_kuratowski,
    heuristica_conjunto_estavel=_graph_heuristics.heuristica_conjunto_estavel,
    calcular_cobertura_vertices=_graph_heuristics.calcular_cobertura_vertices,
    calcular_clique=_graph_heuristics.calcular_clique,
    desenhar_e_salvar_solucao=_graph_heuristics.desenhar_e_salvar_solucao,
    selecionar_arquivo_entrada=_common.selecionar_arquivo_entrada,
    ler_grafo_arquivo=_common.ler_grafo_arquivo,
    adicionar_vertice=_common.adicionar_vertice,
    adicionar_aresta=_common.adicionar_aresta,
)

__all__ = ["graph_tools"]
