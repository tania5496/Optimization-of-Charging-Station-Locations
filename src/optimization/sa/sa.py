from .initialization import initialize_solution
from .neighboring_solution import generate_new_solution
from src.evaluation.fitness import evaluate_fitness
import random
import math

def SA_algorithm(G, dist_matrix, params, region_to_population, node_to_region, region_to_nodes, distance_to_substations):
    """
    Simulated Annealing optimization algorithm for determining optimal charging station placement.
    Returns:
        dict (best solution),
        list (history of fitness values during optimization (each entry is [fitness, cost, time, avg_dist, grid_loss]))
    """
    sa_params = params["simulated_annealing"]
    station_params = params["charging_stations"]

    nodes = list(G.nodes)
    nodes_id = {nodes[i]: i for i in range(len(nodes))}

    cs_types = station_params["types_list"]

    current_solution = initialize_solution(nodes, cs_types)
    best_solution = current_solution

    current_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss = evaluate_fitness(current_solution, params, dist_matrix,\
                                    region_to_population, node_to_region, region_to_nodes, nodes_id, distance_to_substations)
    best_fitness = current_fitness
    best_fitness_list = [[current_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss]]

    
    T = sa_params["initial_temperature"]
    cooling_rate = sa_params["cooling_rate"]
    iterations = sa_params["iterations"]
    bad_attempts_limit = sa_params["bad_attempts_limit"]
    testing_worse_solution = False
    for iteration in range(iterations):
        print("Iteration", iteration + 1, "/", iterations)

        new_solution = generate_new_solution(current_solution, nodes, station_params)
        new_fitness, new_fitness_cost, new_fitness_charging_time, new_fitness_avg_distance, new_fitness_grid_loss = evaluate_fitness(new_solution, params, dist_matrix, region_to_population, node_to_region,
                                        region_to_nodes, nodes_id, distance_to_substations)
        delta_fitness = new_fitness - current_fitness

        if delta_fitness < 0 or (random.random() < math.exp(-delta_fitness / T)):
            current_solution = new_solution
            current_fitness = new_fitness
            if delta_fitness > 0:
                testing_worse_solution = True
                bad_attemmpts = bad_attempts_limit
            else:
                testing_worse_solution = False

            if current_fitness < best_fitness:
                best_solution = current_solution
                best_fitness = current_fitness
                best_fitness_list.append([new_fitness, new_fitness_cost, new_fitness_charging_time, new_fitness_avg_distance, new_fitness_grid_loss])
            else:
                best_fitness_list.append(best_fitness_list[-1]) # when best solution hasn't changed
        else:
            best_fitness_list.append(best_fitness_list[-1]) # when best solution hasn't changed
            if testing_worse_solution:
                bad_attemmpts -=1
        if testing_worse_solution and bad_attemmpts == 0:
            current_solution = best_solution
            current_fitness = best_fitness
            testing_worse_solution = False

        T *= cooling_rate

    return best_solution, best_fitness_list