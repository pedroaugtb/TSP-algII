# algorithms.py
import time, math
from heapq import heappush, heappop
from parser_utils import compute_cost
import networkx as nx


##
# @brief Algoritmo Branch and Bound para o problema do Caixeiro Viajante.
#
# @param distance_matrix Matriz de distâncias entre as cidades.
# @param time_limit Tempo limite para a execução do algoritmo (em segundos).
# @return Tupla contendo a melhor rota encontrada, o custo associado e o tempo decorrido.
def branch_and_bound(distance_matrix, time_limit=1800):
    start_time = time.time()
    n = len(distance_matrix)
    best_cost = float("inf")
    best_route = None
    stack = [([0], 0.0, set([0]))]

    ##
    # @brief Função auxiliar para calcular um limite inferior para um dado caminho.
    #
    # @param route Rota atual.
    # @param cost Custo parcial até o momento.
    # @param visited Conjunto de cidades já visitadas.
    # @return Limite inferior estimado para completar a rota.
    def bound(route, cost, visited):
        b = cost
        not_visited = [i for i in range(n) if i not in visited]
        if not not_visited:
            return b
        min_edges = [min(distance_matrix[k]) for k in not_visited]
        b += sum(min_edges)
        return b

    while stack:
        if time.time() - start_time > time_limit:
            return ("NA", "NA", "NA")
        route, cost_parcial, visited = stack.pop()
        if len(route) == n:
            cost_total = cost_parcial + distance_matrix[route[-1]][route[0]]
            if cost_total < best_cost:
                best_cost = cost_total
                best_route = route[:]
            continue
        for city in range(n):
            if city not in visited:
                new_cost = cost_parcial + distance_matrix[route[-1]][city]
                if new_cost < best_cost:
                    b = bound(route + [city], new_cost, visited.union({city}))
                    if b < best_cost:
                        stack.append((route + [city], new_cost, visited.union({city})))
    elapsed = time.time() - start_time
    return (
        best_route if best_route is not None else "NA",
        best_cost if best_route is not None else None,
        elapsed,
    )


##
# @brief Constrói uma Árvore Geradora Mínima (MST) usando o algoritmo de Prim.
#
# @param distance_matrix Matriz de distâncias entre as cidades.
# @return Lista de arestas que compõem a MST.
def build_mst_prim(distance_matrix):
    n = len(distance_matrix)
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distance_matrix[i][j])
    mst = nx.minimum_spanning_tree(G, algorithm="prim")
    # Obter lista de arestas da MST
    mst_edges = list(mst.edges())
    return mst_edges


##
# @brief Algoritmo Twice-Around-Tree para aproximação do TSP.
#
# @param distance_matrix Matriz de distâncias entre as cidades.
# @param time_limit Tempo limite para a execução do algoritmo (em segundos).
# @return Tupla contendo a rota aproximada, o custo associado e o tempo decorrido.
def twice_around_tree(distance_matrix, time_limit=1800):
    start_time = time.time()
    n = len(distance_matrix)
    # Construir MST
    mst_edges = build_mst_prim(distance_matrix)

    # Duplicar arestas da MST para multigrafo
    double_edges = mst_edges[:] + mst_edges[:]
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(range(n))
    for u, v in double_edges:
        multigraph.add_edge(u, v)

    # Encontrar circuito Euleriano
    euler_circuit = list(nx.eulerian_circuit(multigraph, source=0))
    euler_tour = [euler_circuit[0][0]] + [v for u, v in euler_circuit]

    # Simplificar para obter rota sem repetições de vértices
    visited = set()
    route = []
    for city in euler_tour:
        if city not in visited:
            route.append(city)
            visited.add(city)

    if time.time() - start_time > time_limit:
        return ("NA", "NA", "NA")

    cost = compute_cost(route, distance_matrix)
    elapsed = time.time() - start_time
    return (route, cost, elapsed)


##
# @brief Algoritmo de Christofides para aproximação do TSP.
#
# @param distance_matrix Matriz de distâncias entre as cidades.
# @param time_limit Tempo limite para a execução do algoritmo (em segundos).
# @return Tupla contendo a rota aproximada, o custo associado e o tempo decorrido.
def christofides(distance_matrix, time_limit=1800):
    start_time = time.time()
    n = len(distance_matrix)

    mst_edges = build_mst_prim(distance_matrix)

    # Construir grafo completo para matching
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            # Usar peso negativo para simular mínimo emparelhamento
            G.add_edge(i, j, weight=-distance_matrix[i][j])

    # Encontrar vértices de grau ímpar na MST
    odd_vertices = []
    degree_count = [0] * n
    for u, v in mst_edges:
        degree_count[u] += 1
        degree_count[v] += 1
    for i in range(n):
        if degree_count[i] % 2 != 0:
            odd_vertices.append(i)

    # Subgrafo induzido pelos vértices de grau ímpar para matching
    odd_subgraph = G.subgraph(odd_vertices)

    # Emparelhamento máximo no subgrafo (equivale a mínimo devido aos pesos negativos)
    matching = nx.algorithms.matching.max_weight_matching(
        odd_subgraph, maxcardinality=True
    )
    matching = list(matching)

    # Unir MST + matching
    multiedges = mst_edges + matching

    # Criar grafo multiconexo usando NetworkX para passeio Euleriano
    multigraph = nx.MultiGraph()
    multigraph.add_nodes_from(range(n))
    for u, v in multiedges:
        multigraph.add_edge(u, v)

    # Encontrar circuito Euleriano
    euler_circuit = list(nx.eulerian_circuit(multigraph, source=0))
    # Converter circuito Euleriano em lista de vértices na ordem de visita
    euler_tour = [euler_circuit[0][0]] + [v for u, v in euler_circuit]

    # Aplicar atalhos para obter rota TSP (visita cada vértice uma vez)
    visited = set()
    route = []
    for city in euler_tour:
        if city not in visited:
            route.append(city)
            visited.add(city)

    # Verificação de tempo
    if time.time() - start_time > time_limit:
        return ("NA", "NA", "NA")

    cost = compute_cost(route, distance_matrix)
    elapsed = time.time() - start_time
    return (route, cost, elapsed)
