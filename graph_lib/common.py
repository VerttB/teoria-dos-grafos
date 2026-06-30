import networkx as nx
from pathlib import Path

ENTRADAS_DIR = Path(__file__).resolve().parent.parent / "entradas"


def listar_arquivos_entrada(pasta=ENTRADAS_DIR):
    """Retorna os arquivos .txt disponíveis na pasta de entradas."""
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


def selecionar_arquivo_entrada(pasta=ENTRADAS_DIR):
    """Mostra os arquivos de entrada e permite escolher por número ou nome."""
    arquivos = listar_arquivos_entrada(pasta)

    if not arquivos:
        print(f"Nenhum arquivo .txt encontrado em '{pasta}'.")
        caminho = input("Digite o caminho do arquivo de entrada: ").strip()
        return Path(caminho)

    print("\nArquivos de entrada disponíveis:")
    for indice, arquivo in enumerate(arquivos, start=1):
        print(f"{indice}. {arquivo.name}")

    while True:
        escolha = input(
            "\nEscolha o arquivo pelo número ou nome (ou digite o caminho de outro arquivo): "
        ).strip()
        if not escolha:
            continue

        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(arquivos):
                return arquivos[indice - 1]

        for arquivo in arquivos:
            if escolha.lower() == arquivo.name.lower():
                return arquivo

        caminho = Path(escolha)
        if caminho.exists():
            return caminho

        print("Opção ou caminho inválido. Tente novamente.")


def ler_grafo_arquivo(nome_arquivo):
    """
    Lê um arquivo de texto e cria um grafo/digrafo.
    Suporta arquivos com cabeçalho (ex: 'G N', 'G W') ou sem cabeçalho (ex: direto com 'u v w').
    """
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            linhas = [
                linha.strip()
                for linha in arquivo
                if linha.strip() and not linha.strip().startswith("#")
            ]

        if not linhas:
            print("Arquivo vazio!")
            return None, False

        # Verificar se a primeira linha é cabeçalho
        partes_cabecalho = linhas[0].split()
        tem_cabecalho = False
        if len(partes_cabecalho) == 2:
            tipo_grafo, peso_grafo = partes_cabecalho
            if tipo_grafo in {"G", "D"} and peso_grafo in {"N", "W"}:
                tem_cabecalho = True

        if tem_cabecalho:
            tipo, peso = partes_cabecalho
            if tipo == "G":
                G = nx.Graph()
            elif tipo == "D":
                G = nx.DiGraph()
            else:
                raise ValueError("Primeiro caractere deve ser 'G' ou 'D'.")

            if peso not in {"N", "W"}:
                raise ValueError("Segundo caractere deve ser 'N' ou 'W'.")

            ponderado = peso == "W"
            linhas_arestas = linhas[1:]
        else:
            G = nx.Graph()
            ponderado = len(partes_cabecalho) >= 3
            linhas_arestas = linhas

        for num_linha, linha in enumerate(
            linhas_arestas, start=1 if not tem_cabecalho else 2
        ):
            partes = linha.split()
            if not partes:
                continue
            if ponderado:
                if len(partes) < 3:
                    print(
                        f"Aviso: Linha {num_linha} ignorada devido ao formato inválido (esperado 'u v w'): '{linha}'"
                    )
                    continue
                u, v, w_str = partes[0], partes[1], partes[2]
                try:
                    w = float(w_str)
                    if w.is_integer():
                        w = int(w)
                except ValueError:
                    print(
                        f"Erro: Peso inválido na linha {num_linha}: '{w_str}'. Usando peso 1.0."
                    )
                    w = 1.0
                adicionar_aresta(G, u, v, w, ponderado)
            else:
                if len(partes) < 2:
                    print(
                        f"Aviso: Linha {num_linha} ignorada devido ao formato inválido (esperado 'u v'): '{linha}'"
                    )
                    continue
                u, v = partes[0], partes[1]
                adicionar_aresta(G, u, v)

        print(
            f"Grafo criado ({'digrafo' if isinstance(G, nx.DiGraph) else 'grafo'}, "
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
