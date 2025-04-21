from .data_preperation import create_cs_dataframe, create_cs_occupation_dataframe
from .ev_charging import needs_charge, nearest_cs_search, charge_ev
from .ev_generation import generate_EVs
import random
import pandas as pd
def simulate_charging_demand(solution, params, region_to_population, node_to_region, region_to_nodes, dist_matrix, nodes_id):
    """
    Simulates EV charging behavior and station usage for a full day.
    Returns:
        pd.DataFrame (charging station data),
        pd.DataFrame (charging session data)
    """
    random.seed(12)
    regions = list(region_to_population.keys())
    nodes = list(node_to_region.keys())
    simulation_hours = params["simulation"]["simulation_hours"]

    charging_station_df = create_cs_dataframe(solution, params["charging_stations"])

    charging_session_df = pd.DataFrame(columns = ["cs_id", "node", "capacity", "port", "charging_start_hour", \
                                          "charging_end_hour", "session_duration", "ev_id", "distance_from_ev", "energy_used"])
    charging_session_df["cs_id"] = charging_session_df["cs_id"].astype(int)
    charging_session_df["node"] = charging_session_df["node"].astype(int)

    cs_occupation_df = create_cs_occupation_dataframe(charging_station_df, simulation_hours)

    # For each region initialize ev
    EVs = generate_EVs(regions, region_to_population, region_to_nodes, nodes, params)

    avg_consumption_per_km = params["ev"]["avg_consumption_per_km"] #Wh/km

    # Simulate each hour
    for hour in range(simulation_hours):

        # For each EV
        for i in range(len(EVs)):
            ev = EVs[i]
            
            previous_location = ev["previous_location"]
            # Update location and state of charge
            for j in range(len(ev["parking_periods"])):
                parking_period_start, parking_period_end = ev["parking_periods"][j]
                if hour in range(parking_period_start, parking_period_end + 1):
                    current_location = ev["destinations"][j]
                    break
            if previous_location != current_location:
                distance = dist_matrix[nodes_id[previous_location], nodes_id[current_location]]
                energy_used = distance * (avg_consumption_per_km/1000)
                ev["current_charge"] -= energy_used

            # Charge if needed
            if needs_charge(ev):
                nearest_cs_df = nearest_cs_search(charging_station_df, current_location, dist_matrix, nodes_id)
                charging_session_df, cs_occupation_df, ev = charge_ev(nearest_cs_df, charging_session_df, cs_occupation_df, hour, ev, params)

            ev["previous_location"] = current_location
    
    return cs_occupation_df, charging_session_df