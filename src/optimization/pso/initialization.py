import random

def initialize_particles(nodes, station_types, num_particle):
    """
    Generates an initial population of random solutions for the particle swarm optimization algorithm.
    Returns dict (mapping from (node, station_type) to number of ports installed)
    """
    particles = []
    velocities = []
    for i in range(num_particle):
        solution = {}

        velocity = {}
        for node in random.sample(nodes, k=random.randint(5, 100)):
            cs_type = random.choice(station_types)
            cs_number = random.choices([1,2,3,4], [0.3, 0.4, 0.2, 0.1])[0]
            solution[(node, cs_type)] = cs_number
            velocity[(node, cs_type)] = 0
        particles.append(solution)
        velocities.append(velocity)
    return particles, velocities
