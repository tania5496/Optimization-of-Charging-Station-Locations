import pandas as pd

def create_cs_dataframe(solution, station_params):
    """
    Combines installed and new (optimized) charging stations into a single DataFrame.
    Returns a DataFrame with columns: cs_id, node, capacity, num_of_ports.
    """
    # Merge installed station and solution station data
    station_node_list, capacity_list, station_ports_list  = [], [], []

    for (station_node, station_type), station_ports in solution.items():
        capacity = station_params["types"][station_type]["capacity"]

        station_node_list.append(station_node)
        capacity_list.append(capacity)
        station_ports_list.append(station_ports)

    # Create station dataframes
    charging_station_df = pd.DataFrame({
        "cs_id": range(len(station_node_list)),
        "node": station_node_list,
        "capacity": capacity_list,
        "num_of_ports": station_ports_list,
    })
    return charging_station_df


def create_cs_occupation_dataframe(charging_station_df, simulation_hours):
    """
    Initializes charging station port occupation for 24-hour simulation.
    Returns a DataFrame with columns: cs_id, capacity, port, hour, occupation_time
    """
    cs_occupation_df = pd.DataFrame(columns=["cs_id", "capacity", "port", "hour", "occupation_time"])
    
    for _, row in charging_station_df.iterrows():
        cs_id = row["cs_id"]
        capacity = row["capacity"]
        number_of_ports = int(row["num_of_ports"])

        # Creating rows for each port and hour
        for port in range(1, number_of_ports + 1):
            for hour in range(simulation_hours):
                cs_occupation_df.loc[len(cs_occupation_df)] = {"cs_id": cs_id, "capacity": capacity, "port": port, "hour": hour, "occupation_time": 0.0}

    cs_occupation_df["cs_id"] = cs_occupation_df["cs_id"].astype(int)
    return cs_occupation_df
