import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.data.city_graph import create_graph_network
from src.data.distance_matrix import distance_matrix
from src.data.substations import find_substations
from src.data.substations import calculate_distance_to_substation
from src.data.regions import division_into_secors
from src.data.regions import nodes_to_region
from src.data.population import population_estimation
from src.optimization.sa.sa import SA_algorithm
import yaml
import pickle
# import osmnx as ox

if __name__ == '__main__':
    with open("configs/params.yaml", "r") as f:
        config = yaml.safe_load(f)
    params = config
    city_params = params["city"]

    # Graph
    # G1 = ox.graph_from_place("Lviv, Ukraine", network_type="drive")
    # print(len(G1.nodes))
    print("Creating graph")
    G = create_graph_network(city_params)

    # Calculating distance matrix
    print("Distance matrix")
    dist_matrix = distance_matrix(G, city_params)
    # Calculating distance from nodes to substations
    print("Substantions")
    substations = find_substations(city_params["name"])
    print("Distance to substantions")
    distance_to_substations = calculate_distance_to_substation(G, substations)
    # Division into sectors + demand estimation
    
    print("Division into sectors")
    map_with_grid, city_boundary = division_into_secors(city_params)
    regions, region_to_nodes, node_to_region = nodes_to_region(G, map_with_grid)
    region_to_population = population_estimation(regions, map_with_grid, city_params)
    
    # SA
    best_fitness_lists = []
    n = 1
    for i in range(n):
        best_solution, best_fitness_list = SA_algorithm(G, dist_matrix, params, region_to_population, 
                                                        node_to_region, region_to_nodes, distance_to_substations)
        with open('best_solution_0.pkl', 'wb') as f:
            pickle.dump(best_solution, f)
        with open("best_fitness_list_0.pkl", "wb") as f:
            pickle.dump(best_fitness_list, f)
        best_fitness_lists.append(best_fitness_list)


        # print(len(best_fitness_list))
    # Visualization
    # plot_models_fitness(best_fitness_lists, model_parameters)
    # for i in range(len(best_fitness_lists)):
        # plot_total_fitness(best_fitness_lists[i])
    # visualize_solution(best_solution, G, installed_cs_list = None)