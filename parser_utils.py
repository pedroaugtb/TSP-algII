# parser_utils.py
import math


##
# @brief Faz o parsing de um arquivo TSPLIB para extrair coordenadas.
#
# @param filename Caminho para o arquivo TSPLIB.
# @return Lista de tuplas contendo as coordenadas (x, y) de cada nó.
def parse_tsplib(filename):
    coords = []
    with open(filename, "r") as f:
        in_section = False
        for line in f:
            line = line.strip()
            if line.startswith("NODE_COORD_SECTION"):
                in_section = True
                continue
            if line.startswith("EOF"):
                break
            if in_section:
                parts = line.split()
                if len(parts) >= 3:
                    x = float(parts[1])
                    y = float(parts[2])
                    coords.append((x, y))
    return coords


##
# @brief Calcula a matriz de distâncias entre todas as coordenadas fornecidas.
#
# @param coords Lista de tuplas contendo as coordenadas (x, y).
# @return Matriz 2D onde cada entrada [i][j] representa a distância entre as cidades i e j.
def compute_distance_matrix(coords):
    n = len(coords)
    distance_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                (x1, y1) = coords[i]
                (x2, y2) = coords[j]
                distance_matrix[i][j] = math.dist((x1, y1), (x2, y2))
            else:
                distance_matrix[i][j] = 0.0
    return distance_matrix


##
# @brief Calcula o custo total de uma rota usando a matriz de distâncias.
#
# @param route Lista de índices representando a ordem de visita das cidades.
# @param distance_matrix Matriz de distâncias entre as cidades.
# @return O custo total da rota, somando as distâncias entre cidades consecutivas e voltando ao início.
def compute_cost(route, distance_matrix):
    cost = 0.0
    for i in range(len(route)):
        cost += distance_matrix[route[i]][route[(i + 1) % len(route)]]
    return cost
