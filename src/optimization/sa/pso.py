from .initialization import initialize_particles
from .update_velocity import update_velocity
from .update_particle import update_particle
from src.evaluation.fitness import evaluate_fitness
import numpy as np

def PSO_algorithm(G, dist_matrix, EV_data, CS_data, model_parameters, region_to_population, node_to_region, region_to_nodes, distance_to_substations, installed_cs = False):
    """
    Particle Swarm Optimization algorithm for optimizing the placement of EV charging stations.
    Returns:
        dict (best solution),
        list (history of fitness values during optimization (each entry is [fitness, cost, time, avg_dist, grid_loss]))
    """
    nodes = list(G.nodes)
    nodes_dict = {nodes[i]: i for i in range(len(nodes))}

    particles, velocities = initialize_particles(nodes, CS_data["CS_list"], num_particle = model_parameters["particles"])
    p_best = particles.copy()
    p_best_fitness = [evaluate_fitness(particle, model_parameters, CS_data, EV_data, dist_matrix,\
                                    region_to_population, node_to_region, region_to_nodes, nodes_dict, distance_to_substations, installed_cs)[0] for particle in particles]
    g_best = p_best[np.argmin(p_best_fitness)]
    g_best_fitness = min(p_best_fitness)

    iterations = model_parameters["iterations"]

    g_best_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss = evaluate_fitness(g_best, model_parameters, CS_data, EV_data, dist_matrix,\
                                    region_to_population, node_to_region, region_to_nodes, nodes_dict, distance_to_substations, installed_cs)
    best_fitness_list = [[g_best_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss]]
    
    for iteration in range(iterations):
        print("Iteration", iteration + 1, "/", iterations)

        for i in range(len(particles)):
            velocities[i] = update_velocity(particles[i], velocities[i], p_best[i], g_best, model_parameters)
            particles[i] = update_particle(particles[i], velocities[i], CS_data["max_stations_num"])
            current_fitness = evaluate_fitness(particles[i], model_parameters, CS_data, EV_data, dist_matrix,\
                                    region_to_population, node_to_region, region_to_nodes, nodes_dict, distance_to_substations, installed_cs)[0]
            
            if current_fitness < p_best_fitness[i]:
                p_best[i] = particles[i]
                p_best_fitness[i] = current_fitness

            if current_fitness < g_best_fitness:
                g_best = particles[i]
                g_best_fitness = current_fitness
        g_best_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss = evaluate_fitness(g_best, model_parameters, CS_data, EV_data, dist_matrix,\
                                    region_to_population, node_to_region, region_to_nodes, nodes_dict, distance_to_substations, installed_cs)
        best_fitness_list.append([g_best_fitness, fitness_cost, fitness_charging_time, fitness_avg_distance, fitness_grid_loss])
        print(f"Best Fitness = {g_best_fitness}")
    # plot_fitness(best_fitness_list)

    return g_best, best_fitness_list
