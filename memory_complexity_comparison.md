# Comparação de uso de memória em grafos

###
V = vértice
E = arestas
## O(V²) — Matriz de adjacência
<ul>
<li>Usa uma matriz V×V.
<li> acesso O(1) para checar arestas.
<li>consome muita memória.
<li>melhor usado grafos densos (muitas arestas, E ≈ V²).
</ul>

## O(V·E) — Matriz de incidência (densa)
<ul> 
<li>Estrutura V×E (nós × arestas).
<li>útil em contextos matemáticos específicos.
<li>extremamente ineficiente em memória.
<lI>raramente usada na forma densa; prefira versão esparsa.
</ul>

## O(V + E) — Lista de adjacência

<ul>

<li>Armazena vizinhos de cada vértice.</li>
<li>muito mais econômica.
<li>checar aresta pode ser mais lento que O(1).
<li>melhor usado em grafos esparsos.
</ul>