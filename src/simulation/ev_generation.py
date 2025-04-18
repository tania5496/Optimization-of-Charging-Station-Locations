import random
# import yaml
# with open("configs/params.yaml", "r") as f:
#     config = yaml.safe_load(f)

# params = config
def generate_route(ev, nodes):
    """
    Generates a daily route for an EV, including destinations and parking periods.
    Returns:
        tuple: (list of locations, list of parking periods)
    """

    locations = []
    departure_times = []

    # Fron home
    home_location = ev["home_location"]
    morning_commute_hour = ev["commute_hours"]["morning"]
    
    # Route destinations
    number_of_destinations = random.choices([1, 2, 3], weights = [0.6, 0.3, 0.1], k=1)[0] # Generating number of destinations that are not home
    
    locations.append(home_location) # Home location (start point)
    random_locations = random.choices(nodes, k = number_of_destinations) # Work and other locations
    for location in random_locations:
        while location == home_location:
                location = random.choice(nodes)
        locations.append(location)
    locations.append(home_location) # Home location (end point)

    # Route times
    trip_time = {
        "random morning trip": range(0, ev["commute_hours"]["morning"]),
        "random noon trip": range(ev["commute_hours"]["morning"], ev["commute_hours"]["evening"]),
        "random evening trip": range(ev["commute_hours"]["evening"], 24)
    }
    
    departure_times.append(morning_commute_hour) # Departure to work

    if number_of_destinations > 1:
        for i in range(number_of_destinations-1):
            ranom_trip_type = random.choice(["random morning trip", "random noon trip", "random evening trip"])
            random_trip_time = random.choice(trip_time[ranom_trip_type])
            departure_times.append(random_trip_time)

    departure_times.append(ev["commute_hours"]["evening"]) # Departure from work
    departure_times.sort()

    parking_periods = []
    for i in range(number_of_destinations + 2): # +2 since the route starts and ends at home
        if i == 0:
            parking_periods.append([0, departure_times[i]-1])
        elif i == number_of_destinations + 1:
            parking_periods.append([departure_times[i-1], 23])
        else:
            parking_periods.append([departure_times[i-1], departure_times[i]-1])
    return locations, parking_periods

def generate_EVs(regions, region_to_population, region_to_nodes, nodes, params):
    """
    Generates EV agents based on population data
    Returns:
    list: dict (list of EV dictionaries)
    """
    EVs = []
    ev_id = 0

    for region in regions:
        ev_num = int(region_to_population[region] * params["ev"]["ev_per_capita"])

        potential_home_locations = region_to_nodes[region]
        if len(potential_home_locations) == 0:
            break
        ev_home_locations = random.choices(potential_home_locations, k = ev_num)
        for i in range(ev_num):
            battery_capacity = params["ev"]["battery_capacity"]
            initial_soc_range = params["simulation"]["initial_soc_range"]
            charging_threshold = params["simulation"]["charging_threshold"]
            target_charge = params["simulation"]["min_target_charge"]
            morning_commute_hours = params["simulation"]["commute_hours"]["morning"]
            evening_commute_hours = params["simulation"]["commute_hours"]["evening"]

            ev = {
                    "ev_id": ev_id,
                    "home_location": ev_home_locations[i],
                    "previous_location": ev_home_locations[i],
                    "battery_capacity": random.uniform(battery_capacity[0], battery_capacity[1]),
                    "current_charge": None,  # Will be assigned below
                    "charging_threshold": random.uniform(charging_threshold[0], charging_threshold[1]),  # When to start charging
                    "target_charge": random.uniform(target_charge[0], target_charge[1]),  # Target charge level
                    "commute_hours": {
                        "morning": random.uniform(morning_commute_hours[0], morning_commute_hours[1]),  # Morning commute hour (6-9 AM)
                        "evening": random.uniform(evening_commute_hours[0], evening_commute_hours[1])  # Evening commute hour (4-7 PM)
                    },
                    "destinations": None,  # Will be assigned below
                    "parking_periods": None  # Will be assigned below
            }
            
            # Assigning current state of charge
            ev["current_charge"] = ev["battery_capacity"] * random.uniform(initial_soc_range[0], initial_soc_range[1])

            # Assigning route (destinations + departure_times)
            destinations, parking_periods = generate_route(ev, nodes)
            ev["destinations"] = destinations
            ev["parking_periods"] = parking_periods
            EVs.append(ev)
            ev_id +=1
    return EVs