import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import matplotlib

matplotlib.use("Agg")
import networkx as nx
from graph_lib import graph_tools as lib


def main():
    print("=" * 60)
    print("  RESOLUÇÃO DE PROBLEMAS EM GRAFOS POR HEURÍSTICA GULOSA")
    print("=" * 60)

    caminho_arquivo = lib.selecionar_arquivo_entrada()
    if caminho_arquivo is None or not caminho_arquivo.exists():
        print("Arquivo inválido. Encerrando o programa.")
        return

    G, _ = lib.ler_grafo_arquivo(caminho_arquivo)
    if G is None or G.number_of_nodes() == 0:
        print("Erro ao carregar o grafo. Encerrando.")
        return

    prefixo = (
        input("\nDigite o prefixo para os arquivos de imagem de saída: ")
        .strip()
        .replace(" ", "_")
    )
    if not prefixo:
        prefixo = "resultado"

    conjunto_estavel = lib.heuristica_conjunto_estavel(G)
    cobertura_vertices = lib.calcular_cobertura_vertices(G, conjunto_estavel)
    clique_maximal = lib.calcular_clique(G)

    print("\n" + "-" * 50)
    print("RESULTADOS ENCONTRADOS:")
    print("-" * 50)
    print(
        f"1. Conjunto Estável Maximal (Tamanho {len(conjunto_estavel)}):"
        f"\n   Vértices: {sorted(list(conjunto_estavel))}"
    )
    print(
        f"2. Cobertura de Vértices (Tamanho {len(cobertura_vertices)}):"
        f"\n   Vértices: {sorted(list(cobertura_vertices))}"
    )
    print(
        f"3. Clique Maximal (Tamanho {len(clique_maximal)}):"
        f"\n   Vértices: {sorted(list(clique_maximal))}"
    )
    print("-" * 50)

    print("\nGerando visualizações gráficas...")
    pos = nx.spring_layout(G, seed=42)

    caminho_estavel = f"{prefixo}_conjunto_estavel.png"
    caminho_cobertura = f"{prefixo}_cobertura.png"
    caminho_clique = f"{prefixo}_clique.png"

    lib.desenhar_e_salvar_solucao(
        G, pos, conjunto_estavel, "conjunto_estavel", caminho_estavel
    )
    lib.desenhar_e_salvar_solucao(
        G, pos, cobertura_vertices, "cobertura", caminho_cobertura
    )
    lib.desenhar_e_salvar_solucao(G, pos, clique_maximal, "clique", caminho_clique)

    print("\nProcesso finalizado com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()
