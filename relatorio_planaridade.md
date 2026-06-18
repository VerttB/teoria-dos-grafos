# Relatório: Teste de Planaridade com Algoritmo de Boyer-Myrvold
O código novo se encontra em `graph_lib/graph_planarity.py`

## 1. O Algoritmo de Boyer-Myrvold
O algoritmo de Boyer-Myrvold é um dos métodos mais eficientes para testar se um grafo é planar. 

A ideia central do algoritmo é tentar construir um "embedding" planar (um arranjo combinatório das arestas em torno de cada vértice) progressivamente. O algoritmo realiza uma busca em profundidade (DFS) para organizar o grafo em uma árvore DFS mais as arestas de retorno (back edges). Em seguida, processa os vértices na ordem reversa da DFS, adicionando as arestas e combinando componentes biconexos do grafo. 

Durante essa adição de arestas, o algoritmo tenta preservar a propriedade planar ao permutar e virar (flip) componentes (blocos) em volta dos vértices de articulação. Se ele conseguir adicionar todas as arestas sem cruzamentos forçados, o grafo é considerado planar e o embedding final é gerado. Caso o algoritmo encontre um bloqueio topológico que impossibilite a inserção de uma aresta sem cruzamento, ele detecta e extrai o subgrafo de Kuratowski causador da não-planaridade (uma subdivisão de $K_5$ ou $K_{3,3}$). 

## 2. Como foi utilizado no projeto
Para implementar este requisito no projeto, foi usado uso da função nativa do NetworkX baseada neste algoritmo: `nx.check_planarity(G,True)`.

- **Teste da Planaridade:**
Quando o grafo é planar a função nos retorna uma tupla `[is_planar, embedding]` => `(True, embedding_planar)`, e se não for, retorna `(False, subgrafo_kuratowski)`.

- **Quando é Planar:**
Com isso podemos pegar o retorno da função retornado na tupla. Extraímos as coordenadas para desenhar o grafo de forma totalmente planar através da função `nx.combinatorial_embedding_to_pos(embedding)` O grafo é então salvo em uma imagem caso seja planar.

- **Quando não é Planar:**
Quando a tupla retorna `False`, capturamos o objeto `Graph` do NetworkX correspondente ao `subgrafo_kuratowski`. Iteramos pelos nós desse objeto gerado para exibir visualmente na tela a lista dos vértices envolvidos que causam o cruzamento e forçam o grafo a ser não planar 