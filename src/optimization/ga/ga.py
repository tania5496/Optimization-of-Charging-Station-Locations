from src.evaluation.fitness import evaluate_fitness
from .initialization import initialize_population
from .selection import select_parents
from .crossover import crossover
from .mutation import mutate
import numpy as np

def genetic_algorithm(G, dist_matrix, params, region_to_population, node_to_region, region_to_nodes, distance_to_substations):
    """
    Genetic algorithm for determining optimal charging station placement.
    Returns: 
        dict (best solution),
        list (history of fitness values during optimization (each entry is [fitness, cost, time, avg_dist, grid_loss]))
    """
    nodes = list(G.nodes)
    nodes_id = {nodes[i]: i for i in range(len(nodes))}

    population_size  = params["genetic_algorithm"]["population_size"]
    generations = params["genetic_algorithm"]["generations"]
    mutation_rate = params["genetic_algorithm"]["mutation_rate"]
    crossover_point = params["genetic_algorithm"]["crossover_point"]
    num_of_parents = params["genetic_algorithm"]["num_of_parents"]
    generations = params["genetic_algorithm"]["generations"]
    station_params = params["charging_stations"]
    max_ports_per_station = station_params["max_ports_per_station"]
    cs_types = station_params["types_list"]

    population = initialize_population(nodes, cs_types, population_size)

    # Fitness evaluation
    fitness = [evaluate_fitness(solution, params, dist_matrix,region_to_population,\
                                node_to_region, region_to_nodes, nodes_id, distance_to_substations) for solution in population]
    total_fitness = [solution_fitness[0] for solution_fitness in fitness]

    best_solution = population[np.argmin(total_fitness)]
    best_fitness_list = [fitness[np.argmin(total_fitness)]]

    for generation in range(generations):
        print("Generation", generation + 1, "/", generations)

        # Selecting parents
        parents, parents_fitness = select_parents(population, num_of_parents, num_of_parents)
        # Offspring
        offsprings = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                # Crossover
                offspring = crossover(parents[i], parents[i + 1], parents_fitness[i], parents_fitness[i + 1], crossover_point, max_ports_per_station)
                offsprings.append(offspring)

        # Adding mutations
        offsprings = [mutate(offspring, nodes, cs_types, mutation_rate, max_ports_per_station) for offspring in offsprings]

        # Adding offsprings to population
        population = population + offsprings
        offspring_fitness = [evaluate_fitness(offspring, params, dist_matrix, region_to_population,\
                                            node_to_region, region_to_nodes, nodes_id, distance_to_substations) for offspring in offsprings]
        fitness = fitness + offspring_fitness

        # Selecting solutions that remain in the population
        best_indices = np.argsort([solution_fitness[0] for solution_fitness in fitness])[:population_size]
        population = [population[i] for i in best_indices]
        fitness = [fitness[i] for i in best_indices]

        # Best solution
        total_fitness = [solution_fitness[0] for solution_fitness in fitness]
        best_solution = population[np.argmin(total_fitness)]
        best_fitness_list.append(fitness[np.argmin(total_fitness)])

    return best_solution, best_fitness_list
