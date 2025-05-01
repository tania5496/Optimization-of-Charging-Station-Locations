from .initialization import initialize_particles
from .update_velocity import update_velocity
from .update_particle import update_particle
from .mutation import mutate
from src.evaluation.fitness import evaluate_fitness
import numpy as np

def PSO_algorithm(G, dist_matrix, params, region_to_population, node_to_region, region_to_nodes, distance_to_substations):
    """
    Particle Swarm Optimization algorithm for optimizing the placement of EV charging stations.
    Returns:
        dict (best solution),
        list (history of fitness values during optimization (each entry is [fitness, cost, time, avg_dist, grid_loss]))
    """
    nodes = list(G.nodes)
    nodes_id = {nodes[i]: i for i in range(len(nodes))}
    
    pso_params = params["particle_swarm_optimization"]
    station_params = params["charging_stations"]
    cs_types = station_params["types_list"]
    num_particle = pso_params["particles"]
    iterations = pso_params["iterations"]
    station_params = params["charging_stations"]
    max_ports_per_station = station_params["max_ports_per_station"]

    particles, velocities = initialize_particles(nodes, cs_types, num_particle)

    # Fitness evaluation
    fitness = [evaluate_fitness(particle, params, dist_matrix, region_to_population,\
                                node_to_region, region_to_nodes, nodes_id, distance_to_substations) for particle in particles]
    total_fitness = [particle_fitness[0] for particle_fitness in fitness]

    p_best = particles.copy()
    p_best_fitness = fitness 
    g_best = particles[np.argmin(total_fitness)]
    g_best_fitness = fitness[np.argmin(total_fitness)]
    best_fitness_list = [g_best_fitness]

    
    for iteration in range(iterations):
        print("Iteration", iteration + 1, "/", iterations)

        # Update velocity and position of particle
        for i in range(len(particles)):
            velocities[i] = update_velocity(particles[i], velocities[i], p_best[i], g_best, pso_params)
            particles[i] = update_particle(particles[i], velocities[i], max_ports_per_station)
            particles[i] = mutate(particles[i], nodes, cs_types, max_ports_per_station)
            current_fitness = evaluate_fitness(particles[i], params, dist_matrix, region_to_population,\
                                node_to_region, region_to_nodes, nodes_id, distance_to_substations)
                                
            current_total_fitness = current_fitness[0]
            
            # Update p_best
            p_best_total_fitness = p_best_fitness[i][0]
            if current_total_fitness < p_best_total_fitness:
                p_best[i] = particles[i]
                p_best_fitness[i] = current_fitness

            # Update g_best
            g_best_total_fitness = g_best_fitness[0]
            if current_total_fitness < g_best_total_fitness:
                g_best = particles[i]
                g_best_fitness = current_fitness

        best_fitness_list.append(g_best_fitness)

    return g_best, best_fitness_list
