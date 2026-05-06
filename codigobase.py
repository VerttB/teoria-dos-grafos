from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import networkx as nx

import lib


ENTRADAS_DIR = Path(__file__).resolve().parent / "entradas"


def listar_arquivos_entrada(pasta=ENTRADAS_DIR):
    """Retorna os arquivos .txt disponiveis na pasta de entradas."""
    if not pasta.exists():
        return []

    return sorted(
        [
            arquivo
            for arquivo in pasta.iterdir()
            if arquivo.is_file() and arquivo.suffix.lower() == ".txt"
        ],
        key=lambda arquivo: arquivo.name.lower(),
    )


def selecionar_arquivo_entrada():
    """Mostra os arquivos de entrada e permite escolher por numero ou nome."""
    arquivos = listar_arquivos_entrada()

    if not arquivos:
        print(f"Nenhum arquivo .txt encontrado em '{ENTRADAS_DIR}'.")
        return None

    print("\nArquivos de entrada disponiveis:")
    for indice, arquivo in enumerate(arquivos, start=1):
        print(f"{indice}. {arquivo.name}")

    while True:
        escolha = input("\nEscolha o arquivo pelo numero ou nome: ").strip()

        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(arquivos):
                return arquivos[indice - 1]

        for arquivo in arquivos:
            if escolha.lower() == arquivo.name.lower():
                return arquivo

        print("Opcao invalida. Tente novamente.")


def ler_grafo_arquivo(nome_arquivo):
    """
    Le um arquivo de texto e cria um grafo/digrafo.

    Formato esperado:
    1a linha: [G|D] [N|W]
        G = Grafo nao direcionado
        D = Digrafo
        N = Nao ponderado
        W = Ponderado
    Demais linhas:
        Se nao ponderado: u v
        Se ponderado:     u v w
    """
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

        if not linhas:
            print("Arquivo vazio!")
            return None, False

        tipo, peso = linhas[0].split()
        if tipo == "G":
            G = nx.Graph()
        elif tipo == "D":
            G = nx.DiGraph()
        else:
            raise ValueError("Primeiro caractere deve ser 'G' ou 'D'.")

        if peso not in {"N", "W"}:
            raise ValueError("Segundo caractere deve ser 'N' ou 'W'.")

        ponderado = peso == "W"

        for linha in linhas[1:]:
            partes = linha.split()
            if ponderado:
                if len(partes) != 3:
                    raise ValueError("Esperado formato 'u v w' para grafos ponderados.")
                u, v, w = partes
                adicionar_aresta(G, u, v, w, ponderado)
            else:
                if len(partes) != 2:
                    raise ValueError(
                        "Esperado formato 'u v' para grafos nao ponderados."
                    )
                u, v = partes
                adicionar_aresta(G, u, v)

        print(
            f"Grafo criado ({'digrafo' if tipo == 'D' else 'grafo'}, "
            f"{'ponderado' if ponderado else 'nao ponderado'}) com "
            f"{G.number_of_nodes()} vertices e {G.number_of_edges()} arestas. \n"
            f"Vértices: {list(G.nodes())}"
        )
        return G, ponderado

    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' nao encontrado.")
        return None, False
    except ValueError as erro:
        print(f"Erro no arquivo '{nome_arquivo}': {erro}")
        return None, False


def adicionar_vertice(G, v):
    """Adiciona um vertice ao grafo, se nao existir."""
    if v not in G:
        G.add_node(v)
        print(f"Vertice '{v}' adicionado.")
    else:
        print(f"Vertice '{v}' ja existe.")


def adicionar_aresta(G, u, v, w=1, ponderado=False):
    """Adiciona uma aresta ao grafo."""
    if ponderado:
        G.add_edge(u, v, weight=float(w))
        print(f"Aresta '{u} - {v}' com peso {w} adicionada.")
    else:
        G.add_edge(u, v)
        print(f"Aresta '{u} - {v}' adicionada.")


def visualizar_grafo(G, ponderado=False):
    """Desenha o grafo em um arquivo PNG."""
    pos = nx.spring_layout(G)
    desenho = {
        "with_labels": True,
        "node_color": "lightblue",
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

    plt.savefig("visualizacao_grafo.png")
    plt.close()


if __name__ == "__main__":
    path = selecionar_arquivo_entrada()
    if path is None:
        exit(1)

    print(f"\nArquivo lido: {path.name}")
    G, ponderado = ler_grafo_arquivo(path)

    if G is None:
        print("Nenhum grafo carregado. Encerrando.")
        exit(1)

    visualizar_grafo(G, ponderado)

    start = input("Qual o vertice de origem? ").strip().upper()
    end = input("Qual o vertice de destino? ").strip().upper()

    dijkstra = lib.djisktra_shortest_path(G, start, end)
    print(f"Caminho mais curto de {start} para {end}: {dijkstra}")

    bellman_ford = lib.bellman_ford_shortest_path(G, start, end)
    print(f"Caminho mais curto de {start} para {end}: {bellman_ford}")
