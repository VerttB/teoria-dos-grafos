# Comparação de uso de memória em grafos

###
V = vértice
E = arestas
## O(V²) — Matriz de adjacência
<ul>
<li>Usa uma matriz V×V.
<li>Acesso O(1) para checar arestas.
<li>consome muita memória.
<li>Melhor usado grafos densos (muitas arestas, E ≈ V²).
</ul>

## O(V·E) — Matriz de incidência 
<ul> 
<li>Estrutura V×E (nós × arestas).
<li>útil em contextos matemáticos específicos.
<li>Extremamente ineficiente em memória.
<lI>Raramente usada na forma densa prefirível na versão esparsa.
</ul>

## O(V + E) — Lista de adjacência

<ul>

<li>Armazena vizinhos de cada vértice.</li>
<li>Muito mais econômica.
<li>Checar aresta pode ser mais lento que O(1).
<li>Melhor usado em grafos esparsos.
</ul>