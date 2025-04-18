# import yaml
# with open("configs/params.yaml", "r") as f:
#     config = yaml.safe_load(f)

# params = config
def needs_charge(ev):
    """
    Determines if EV needs to charge based on its current state and threshold.
    Returns True/False
    """
    return (ev["current_charge"] < ev["battery_capacity"]*ev["charging_threshold"])

def nearest_cs_search(charging_station_df, current_location, dist_matrix, nodes_id):
    """
    Sorts charging stations by distance to given location and capacity.
    """
    nearest_cs = charging_station_df.copy()
    cs_nodes = nearest_cs["node"]

    nearest_cs["distance"] = nearest_cs["node"].apply(lambda x: dist_matrix[nodes_id[current_location], nodes_id[x]])
    nearest_cs = nearest_cs.sort_values(by = ["distance", "capacity"], ascending=[True, False])
    return nearest_cs[nearest_cs["distance"] < float("inf")]

def charge_ev(nearest_cs_df, charging_session_df, cs_occupation_df, hour, ev, params):
    """
    Tries to charge the EV at nearest available station.
    Updates occupation_df and charging_df if a port is found.
    """
    # Calculating needed energy
    energy_needed = ev["battery_capacity"] * ev["target_charge"] - ev["current_charge"]
    total_energy_needed = energy_needed/(1-params["charging_stations"]["energy_loss"])
    
    # Calculating departure time (from charging station to next location)
    for j in range(len(ev["parking_periods"])):
        parking_period_start, parking_period_end = ev["parking_periods"][j]
        if hour in range(parking_period_start, parking_period_end + 1):
            departure_time = parking_period_end + 1

    # Searching for a nearest charging station
    while True:
        if len(nearest_cs_df) == 0:
            print("No charhing station is reachable")
            return charging_session_df, cs_occupation_df, ev

        for i in range(len(nearest_cs_df)):
            charging_station_data = nearest_cs_df.iloc[i]
            cs_node = charging_station_data["node"]
            cs_id = charging_station_data["cs_id"]
            cs_capacity = charging_station_data["capacity"]
            num_of_ports = int(charging_station_data["num_of_ports"])
            distance = charging_station_data["distance"]
            # Searching for a free port
            for port in range(1, num_of_ports + 1):
                port_occupation_data = cs_occupation_df[(cs_occupation_df["cs_id"]==cs_id) & (cs_occupation_df["hour"]==hour)&(cs_occupation_df["port"]==port)]
                port_occupation_time = port_occupation_data["occupation_time"].iloc[0]
                if port_occupation_time < 60:
                    break
            if port_occupation_time < 60: # To exit the first For loop
                break

        # If at the current hour each port is occupied for 60 minutes
        # then it is necessary to search for a free port in the next hour, if the day hasn't ended
        if port_occupation_time != 60:
            break
        else:
            if hour + 1 < 24 and hour + 1 < departure_time:
                hour +=1
            else:
                return charging_session_df, cs_occupation_df, ev
        
    # Calculating charging time
    charging_time_minutes = (total_energy_needed/cs_capacity)*60
    # EV charges until it is time for the next trip or until it is charged
    charging_time_minutes = min(charging_time_minutes, max(0, (departure_time - hour)*60 - port_occupation_time))

    # Update charging station occupation dataframe
    if port_occupation_time + charging_time_minutes <=60:
        cs_occupation_df.loc[(cs_occupation_df["cs_id"] == cs_id) & (cs_occupation_df["hour"] == hour) & (cs_occupation_df["port"] == port),\
                              "occupation_time"] = port_occupation_time + charging_time_minutes
        charging_end_hour = hour
    else:
        cs_occupation_df.loc[(cs_occupation_df["cs_id"] == cs_id) & (cs_occupation_df["hour"] == hour) & (cs_occupation_df["port"] == port),\
                              "occupation_time"] = 60
        charging_time_left = charging_time_minutes + port_occupation_time - 60
        next_hour = hour + 1
        while charging_time_left > 60 and next_hour < 24:
            cs_occupation_df.loc[(cs_occupation_df["cs_id"] == cs_id) & (cs_occupation_df["hour"] == next_hour) & (cs_occupation_df["port"] == port),\
                              "occupation_time"] = 60
            charging_time_left -= 60
            next_hour +=1
        if next_hour < 24:
            cs_occupation_df.loc[(cs_occupation_df["cs_id"] == cs_id) & (cs_occupation_df["hour"] == next_hour) & (cs_occupation_df["port"] == port),\
                              "occupation_time"] = charging_time_left
        charging_end_hour = min(23, next_hour)

    # Add new session
    new_session = {
        "cs_id": cs_id,
        "node": cs_node,
        "capacity": cs_capacity,
        "port": port,
        "charging_start_hour": hour,
        "charging_end_hour": charging_end_hour,
        "session_duration": charging_time_minutes,
        "ev_id": ev["ev_id"],
        "distance_from_ev": distance,
        "energy_used": cs_capacity*(charging_time_minutes/60)
    }
        
    charging_session_df.loc[len(charging_session_df)] = new_session
    charging_session_df["cs_id"] = charging_session_df["cs_id"].astype(int)
    # Update EV data
    ev["current_charge"] = ev["current_charge"] + cs_capacity*(charging_time_minutes/60)
    ev["previous_location"] = cs_node

    return charging_session_df, cs_occupation_df, ev