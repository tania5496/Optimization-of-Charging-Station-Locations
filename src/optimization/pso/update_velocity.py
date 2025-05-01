import random

def update_velocity(particle, velocity, personal_best, global_best, pso_params):
    """
    Updates the velocity vector for a PSO particle using inertia and cognitive/social components.
    Each charging station's change in port number is influenced by its difference from the particle's
    personal best and the global best solutions.

    Returns: dict (new velocity for the particle)
    """
    w = pso_params["w"]
    c1 = pso_params["c1"]
    c2 = pso_params["c2"]

    new_velocity = dict()
    all_stations = set(particle.keys())
    all_stations = all_stations.union(personal_best.keys())
    all_stations = all_stations.union(global_best.keys())
    for station in all_stations:

        if station in personal_best:
            p_best_ports = personal_best[station]
        else:
            p_best_ports = 0

        if station in global_best:
            g_best_ports = global_best[station]
        else:
            g_best_ports = 0

        if station in particle:
            particle_ports = particle[station]
        else:
            particle_ports = 0

        p_best_diff = p_best_ports - particle_ports
        g_best_diff = g_best_ports - particle_ports
        
        new_velocity[station] = int(w * velocity.get(station, 0) + c1 * random.random() * p_best_diff + c2 * random.random() * g_best_diff)

    return new_velocity