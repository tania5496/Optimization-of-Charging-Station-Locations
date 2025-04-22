import random

def mutate(solution, nodes, cs_types, mutation_rate, max_ports_per_station):
    """
    Applies mutation to a solution with a given probability.
    Returns: dict (the mutated solution)
    """
    if random.random() >= mutation_rate: # No mutation
        return solution
    
    rng = random.Random()
    action = rng.choice(["add", "remove", "change_type"])

    if action == "remove":  # Remove random stations
        num_of_stations = random.choices([1, 2, 3, 4], [0.4, 0.3, 0.2, 0.1])[0]
        for i in range(num_of_stations):
            random_cs = random.choice([cs for cs in solution])
            num_of_ports = random.choice(range(0, solution[random_cs]))
            if num_of_ports < solution[random_cs]:
                solution[random_cs] = solution[random_cs] - num_of_ports
            else:
                solution.pop(random_cs)
    elif action == "add":  # Add a new stations
        num_of_stations = random.choices([1, 2, 3, 4], [0.4, 0.3, 0.2, 0.1])[0]
        for i in range(num_of_stations):
            random_node = random.choice(nodes)
            cs_type = random.choice(cs_types)
            num_of_ports = random.choice(range(1, 4))
            if (random_node, cs_type) in solution:
                solution[(random_node, cs_type)] = min(4, solution[(random_node, cs_type)] + num_of_ports)
            else: 
                solution[(random_node, cs_type)] = num_of_ports
    else:  # Change station type
        num_of_stations = random.choices([1, 2, 3, 4], [0.4, 0.3, 0.2, 0.1])[0]
        for i in range(num_of_stations):
            cs_node, cs_type = random.choice([cs for cs in solution])
            new_cs_types_list = cs_types.copy()
            new_cs_types_list.remove(cs_type)

            new_cs_type = random.choice(new_cs_types_list)
            if (cs_node, new_cs_type) in solution:
                solution[(cs_node, new_cs_type)] = min(max_ports_per_station, \
                                                        solution[(cs_node, cs_type)] + solution[(cs_node, new_cs_type)])
            else:
                solution[(cs_node, new_cs_type)] = solution[(cs_node, cs_type)]

            solution.pop((cs_node, cs_type))

    return solution