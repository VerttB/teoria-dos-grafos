import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from graph_lib import graph_tools as lib
import networkx as nx


def formatar_num(val):
    if val == float("inf") or val == float("-inf"):
        return "Inf"
    if isinstance(val, (int, float)) and float(val).is_integer():
        return str(int(val))
    return f"{val:.2f}"


def main():
    print("=" * 65)
    print("   FLUXO MÁXIMO EM REDES - ALGORITMO DE FORD-FULKERSON")
    print("=" * 65)

    caminho_arquivo = lib.selecionar_arquivo_entrada()
    if caminho_arquivo is None or not caminho_arquivo.exists():
        print("Arquivo inválido. Encerrando o programa.")
        return

    ler_retorno = lib.ler_grafo_arquivo(caminho_arquivo)
    if ler_retorno is None or ler_retorno[0] is None:
        print("Erro ao carregar o grafo. Encerrando.")
        return

    G, _ = ler_retorno

    if not isinstance(G, nx.DiGraph):
        print("Erro: O arquivo deve representar um dígrafo (cabeçalho 'D W').")
        return

    prefixo_imagem = input(
        "\nDigite o nome da imagem de saída (ex: fluxo_maximo.png): "
    ).strip()
    if not prefixo_imagem:
        prefixo_imagem = "fluxo_maximo.png"
    elif not prefixo_imagem.endswith(".png"):
        prefixo_imagem += ".png"

    try:
        (
            fluxo_maximo,
            historico_caminhos,
            tabela_fluxos,
            G_ext,
            s,
            t,
            fontes,
            sorvedouros,
        ) = lib.executar_ford_fulkerson(G)
    except Exception as e:
        print(f"Erro ao executar o Algoritmo de Ford-Fulkerson: {e}")
        return

    print("\n" + "-" * 60)
    print("ESTRUTURA DA REDE DE FLUXO:")
    print("-" * 60)
    print(f"Fontes Originais (In-degree = 0): {fontes}")
    print(f"Sorvedouros Originais (Out-degree = 0): {sorvedouros}")
    print(f"Super-Fonte Criada: '{s}'")
    print(f"Super-Sorvedouro Criado: '{t}'")

    print("\n" + "-" * 60)
    print("CAMINHOS AUMENTANTES IDENTIFICADOS (POR ITERAÇÃO):")
    print("-" * 60)
    if not historico_caminhos:
        print("Nenhum caminho aumentante foi encontrado.")
    else:
        for item in historico_caminhos:
            str_caminho = " -> ".join(item["caminho"])
            gargalo = item["gargalo"]
            print(
                f"Iteração {item['iteracao']:02d}: {str_caminho} | Gargalo (Capacidade Aumentada): {formatar_num(gargalo)}"
            )

    print("\n" + "-" * 60)
    print("TABELA FINAL DE FLUXOS POR ARESTA:")
    print("-" * 60)
    print(f"{'Origem':<15} {'Destino':<15} {'Fluxo Atual':<15} {'Capacidade':<15}")
    print("-" * 60)
    for row in tabela_fluxos:
        u = row["origem"]
        v = row["destino"]
        f = row["fluxo"]
        c = row["capacidade"]
        print(f"{u:<15} {v:<15} {formatar_num(f):<15} {formatar_num(c):<15}")

    print("-" * 60)
    print(f"FLUXO MÁXIMO TOTAL CALCULADO: {formatar_num(fluxo_maximo)}")
    print("-" * 60)

    # 6. Gerar e salvar a visualização gráfica
    print("\nGerando visualização gráfica da rede...")
    try:
        lib.desenhar_e_salvar_fluxo_maximo(
            G_ext,
            tabela_fluxos,
            s,
            t,
            fontes,
            sorvedouros,
            fluxo_maximo,
            prefixo_imagem,
        )
        print("Processo finalizado com sucesso!")
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Erro ao gerar a visualização: {repr(e)}")

    print("=" * 65)


if __name__ == "__main__":
    main()
