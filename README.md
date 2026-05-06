# Menor caminho em grafos

Projeto da disciplina de Teoria dos Grafos para leitura de grafos a partir de arquivos texto. O grafo e representado com a biblioteca `NetworkX`, mas boa parte de seus algorimos foram implementados manualmente

## Funcionalidades

- Leitura de grafos e digrafos a partir de arquivos `.txt`.
- Suporte a grafos ponderados e nao ponderados.
- Selecao interativa do arquivo de entrada.
- Solicitacao de vertice de origem e destino pelo terminal.
- Execucao de Dijkstra para grafos sem pesos negativos.
- Execucao de Bellman-Ford com suporte a pesos negativos.
- Deteccao de ciclos negativos no Bellman-Ford.
- Aviso quando nao existe caminho entre origem e destino.
- Geracao da imagem `visualizacao_grafo.png`.

## Formato dos arquivos

Os arquivos de entrada ficam na pasta `entradas/`.

A primeira linha define o tipo do grafo:

```txt
[G|D] [N|W]
```

Onde:

- `G`: grafo nao direcionado
- `D`: digrafo
- `N`: nao ponderado
- `W`: ponderado

Para grafos nao ponderados:

```txt
D N
A B
A C
B D
```

Para grafos ponderados:

```txt
D W
A B 4
A C 2
B D 5
```

## Exemplos disponiveis

A pasta `entradas/` contem exemplos para diferentes situacoes:

| Arquivo | Tipo | Descricao |
| --- | --- | --- |
| `digrafo_ponderado.txt` | `D W` | Digrafo ponderado sem pesos negativos |
| `digrafo_ponderado_negativo.txt` | `D W` | Digrafo com peso negativo para Bellman-Ford |
| `digrafo_ciclo_negativo.txt` | `D W` | Digrafo com ciclo negativo |
| `digrafo_nao_ponderado.txt` | `D N` | Digrafo nao ponderado |
| `grafo_ponderado.txt` | `G W` | Grafo nao direcionado ponderado |
| `grafo_nao_ponderado.txt` | `G N` | Grafo nao direcionado nao ponderado |
| `grafo_desconexo.txt` | `G W` | Grafo com componentes desconexos |
| `grafo-WD.txt` | `D W` | Exemplo adicional de digrafo ponderado |

## Como executar

Instale as dependencias:

```bash
pip install networkx matplotlib
```

Execute o programa:

```bash
python main.py
```

O programa mostra uma lista com os arquivos disponiveis:

```txt
Arquivos de entrada disponiveis:
1. digrafo_ciclo_negativo.txt
2. digrafo_nao_ponderado.txt
3. digrafo_ponderado.txt
...

Escolha o arquivo pelo numero ou nome:
```

Depois, informe os vertices:

```txt
Qual o vertice de origem? A
Qual o vertice de destino? F
```

## Exemplo com Dijkstra

Entrada sugerida:

```txt
digrafo_ponderado.txt
```

Origem e destino:

```txt
A
F
```

Saida esperada:

```txt
Running Dijkstra's algorithm...
Caminho mais curto de 'A' para 'F': A -> B -> D -> E -> F
Caminho mais curto de A para F: 14.0
```

## Exemplo com Bellman-Ford

Entrada sugerida:

```txt
digrafo_ponderado_negativo.txt
```

Origem e destino:

```txt
A
E
```

Saida esperada:

```txt
Running Bellman-Ford algorithm...
Caminho mais curto de 'A' para 'E': A -> B -> C -> D -> E
Caminho mais curto de A para E: 7.0
```

## Estrutura do projeto

```txt
.
|-- main.py
|-- entradas/
|   |-- digrafo_ponderado.txt
|   |-- digrafo_ponderado_negativo.txt
|   |-- digrafo_ciclo_negativo.txt
|   `-- ...
|-- graph_lib/
|   |-- api.py
|   |-- shortest_path.py
|   |-- graph_matrix.py
|   |-- graph_adjacency.py
|   |-- graph_edges.py
|   |-- graph_traversal.py
|   |-- graph_validation.py
|   `-- graph_components.py
`-- README.md
```
