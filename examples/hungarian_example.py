import sys
from pathlib import Path

# Adiciona o diretório pai ao sys.path para permitir importar graph_lib
sys.path.append(str(Path(__file__).resolve().parent.parent))

from graph_lib import graph_tools as lib
import networkx as nx


def main():
    print("=" * 60)
    print("  EMPARELHAMENTO ÓTIMO EM GRAFOS BIPARTIDOS (ALGORITMO HÚNGARO)")
    print("=" * 60)

    caminho_arquivo = lib.selecionar_arquivo_entrada()
    if caminho_arquivo is None or not caminho_arquivo.exists():
        print("Arquivo inválido. Encerrando o programa.")
        return

    ler_retorno = lib.ler_grafo_arquivo(caminho_arquivo)
    if ler_retorno is None or ler_retorno[0] is None:
        print("Erro ao carregar o grafo. Encerrando.")
        return

    G, _ = ler_retorno

    if not nx.is_bipartite(G):
        print(
            "Erro: O grafo carregado não é bipartido! O Algoritmo Húngaro exige um grafo bipartido."
        )
        return

    imagem_saida = input(
        "\nDigite o nome do arquivo de imagem de saída (ex: emparelhamento.png): "
    ).strip()
    if not imagem_saida:
        imagem_saida = "emparelhamento.png"
    elif not imagem_saida.endswith(".png"):
        imagem_saida += ".png"

    try:
        matching, custo_total, A, B = lib.resolver_emparelhamento_hungaro(G)
    except Exception as e:
        print(f"Erro ao executar o Algoritmo Húngaro: {e}")
        return

    print("\n" + "-" * 50)
    print("RESULTADO DO EMPARELHAMENTO ÓTIMO:")
    print("-" * 50)
    print(f"Partição A (Esquerda): {A}")
    print(f"Partição B (Direita): {B}")
    print("Arestas selecionadas para o emparelhamento:")
    for u, v in sorted(matching):
        peso = G[u][v].get("weight", 1)
        print(f"  {u} <-> {v} (Peso: {peso})")
    print(f"Custo Total da Solução: {custo_total}")
    print("-" * 50)

    print("\nGerando visualização gráfica...")
    try:
        lib.desenhar_e_salvar_emparelhamento(
            G, matching, A, B, custo_total, imagem_saida
        )
        print("Visualização gerada com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar visualização: {e}")

    print("=" * 60)


if __name__ == "__main__":
    main()
