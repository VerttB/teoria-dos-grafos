from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx
from graph_lib import graph_tools as lib





def visualizar_grafo_planar(G, pos, ponderado=False):
    """Desenha o grafo em um arquivo PNG utilizando posições do embedding planar."""
    desenho = {
        "with_labels": True,
        "node_color": "lightgreen",
        "edge_color": "black",
        "node_size": 1000,
        "font_size": 12,
        "arrows": isinstance(G, nx.DiGraph),
    }

    if isinstance(G, nx.DiGraph):
        desenho["arrowsize"] = 20

    nx.draw(G, pos, **desenho)

    if ponderado:
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.savefig("visualizacao_grafo_planar.png")
    plt.close()
    print(
        "Imagem gerada com embedding planar salva como 'visualizacao_grafo_planar.png'."
    )


if __name__ == "__main__":
    path = lib.selecionar_arquivo_entrada()
    if path is None:
        exit(1)

    print(f"\nArquivo lido: {path.name}")
    G, ponderado = lib.ler_grafo_arquivo(path)

    if G is None:
        print("Nenhum grafo carregado. Encerrando.")
        exit(1)

    is_planar, result = lib.test_planarity(G)

    if is_planar:
        print("\nResultado: O grafo é planar.")
        print("Resultado da planaridade", result)
        pos = lib.get_planar_positions(result)
        visualizar_grafo_planar(G, pos, ponderado)
    else:
        print("\nResultado: O grafo NÃO é planar.")
        vertices, edges = lib.extract_kuratowski(result)
        print(
            f"Subgrafo de Kuratowski encontrado: Vértices {vertices}, Arestas {edges}"
        )
