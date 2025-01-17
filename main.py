# main.py
import sys, os, time, json
from parser_utils import parse_tsplib, compute_distance_matrix
from algorithms import branch_and_bound, twice_around_tree, christofides


##
# @brief Processa um arquivo TSP, executa algoritmos e coleta resultados.
#
# @param filename Caminho para o arquivo TSP.
# @param time_limit Tempo limite para execução dos algoritmos (em segundos).
# @return Dicionário com os dados necessários para salvar os resultados.
def process_file(filename, otimos, time_limit=1800):
    coords = parse_tsplib(filename)
    dist_matrix = compute_distance_matrix(coords)
    qtd_cidades = len(coords)

    print(f"\nProcessando {filename} com {qtd_cidades} cidades.")

    # Twice-Around-The-Tree
    print("\n--- Twice-Around-The-Tree ---")
    route_twice, cost_twice, time_twice = twice_around_tree(
        dist_matrix, time_limit=time_limit
    )
    print(f"Tempo de execução TAT: {time_twice}")
    print(f"Custo da rota TAT: {cost_twice}")

    # Christofides
    print("\n--- Christofides ---")
    route_ch, cost_ch, time_ch = christofides(dist_matrix, time_limit=time_limit)
    print(f"Tempo de execução Christofides: {time_ch}")
    print(f"Custo da rota Christofides: {cost_ch}")

    print("\n--- Branch-and-Bound ---")
    route_bb, cost_bb, time_bb = branch_and_bound(dist_matrix, time_limit=1)
    print(f"Tempo de execução B&B: {time_bb}")
    print(f"Custo da rota B&B: {cost_bb}")

    # Obter nome base do arquivo para buscar custo ótimo
    nome_arquivo = os.path.basename(filename)
    custo_otimo = otimos.get(nome_arquivo, "NA")

    # Como o algoritmo B&B não executa em menos de 30 minutos, seus resultados
    # estão omitidos no json final.
    result = {
        "Nome_Arquivo": nome_arquivo,
        "Tempo_TAT": str(time_twice),
        "Tempo_Christofides": str(time_ch),
        # "Tempo B&B": str(time_bb),
        "Custo_Otimo": str(custo_otimo),
        "Custo_TAT": str(cost_twice),
        "Custo_Christofides": str(cost_ch),
        # "Custo B&B": str(cost_bb),
        "Qtd_Cidades": str(qtd_cidades),
    }

    return result


##
# @brief Função principal que gerencia a execução do programa.
#
# Lê arquivos de entrada, processa cada instância TSP, executa algoritmos e salva resultados em JSON.
def main():
    input_folder = "tsp_instances"
    time_limit = 1800  # 30 minutos
    results_list = []

    # Carregar valores ótimos de otimos.json
    otimos_path = "otimos.json"
    if os.path.exists(otimos_path):
        with open(otimos_path, "r") as f:
            otimos_list = json.load(f)
        # Converter lista para dicionário
        otimos = { entry["Nome_Arquivo"]: entry["Custo_Otimo"] for entry in otimos_list }
    else:
        print(f"Atenção: {otimos_path} não encontrado. Custo ótimo não será disponibilizado.")
        otimos = {}

    # Definir quais arquivos serão processados
    if len(sys.argv) >= 2:
        filenames = [sys.argv[1]]
    else:
        filenames = []
        for file in os.listdir(input_folder):
            if file.endswith(".tsp"):
                filenames.append(os.path.join(input_folder, file))

    output_filename = "tsp_results.json"

    # Processar cada arquivo, salvar incrementalmente após cada processamento
    for filename in filenames:
        result = process_file(filename, otimos, time_limit)
        results_list.append(result)
        print(f"Processado {filename}.")

        with open(output_filename, "w") as outfile:
            json.dump(results_list, outfile, indent=4)
        print(f"Resultados atualizados salvos em {output_filename}")

    print(f"\nTodos os resultados foram salvos em {output_filename}")


if __name__ == "__main__":
    main()
