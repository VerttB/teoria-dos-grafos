import networkx as nx


def check_sequence(G: nx.Graph | nx.DiGraph, S: list):
    """Verifica propriedades de uma sequencia de vertices no grafo."""
    if not S:
        print("Sequencia vazia.")
        return

    for v in S:
        if v not in G:
            print(f"Erro: O vertice '{v}' nao existe no grafo.")
            return

    is_walk = True
    seen_edges = []
    is_directed = isinstance(G, nx.DiGraph)

    for i in range(len(S) - 1):
        u, v = S[i], S[i + 1]
        if not G.has_edge(u, v):
            is_walk = False
            break
        if is_directed:
            edge = (u, v)
        else:
            edge = tuple(sorted((u, v)))
        seen_edges.append(edge)

    if not is_walk:
        print(f"A sequencia {S}:")
        print(
            "- Nao e um passeio valido: sequencia de vertices nao esta "
            "presente em todas as arestas."
        )
        return

    is_path = len(set(S)) == len(S)
    is_trail = len(set(seen_edges)) == len(seen_edges)
    is_circuit = is_trail and S[0] == S[-1] and len(S) > 1

    print(f"A sequencia {S}:")
    print("- E um passeio valido: Sim")
    print(f"- E um caminho (sem repeticao de vertices): {'Sim' if is_path else 'Nao'}")
    print(f"- E uma trilha (sem repeticao de arestas): {'Sim' if is_trail else 'Nao'}")
    print(f"- E um circuito (trilha fechada): {'Sim' if is_circuit else 'Nao'}")
