import networkx as nx


def test_planarity(G):
    """
    Testa a planaridade de um grafo G utilizando o algoritmo de Boyer-Myrvold
    Retorna uma tupla (is_planar, result):
      - Se is_planar for True, result é o PlanarEmbedding.
      - Se is_planar for False, result é o subgrafo de Kuratowski.
    """
    # Converter para grafo não direcionado se for direcionado,
    # pois a planaridade depende da estrutura de conexões.
    if isinstance(G, nx.DiGraph):
        G_test = nx.Graph(G)
    else:
        G_test = G

    is_planar, result = nx.check_planarity(G_test, True)

    return is_planar, result


def get_planar_positions(embedding):
    """
    Converte o embedding planar em posições para desenhar o grafo em visualização.
    """
    return nx.combinatorial_embedding_to_pos(embedding)


def extract_kuratowski(result):
    """
    Extrai manualmente os vértices e arestas do subgrafo de Kuratowski.
    O parâmetro kuratowski_graph é um objeto nx.Graph
    retornado pelo check_planarity quando o grafo não é planar.
    """

    if isinstance(result, nx.Graph):
        vertices = list(result.nodes())
        edges = list(result.edges())
        return vertices, edges

    try:
        data = result.get_data()
    except AttributeError:
        data = dict(result)

    vertices = set()
    edges = []

    for u in data:
        for v in data[u]:
            edges.append((u, v))
            vertices.add(u)
            vertices.add(v)

    return list(vertices), edges
