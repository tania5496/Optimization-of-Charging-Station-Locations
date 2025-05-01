import random

def add_random_station(solution, nodes, cs_types, max_ports_per_station):
    """
    Adds a random number of new charging stations to randomly selected nodes, considering port limits.
    Returns: dict (updated solution dictionary after station additions)
    """
    new_solution = solution.copy()

    # Calculating total number of cs ports in each node
    total_node_ports = {cs_node: 0 for cs_node, cs_type in new_solution}
    for station in new_solution:
        total_node_ports[station[0]] = total_node_ports[station[0]] + new_solution[station]
        
    num_of_stations = random.choices([1, 2, 3, 4, 5, 6], [0.05, 0.1, 0.15, 0.2, 0.25, 0.25])[0]
    for i in range(num_of_stations):

        # Generate random node, type 
        random_node = random.choice(nodes)
        cs_type = random.choice(cs_types)
        while random_node in total_node_ports.keys() and total_node_ports[random_node] == max_ports_per_station:
            random_node = random.choice(nodes)

        # Generate random number of ports taking into account number of existing stations in the node
        if random_node in total_node_ports.keys():
            num_of_ports = random.choice(range(0, max_ports_per_station - total_node_ports[random_node])) + 1
        else:
            num_of_ports = random.choice(range(0, max_ports_per_station)) + 1

        # Generate random number of ports taking into account number of existing stations in the node
        if (random_node, cs_type) in new_solution:
            new_solution[(random_node, cs_type)] = new_solution[(random_node, cs_type)] + num_of_ports
        else:
            new_solution[(random_node, cs_type)] = num_of_ports

        # Update num_cs_ports
        if random_node in total_node_ports.keys():
            total_node_ports[random_node] = total_node_ports[random_node] + num_of_ports
        else: 
            total_node_ports[random_node] = num_of_ports
    return new_solution

def remove_random_station(solution):
    """
    Removes a random number of charging stations (or ports) from the current solution.
    Returns: dict (updated solution after station removals)
    """
    new_solution = solution.copy()

    num_of_stations = random.choices([1, 2, 3, 4, 5, 6], [0.05, 0.1, 0.15, 0.2, 0.25, 0.25], k = 1)[0]
    num_of_stations = min(num_of_stations, len(list(new_solution.keys())))

    for i in range(num_of_stations):
        random_station = random.choice(list(new_solution.keys()))
        num_of_ports_remove = random.choice(range(1, new_solution[random_station] + 1)) 

        if num_of_ports_remove < new_solution[random_station]:
            new_solution[random_station] = new_solution[random_station] - num_of_ports_remove
        else:
            new_solution.pop(random_station)
    return new_solution

def change_station_type(solution, cs_types, max_ports_per_station):
    """
    Randomly changes the types of selected charging stations, transferring ports where necessary.
    Returns: dict (updated solution with some station types changed)
    """
    new_solution = solution.copy()
    num_of_stations = random.choices([1, 2, 3, 4], [0.4, 0.3, 0.2, 0.1])[0]

    for i in range(num_of_stations):
        cs_node, cs_type = random.choice([station for station in new_solution])
        new_cs_types_list = cs_types.copy()
        new_cs_types_list.remove(cs_type)

        new_cs_type = random.choice(new_cs_types_list)
        if (cs_node, new_cs_type) in new_solution:
            new_solution[(cs_node, new_cs_type)] = min(max_ports_per_station, \
                                                       new_solution[(cs_node, cs_type)] + new_solution[(cs_node, new_cs_type)])
        else:
            new_solution[(cs_node, new_cs_type)] = new_solution[(cs_node, cs_type)]

        new_solution.pop((cs_node, cs_type))
    
    return new_solution

def generate_new_solution(solution, nodes, station_params):
    """
    Generates a new candidate solution by performing a random modification (add, remove, or change).
    Returns: dict (new candidate solution after applying a random change)
    """
    cs_types = station_params["types_list"]
    max_ports_per_station = station_params["max_ports_per_station"]

    action = random.choice(["add", "remove", "change_type"])
    print(action)
    if action == "add":
        new_solution = add_random_station(solution, nodes, cs_types, max_ports_per_station)
    elif action == "remove":
        new_solution = remove_random_station(solution)
    else:
        new_solution = change_station_type(solution, cs_types, max_ports_per_station)

    return new_solution
