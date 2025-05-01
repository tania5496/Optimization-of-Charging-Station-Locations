import random

def initialize_solution(nodes, station_types):
    """
    Initializes a random solution by assigning a random number of charging stations of random types to randomly selected nodes.
    Returns dict (mapping from (node, station_type) to number of ports installed)
    """
    solution = {}

    for node in random.sample(nodes, k=random.randint(10, 100)):
        cs_type = random.choice(station_types)
        cs_number = random.choices([1,2,3,4], [0.3, 0.4, 0.2, 0.1])[0]
        solution[(node, cs_type)] = cs_number
    return solution