import random

def initialize_population(nodes, station_types, population_size):
    """
    Generates an initial population of random solutions for the genetic algorithm.
    Returns dict (mapping from (node, station_type) to number of ports installed)
    """
    population = []
    for i in range(population_size):
        solution = {}
        for node in random.sample(nodes, k=random.randint(5, 100)):
            cs_type = random.choice(station_types)
            cs_number = random.choices([1,2,3,4], [0.3, 0.4, 0.2, 0.1])[0]
            solution[(node, cs_type)] = cs_number
        population.append(solution)
    return population
