from src.simulation.demand_simulation import simulate_charging_demand

def cs_cost_penalty(solution, station_params):
    """
    Calculates total installation cost for a given solution.
    Inputs:
        solution (dict): mapping of (node, station_type) to number of stations
        params (dict): metadata about charging station types and costs
    Returns: 
        float: total cost.
    """
    total_cost = 0
    for charging_station in solution:
        cs_type = charging_station[1]
        cost = station_params["types"][cs_type]["cost"]
        number_of_ports = solution[charging_station]
        total_cost += cost*number_of_ports
    return total_cost

def avg_time_per_kWh(charging_session_data):
    """
    Calculates average required time to charge 1 kWh from charging session data
    Inputs:
        charging_session_data (DataFrame): simulated EV charging sessions
    Returns:
        float: average charging time per 1 kWh.
    """
    return sum(charging_session_data["session_duration"])/(sum(charging_session_data["energy_used"])/1000)

def average_distance_to_cs(charging_session_data):
    """
    Calculates average distance from EVs to the nearest charging stations
    Inputs:
        charging_session_data (DataFrame): simulated EV charging sessions
    Returns:
        float: average distance to a charging station.
    """
    return charging_session_data["distance_from_ev"].mean()

def total_grid_loss(solution, distance_to_substations):
    """
    Calculates grid loss penalty based on distance from charging stations to substations.
    Inputs:
        solution (dict): charging station solution
        distance_to_substations (dict): distance from nodes to the nearest substations
    Returns:
        float: proxy measure of grid loss.
    """
    total_distance = 0
    for station in solution:
        cs_node = station[0]
        total_distance += distance_to_substations[cs_node]
    return total_distance

def evaluate_fitness(solution, params, dist_matrix, region_to_population, node_to_region, region_to_nodes, nodes_id, distance_to_substations):
    """
    Evaluates the fitness of a solution using weighted objectives.
    Returns:
        tuple: (fitness score, cost score, charging time score, distance score, grid loss score)
    """
    alpha = params["evaluation_weights"]["alpha"]
    beta = params["evaluation_weights"]["beta"]
    gamma = params["evaluation_weights"]["gamma"]
    delta = params["evaluation_weights"]["delta"]

    cs_occupation_df, charging_session_data = simulate_charging_demand(solution, params, region_to_population, node_to_region, region_to_nodes,
                                dist_matrix, nodes_id)
    

    cs_cost = cs_cost_penalty(solution, params["charging_stations"])
    avg_charging_time_kWh = avg_time_per_kWh(charging_session_data)
    avg_distance= average_distance_to_cs(charging_session_data)
    grid_loss = total_grid_loss(solution, distance_to_substations)

    fitness = alpha*cs_cost + beta*avg_charging_time_kWh + gamma*avg_distance + delta*grid_loss
    return fitness, alpha*cs_cost, beta*avg_charging_time_kWh, gamma*avg_distance, delta*grid_loss